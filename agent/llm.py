import os
#pyrefly: ignore 
from dotenv import load_dotenv
#pyrefly:  ignore
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    groq_api_key = os.getenv("GROQ_API_KEY"),
    model = "openai/gpt-oss-120b",
    temperature = 0.5,
    reasoning_effort="medium",
)

def getllm():
    return llm