import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    groq_api_key = os.getenv("GROQ_API_KEY"),
    model = "openai/gpt-oss-120b",
    temperature = 0.5,
    max_tokens = 2000,
    timeout = 10,
    max_retries=2,
)

message = [
    ("system","You are a helpful assistant."),
    
]

response = llm.invoke(message)
print(response.content)

def getllm():
    return llm