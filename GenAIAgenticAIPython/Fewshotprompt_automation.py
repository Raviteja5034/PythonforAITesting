import os 
from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

OPEN_API_KEY = os.environ.get("OPEN_API_KEY","")
chat_llm=ChatOpenAI(api_key=OPEN_API_KEY , model="gpt-5.4-nano")

messages=[SystemMessage(content="Act as drugs.com pharmasist,advise medication usage"),
          HumanMessage(content="What is use of Paracetamol")]
response=chat_llm.invoke(messages)
print(response.content)

messages1=[SystemMessage(content="Act as drugs.com pharma assist"),
           HumanMessage(content="What is use of Azee500 ?"),
           AIMessage(content="It is used for Bacterial infections"),
           HumanMessage(content="what is use of Vymada100mg?")]
response2=chat_llm(messages1)
print(response2.content)

path="C:/Users/RavitejaPalakurthi/Documents/Archive/prompts.txt"
File=open(path,'w')
File.write(response.content+response2.content)
File.close()

File1=open(path,'r')
Filedata=File1.read()
