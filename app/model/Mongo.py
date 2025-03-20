from pymongo import MongoClient
import json
import os
from datetime import datetime

class Mongo:
    def __init__(self):
        self.db = self.connection()
        

    def connection(self):
        try:
            URI = os.getenv("MONGO_URL")
            client = MongoClient(URI)
            db = client['chatbot']  
            print("Conexão bem-sucedida ao MongoDB")
            return db
        except Exception as e:
            print(f"Erro ao conectar ao MongoDB: {str(e)}")
            return None

    def get_chat_history(self,user_id: int):
        history = self.db.chat_history.find_one({"user_id": user_id})
        
        if history:
            return {"user_id": user_id, "conversa": history["conversa"]}
        return {"user_id": user_id, "conversa": []}

    def save_chat_history(self, user_id: int, question: str, response: str):
        existing_entry = self.db.chat_history.find_one({"user_id": user_id})
        
        if existing_entry:
            self.db.chat_history.update_one(
                {"user_id": user_id},
                {"$push": {"conversa": {"usuario": question, "chat": response}}}
            )
        else:
            self.db.chat_history.insert_one({
                "user_id": user_id,
                "conversa": [{"usuario": question, "chat": response}],
                "timestamp": datetime.utcnow()
            })