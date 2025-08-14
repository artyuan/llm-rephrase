from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    api_key=openai_api_key
)

TAB_NAMES = ["Professional", "Casual", "Polite", "Social-media"]
GRAPH_CONFIG = {
    "configurable": {"thread_id": 41}
}
