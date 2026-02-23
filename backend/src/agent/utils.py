import json

from copilotkit import CopilotKitMiddleware
from deepagents import create_deep_agent
from langchain_litellm import ChatLiteLLM
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph

model = ChatLiteLLM(model="github_copilot/gpt-5-mini")


def get_weather(city: str) -> str:
    """Get weather for a given city.

    Args:
        city: The city to get weather for

    Returns:
        JSON string with weather data including temperature, conditions, humidity, and wind speed
    """
    # In a real app, you'd call a weather API here
    # For now, return mock data with all the properties the frontend expects
    weather_data = {
        "location": city,
        "temperature": 72,
        "unit": "F",
        "weather": "sunny",
        "humidity": 45,
        "windSpeed": 8,
    }

    # Return as JSON string so frontend can parse it
    return json.dumps(weather_data)


def build_agent() -> CompiledStateGraph:
    checkpointer = MemorySaver()
    agent_graph = create_deep_agent(
        model=model,
        tools=[get_weather],
        middleware=[CopilotKitMiddleware()],
        system_prompt="You are a helpful assistant",
        checkpointer=checkpointer,
    )
    print("[AGENT] Deep Agents graph created")
    print(agent_graph)
    return agent_graph


if __name__ == "__main__":
    # Quick test to make sure the agent is working `python src/agent/utils.py`
    # Build the agent
    agent_graph = build_agent()
    # Run the agent with a thread_id config (required when using a checkpointer)
    config = {"configurable": {"thread_id": "test-session-1"}}
    result = agent_graph.invoke(
        {"messages": [{"role": "user", "content": "what is the weather in sf"}]}, config=config
    )
    # Print the agent's response
    print(result["messages"][-1].content)
