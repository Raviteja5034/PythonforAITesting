from phi.agent import Agent
from phi.model.openai import OpenAIChat

simpleagent=Agent(name="Simple agent for chat",
                  model=OpenAIChat(id="gpt-4-turbo",temperature=0)
                  )
response=simpleagent.run("What is Cosine similarity?")
print(response.content)