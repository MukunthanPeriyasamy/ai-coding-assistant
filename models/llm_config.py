from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
model_name = "openai/gpt-oss-20b"

llm = ChatGroq(model_name=model_name, api_key=groq_api_key)