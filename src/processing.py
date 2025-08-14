from src.rephrase_agent import build_graph
from src.config import GRAPH_CONFIG

graph = build_graph()

def rephrase_text(user_input: str) -> dict:
    """Run the AI model to get rephrased versions."""
    return graph.invoke({'user_input': user_input}, config=GRAPH_CONFIG)