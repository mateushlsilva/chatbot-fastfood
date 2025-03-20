from app.core.Config import llm, vectorstore
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Union
from langchain.tools import StructuredTool
from pydantic import BaseModel
from langchain.agents import AgentType, initialize_agent
import logging

class BuscarCardapioParams(BaseModel):
    param: str = 'menu'

class EnviarPedidosParams(BaseModel):
    pedido: str

class ChatService:
    def __init__(self):
        self.llm = llm
        self.retriever = vectorstore.as_retriever()
        self.busca_tool = StructuredTool.from_function(
            func=self.buscarCardapio,
            name="buscarCardapio",
            description="Útil para obter o cardápio do fast food.",
            args_schema=BuscarCardapioParams
        )
        self.enviar_tool = StructuredTool.from_function(
            func=self.enviarPedidos,
            name="enviarPedidos",
            description="Útil para enviar o pedido para o fast food.",
            args_schema=EnviarPedidosParams
        )
        self.tools = [self.busca_tool, self.enviar_tool]
        logging.basicConfig(level=logging.INFO)



    def ask(self, question):
        template = """Você é um assistente amigável de um Fast Food. A sua missão é atender os clientes respondendo dúvidas e anotando pedidos.

        Use a ferramenta `buscarCardapio` para buscar informações sobre o cardápio. O parâmetro `param` deve conter o item que o usuário está procurando.

        Use a ferramenta `enviarPedidos` para anotar o pedido do cliente. Se um usuário pedir qualquer item do cardápio, registre esse pedido com a ferramenta `enviarPedidos`. O parâmetro `pedido` deve conter o pedido completo.


        Exemplo:
        Usuário: Qual o preço da pizza?
        Agente: Action: `buscarCardapio`, Action Input: `param: pizza`

        Usuário: Eu quero uma pizza e uma coca.
        Agente: Action: `enviarPedidos`, Action Input: `pedido: pizza e coca`

        Usuário: Qual o menu?
        Agente: Action: `buscarCardapio`, Action Input: `param: menu`

        Usuário: Eu quero uma pizza de calabresa.
        Agente: Action: `enviarPedidos`, Action Input: `pedido: pizza de calabresa`

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
            result = response.invoke({"input": question})
            logging.info(f"Resposta do agente: {result}")
            return result["output"]
        except Exception as e:
            logging.error(f"Erro ao executar o agente: {e}", exc_info=True)
            return f"Ocorreu um erro: {e}"
    
   
    def buscarCardapio(self, params: dict) -> List[str]:
        """Busca informações no banco vetorial sobre o cardápio com base em uma consulta."""
        try:
            print(f"Tipo de params: {type(params)}")
            print(f"Valor de params: {params}")

            if isinstance(params, str):
                params = BuscarCardapioParams(param=params)

            elif isinstance(params, dict):
                if "param" in params:  
                    params = BuscarCardapioParams(param=params["param"])
                else:  
                    raise ValueError("Formato inválido de 'params'")

            if "cardápio" in params.param.lower() or "menu" in params.param.lower():
                print("Ta no menu")
                docs = vectorstore._client.get_collection(name='langchain').get()
                return docs["documents"]

          
            docs = vectorstore.similarity_search(params.param)
            return [doc.page_content for doc in docs]

        except Exception as e:
            logging.error(f"Erro ao buscar cardápio: {e}", exc_info=True)
            return []

    def enviarPedidos(self, pedido: EnviarPedidosParams) -> str:
        """Anota o pedido do cliente"""
        print(f"Tipo de params: {type(pedido)}")
        print(f"Valor de params: {pedido}")
        if isinstance(pedido, str):
            pedido = EnviarPedidosParams(pedido=pedido)
        elif isinstance(pedido, dict):
            if "pedido" in pedido:
                pedido = EnviarPedidosParams(pedido=pedido["pedido"])
            else:
                raise ValueError("Formato inválido de 'pedido'")
                
        logging.info(f"Pedido recebido: {pedido.pedido}")
        return f"Pedido '{pedido.pedido}' anotado com sucesso!"

    def vericarAuth():
        pass