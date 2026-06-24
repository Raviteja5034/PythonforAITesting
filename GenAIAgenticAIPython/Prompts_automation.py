import os    # os module is used to setting up api key in the enviornment
OPEN_API_KEY=os.environ.get("OPEN_API_KEY","")
from langchain_openai import OpenAI  #OpenAI is class used input prompts to LLM and 
#provide the response(OpenAI-normal text)
llm=OpenAI(api_key=OPEN_API_KEY)
response=llm.invoke("provide me details of a transformer")
response1=llm.invoke("As an electrical engineer provide me explanation of transformer in 2 sentences")
prompt="As an AI engineer provide me explanation of transformer in 2 paragraphs"
response2=llm.invoke(prompt)
print(response)
print("========================")
print(response1)
print("========================")
print(response2)
