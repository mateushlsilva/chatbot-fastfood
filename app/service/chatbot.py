from app.core.config import llm


class ChatService:
    def __init__(self):
        self.llm = llm

    def ask(self, question):
        response = self.llm.invoke(question)
        return response.content
