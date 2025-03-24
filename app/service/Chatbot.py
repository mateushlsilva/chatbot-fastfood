from app.core.Config import llm, vectorstore
from langchain_core.prompts import ChatPromptTemplate
from typing import List
from langchain.tools import StructuredTool
from pydantic import BaseModel
from langchain.agents import AgentType, initialize_agent
import logging
from app.model.Mongo import Mongo
import requests

class BuscarCardapioParams(BaseModel):
    param: str = 'menu'
    usuarioId: str 

class EnviarPedidosParams(BaseModel):
    pedido: str
    usuarioId: str 

class ChatService:
    def __init__(self):
        self.mongo = Mongo()
        self.llm = llm
        self.retriever = vectorstore.as_retriever()
        self.busca_tool = StructuredTool.from_function(
            func=self.buscarCardapio,
            name="buscarCardapio",
            description="Útil para obter o cardápio do fast food. , incluindo o ID do usuário.",
            args_schema=BuscarCardapioParams,
            handle_tool_error=True
        )
        self.enviar_tool = StructuredTool.from_function(
            func=self.enviarPedidos,
            name="enviarPedidos",
            description="Útil para enviar o pedido para o fast food, incluindo o ID do usuário.",
            args_schema=EnviarPedidosParams
        )
        self.tools = [self.busca_tool, self.enviar_tool]
        self.short_term_memory = {}
        logging.basicConfig(level=logging.INFO)



    def ask(self, question, user):
        user_id = user['id']
        name_user = user['name']

        if user_id not in self.short_term_memory:
            self.short_term_memory[user_id] = []

        self.short_term_memory[user_id].append(f"Usuário: {question}")

        if len(self.short_term_memory[user_id]) > 5:
            self.short_term_memory[user_id].pop(0)

        short_term_context = "\n".join(self.short_term_memory[user_id])

        template = """Você é um assistente amigável de um Fast Food. A sua missão é atender os clientes respondendo dúvidas e anotando pedidos.

            Nome do usuário: {name_user}
            ID do usuário: {user_id}

            Histórico recente da conversa:
            {short_term_context}

            Use a ferramenta `buscarCardapio` para buscar informações sobre o cardápio. O parâmetro `param` deve conter o item que o usuário está procurando e o parâmetro `usuarioId` deve conter o ID do usuário.

            Use a ferramenta `enviarPedidos` para anotar o pedido do cliente. O parâmetro `pedido` deve conter o pedido completo e o parâmetro `usuarioId` deve conter o ID do usuário.

            Use SEMPRE o ID correto do usuário ao chamar uma ferramenta. O ID do usuário é: {user_id}
            ID do usuário correto: {user_id}. Nunca use outro ID.

            Exemplo:
            Usuário: Qual o preço da pizza?
            Agente: Action: `buscarCardapio`, Action Input: `param: pizza, usuarioId: {user_id}`

            Usuário: Eu quero uma pizza e uma coca.
            Agente: Action: `enviarPedidos`, Action Input: `pedido: pizza e coca, usuarioId: {user_id}`

            Usuário: Qual o menu?
            Agente: Action: `buscarCardapio`, Action Input: `param: menu, usuarioId: {user_id}`

            Usuário: Eu quero uma pizza de calabresa.
            Agente: Action: `enviarPedidos`, Action Input: `pedido: pizza de calabresa, usuarioId: {user_id}`

            {tools}

            {format_instructions}

            {input}

            {agent_scratchpad}"""



        prompt = ChatPromptTemplate.from_template(template)
        try:
            response = initialize_agent(
                self.tools,
                self.llm,
                agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                agent_kwargs={"prompt": prompt},
            )
            result = response.invoke({"input": question, 
                "usuarioId": user_id,  
                "name_user": name_user,
                "short_term_context": short_term_context})
            logging.info(f"Resposta do agente: {result}")
            self.short_term_memory[user_id].append(f"Agente: {result['output']}")
            self.mongo.save_chat_history(user_id=user['id'], question=question, response=result["output"])
            return result["output"]
        except Exception as e:
            logging.error(f"Erro ao executar o agente: {e}", exc_info=True)
            return f"Ocorreu um erro: {e}"
    
   
    def buscarCardapio(self, param: str, usuarioId: str) -> List[str]:
        """Busca informações no banco vetorial sobre o cardápio com base em uma consulta."""
        try:
            params = BuscarCardapioParams(param=param, usuarioId=usuarioId)

            # Verifica se o usuário quer ver o cardápio inteiro
            if "cardápio" in params.param.lower() or "menu" in params.param.lower():
                print("Buscando menu completo...")
                docs = vectorstore._client.get_collection(name='langchain').get()
                return docs["documents"]

            # Busca no banco vetorial
            if params.param:
                docs = vectorstore.similarity_search(params.param)
                return [doc.page_content for doc in docs]
            
            return []
        
        except Exception as e:
            logging.error(f"Erro ao buscar cardápio: {e}", exc_info=True)
            return []


    def enviarPedidos(self, pedido: str, usuarioId: str) -> str:
        """Anota o pedido do cliente"""
        print(f"Pedido: {pedido}, Usuário ID: {usuarioId}")
        
        request = requests.post("http://127.0.0.1:8080/pedido", json={"pedido": pedido, "usuarioId": usuarioId})
        
        if request.status_code != 201:
            return f"Erro ao enviar pedido: {request.text}"
        
        logging.info(f"Pedido recebido: {pedido}")
        return f"Pedido '{pedido}' anotado com sucesso!"

    
    def buscarHistorico(self, user_id):
        """Busca o histórico de conversas do usuário"""
        return self.mongo.get_chat_history(user_id=user_id)
    