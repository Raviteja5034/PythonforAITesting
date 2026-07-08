from phi.agent import Agent 
from phi.model.openai import OpenAIChat

def add_tool(a1,a2):
    sum=a1+a2
    return str(sum)
def mul_tool(b1,b2):
    mul=str(b1*b2)  # Function output should be always str 
    return mul
def div_tool(c1,c2):
    div=str(c1/c2)
    return div
def sub_tool(d1,d2):
    sub=d1-d2
    return str(sub)

a1=Agent(name="Calculator agent",
         model=OpenAIChat(id="gpt-4o-mini",temperature=0),
         tools=[add_tool,mul_tool,div_tool,sub_tool],
         instructions=["Call add_tool function when user asks for sum",
                       "Call mul_tool function when user asks for Multiplication",
                       "Call div_tool function when user asks for division",
                       "Call sub_tool function when user asks for Subtraction"],
         system_prompt="This calculator only used for integer values only.It should not take negitive values." \
         "It should allow only tools hanlded operations Not other mathemetical operations"
         )
text=input("Please enter text")
response=a1.run(text)
print(response.content)



