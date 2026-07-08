from phi.agent import Agent 
from phi.model.openai import OpenAIChat 
# Tools 
def evenchecker(num1):
    try:
      if num1%2==0:
        return (f"{num1} is even number")
      else:
        return (f"{num1} is odd number")
    except Exception as e:
       return f"Exception occured :{str(e)}"
      
def oddchecker(num1):
    try:
      if num1%2!=0:
       return (f"{num1} is odd number")
      else:
        return (f"{num1} is even number")
    except Exception as e:
       return f"Exception occured :{str(e)}"
      
agent=Agent(name="EvenorOddchecker Agent",
            model=OpenAIChat(id="gpt-4-turbo"),
            tools=[evenchecker,oddchecker],
            instructions=["call evenchecker if user inputs even number",
                          "call oddchecker if user inputs odd number"],
            system_prompt="This agent only checks the input number is even or add ,this should not perform any calculations"
            )

number=input("Input any number")
response1=agent.run(number)
print(response1.content)