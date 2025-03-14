from app.core.config import llm


class ChatService:
    def __init__(self):
        self.llm = llm

    def ask(self, question):
        messages = [
            ("system", "Você é um assistente amigável de um Fast Food. A sua missão é atender os clientes respondendo dúvidas e anotando pedidos."),
            ("human", question)
        ]
        response = self.llm.invoke(messages)
        return response.content
    
    def buscarCardapio():
        pass

    def enviarPedidos():
        pass

    def vericarAuth():
        pass