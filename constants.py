from dotenv import load_dotenv
import os

# API keys
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Data collection
driver_path = "C:/Users/nagpa/chromedriver.exe"
site = "https://www.iitg.ac.in/iitg_faculty_all"

# VectorDB
index_name = "chatbot"
ENV = 'gcp-starter'
CHUNK_SIZE = 3000
CHUNK_OVERLAP = 20

# Models
EMB_MODEL = "all-MiniLM-L6-v2"
QUERY_MODEL = "text-davinci-003"
CHAT_MODEL = "gpt-3.5-turbo"