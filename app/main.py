from fastapi import FastAPI
from app.service.chatbot import ChatService
from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str

app = FastAPI()

chatbot =  ChatService()

@app.get("/")
def read_root():
    cardapio = chatbot.buscarCardapio()
    print(cardapio)
    return {"Hello": "World"}

@app.post("/conversa")
def conversa(request: QuestionRequest):
    response = chatbot.ask(request.question)
    #response = chatbot.buscarCardapio({"params":request.question})
    return {"question": request.question, "response": response}