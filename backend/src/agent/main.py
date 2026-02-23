import os

import uvicorn
from ag_ui_langgraph import add_langgraph_fastapi_endpoint
from copilotkit import LangGraphAGUIAgent
from dotenv import load_dotenv
from fastapi import FastAPI

from agent.utils import build_agent

load_dotenv()

app = FastAPI(
    title="Weather Application Assistant",
    description="Get personalized weather updates based on your location and preferences",
    version="1.0.0",
)

try:
    agent_graph = build_agent()
    print(agent_graph)
    add_langgraph_fastapi_endpoint(
        app=app,
        agent=LangGraphAGUIAgent(
            name="weather_application_assistant",
            description="Get personalized weather updates based on your location and preferences",
            graph=agent_graph,
        ),
        path="/",
    )
    print("[MAIN] Agent registered")
except Exception as e:
    print(f"[ERROR] Failed to build agent: {str(e)}")
    raise


@app.get("/healthz")
async def health_check() -> dict:
    """Health check"""
    return {
        "status": "healthy",
        "service": "weather-application-assistant",
        "version": "1.0.0",
    }


def main() -> None:
    """Run server"""
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", "8123"))

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
