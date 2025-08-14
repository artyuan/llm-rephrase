import pytest
from rephrase_agent import build_graph

config = {"configurable": {'thread_id': 41}}


@pytest.fixture
def graph():
    """A pytest fixture that returns a graph object."""
    return build_graph()


def test_agent_rephrase(graph):
    prompt = "Hey team, we have to talk about about progress of the project"
    response = graph.invoke({'user_input': prompt}, config=config)
    assert response['moderator'] is False
    assert response['polite_output'] is not None
    assert response['professional_output'] is not None
    assert response['social_media_output'] is not None
    assert response['casual_output'] is not None


def test_inappropriate_prompt(graph):
    prompt = "It's horrible working with incompetent people"
    response = graph.invoke({'user_input': prompt}, config=config)
    assert response['moderator'] is True
