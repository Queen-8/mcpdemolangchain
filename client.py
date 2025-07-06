import os
import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
# from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from typing import Any
from pydantic import SecretStr
from dotenv import load_dotenv
load_dotenv() # 加载 .env 文件中的 OPENROUTER_API_KEY

import asyncio

async def main():
    connections: dict[str, Any] = {
        "math": {
            "command": "python",
            "args": [os.path.abspath("mathserver.py")],
            "transport": "stdio",
        },
        "weather": {
            "command": "python",
            "args": [os.path.abspath("weather.py")],
            "transport": "stdio",
        }
    }
    client = MultiServerMCPClient(connections)

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable is required")

    tools=await client.get_tools()
    print(f"Loaded {len(tools)} tools: {[tool.name for tool in tools]}")
    
    model = ChatOpenAI(
        model="openai/gpt-4o-mini",
        base_url="https://openrouter.ai/api/v1",
        api_key=SecretStr(api_key),
    )
    agent = create_react_agent(model, tools)
    
    math_response = await agent.ainvoke(
        {"messages":[{"role":"user","content":"what's (3 + 1) * 12?"}]}
    )
    
    # print("Math response:", math_response['message'][-1].content)
    # print("Raw math_response:", math_response) 
    print("Answer:", math_response["messages"][-1].content)

    weather_response = await agent.ainvoke(
        {"messages":[{"role": "user", "content":"请使用 get_weather 工具查询纽约的天气"}]}
    )

    # print("Raw math_response:", weather_response) 
    print("Answer:", weather_response["messages"][-1].content)
    # print("Weather response:", weather_response['message'][-1].content)

asyncio.run(main())
