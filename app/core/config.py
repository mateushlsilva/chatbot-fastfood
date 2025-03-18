import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document


load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    LLM_MODEL = "gemini-1.5-pro"
    TEMPERATURE = 0

    @classmethod
    def get_llm(cls):
        """Retorna uma instância do LLM."""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY não foi encontrada. Verifique o arquivo .env.")
        
        return ChatGoogleGenerativeAI(
            model=cls.LLM_MODEL,
            temperature=cls.TEMPERATURE
        )

    # @classmethod
    # def get_embeddings(cls, text_list):  # Adicionado o parâmetro text_list
    #     """Gera embeddings para uma lista de textos."""
    #     if not cls.GOOGLE_API_KEY:
    #         raise ValueError("GOOGLE_API_KEY não foi encontrada. Verifique o arquivo .env.")

    #     embeddings_model = GoogleGenerativeAIEmbeddings(model='models/text-embedding-004')
    #     embeddings = embeddings_model.embed_documents(text_list)
    #     return embeddings
    @classmethod
    def get_embeddings(cls):
        """Retorna uma instância de GoogleGenerativeAIEmbeddings."""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY não foi encontrada. Verifique o arquivo .env.")

        return GoogleGenerativeAIEmbeddings(model='models/text-embedding-004')


    @classmethod
    def create_vectorstore(cls):
        """Criação do banco vetorial usando o Chroma."""
        itens = [
            "Hambúrguer Artesanal - Ingredientes: carne bovina, pão brioche, queijo cheddar, alface, tomate - Preço: R$24,90",
            "Pizza de Calabresa - Ingredientes: massa fina, calabresa, queijo mussarela, cebola - Preço: R$38,50",
            "Refrigerante Coca-Cola - Ingredientes: refrigerante - Preço: R$6,00",
            "Frango Frito - Ingredientes: frango, óleo, sal, pimenta - Preço: R$19,90",
            "Batata Frita - Ingredientes: batata, óleo, sal - Preço: R$12,50",
            "Milkshake de Chocolate - Ingredientes: leite, chocolate, sorvete de creme - Preço: R$14,90",
            "Pizza de Marguerita - Ingredientes: massa fina, molho de tomate, queijo mussarela, manjericão - Preço: R$35,00",
            "Burguer Vegetariano - Ingredientes: hambúrguer de grão de bico, alface, tomate, cebola, molho de iogurte - Preço: R$22,00",
            "Refrigerante Fanta - Ingredientes: refrigerante - Preço: R$6,50",
            "Torrada com Queijo - Ingredientes: pão, queijo, manteiga - Preço: R$8,00"
        ]
        
        if not 'chroma_db' in os.listdir():
            print('Não existe banco vetorial. Criando...')
            documents = [Document(page_content=item) for item in itens]
            vectorstore = Chroma.from_documents(documents, cls.get_embeddings(), persist_directory="./chroma_db")
        else:
            print('Banco vetorial já existe. Carregando...')
            vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=cls.get_embeddings())
        return vectorstore


llm = Config.get_llm()
vectorstore = Config.create_vectorstore()
