import asyncio
from rasa.core.agent import Agent

async def main():
    agent = Agent.load("models")
    for msg in ["hello world", "hi", "bye"]:
        responses = await agent.handle_text(msg)
        texts = [r.get("text") for r in responses]
        print(f"IN:  {msg}\nOUT: {texts}\n")

asyncio.run(main())
