from typing_extensions import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from typing import Literal
from src.config import llm
from src.prompt import moderator_prompt, rephrase_prompt
from src.parsers import ModeratorParser, RephraseParser


class GraphState(TypedDict):
    """
    Graph state is a dictionary that contains information we want to propagate to, and modify in, each graph node.
    """
    user_input: Annotated[str, "The initial input from the user."]
    moderator: Annotated[str | None, "Indicates if the input has passed moderation."]
    professional_output: Annotated[str | None, "The professionally-toned version of the user input."]
    casual_output: Annotated[str | None, "The casually-toned version of the user input."]
    polite_output: Annotated[str | None, "The politely-toned version of the user input."]
    social_media_output: Annotated[str | None, "The social media-friendly version of the user input."]


def moderate_input(state: GraphState) -> GraphState:
    """
    Runs the input text through a moderation LLM to detect inappropriate content.

    Args:
        state (GraphState): A dictionary-like state object containing the 'user_input' string.

    Returns:
        GraphState: A dictionary containing:
            - 'moderator' (bool): True if the content is flagged as inappropriate, False otherwise.
    """
    user_input = state['user_input']
    structured_llm = llm.with_structured_output(ModeratorParser)
    moderator_chain = moderator_prompt | structured_llm
    result = moderator_chain.invoke({"input": user_input})
    return {'moderator': result['output']}


def check_moderation(state: GraphState) -> Command[Literal["rephrase_sentence", END]]:
    """
    Determines the next step in the workflow based on moderation results.
    - If 'moderator' is True (content flagged), go to END.
    - If 'moderator' is False, proceed to 'rephrase_sentence'.
    """
    return Command(goto=END) if state["moderator"] else Command(goto='rephrase_sentence')


def rephrase_sentence(state: GraphState) -> GraphState:
    """
    Rephrases the user input into multiple writing styles using an LLM.

    Args:
        state (GraphState): A dictionary-like state object containing the 'user_input' string.

    Returns:
        GraphState: A dictionary containing rephrased text in different styles:
            - 'professional_output': Professional tone rephrase.
            - 'casual_output': Informal/casual tone rephrase.
            - 'polite_output': Polite and respectful tone rephrase.
            - 'social_media_output': Social media–friendly tone rephrase.
    """
    user_input = state['user_input']
    structured_llm = llm.with_structured_output(RephraseParser)
    rephrase_chain = rephrase_prompt | structured_llm
    result = rephrase_chain.invoke({"input": user_input})
    return {'professional_output': result['professional_output'],
            'casual_output': result['casual_output'],
            'polite_output': result['polite_output'],
            'social_media_output': result['social_media_output'],
            }


def build_graph():
    workflow = StateGraph(GraphState)

    # Define the nodes
    workflow.add_node("moderate_input", moderate_input)
    workflow.add_node("check_moderation", check_moderation)
    workflow.add_node("rephrase_sentence", rephrase_sentence)

    workflow.add_edge(START, "moderate_input")
    workflow.add_edge("moderate_input", "check_moderation")
    workflow.add_edge("rephrase_sentence", END)
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


if __name__ == "__main__":
    graph = build_graph()
    config = {"configurable": {'thread_id': 41}}
    prompt = "hey team, we have to talk about how the project is going"
    response = graph.invoke({'user_input': prompt}, config=config)
    print(response)

