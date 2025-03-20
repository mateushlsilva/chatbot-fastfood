from fastapi import FastAPI, Depends
from app.service.Chatbot import ChatService
from pydantic import BaseModel
from app.middleware.Authorization import Authorization
from typing import Tuple

class QuestionRequest(BaseModel):
    question: str

app = FastAPI()

chatbot =  ChatService()
user_middleware = Authorization()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/perfil")
def get_perfil(user_info: Tuple[dict, str] = Depends(user_middleware)):
    user, token = user_info
    return {"message": "Perfil do usuário", "user": user, "token": token, "historic": chatbot.buscarHistorico(user['id'])}

@app.post("/conversa")
def conversa(request: QuestionRequest, user_info: Tuple[dict, str] = Depends(user_middleware)):
    user, token = user_info
    response = chatbot.ask(request.question, user)
    return {"question": request.question, "response": response}