import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Carrega variáveis de ambiente do .env
load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    LLM_MODEL = "gemini-1.5-pro"
    TEMPERATURE = 0

    @classmethod
    def get_llm(cls):
        """Retorna uma instância do LLM configurada corretamente."""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY não foi encontrada. Verifique o arquivo .env.")
        
        return ChatGoogleGenerativeAI(
            model=cls.LLM_MODEL,
            temperature=cls.TEMPERATURE
        )

# Criando uma instância do LLM que pode ser usada em outras partes do código
llm = Config.get_llm()
