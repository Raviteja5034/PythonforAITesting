#import needed packages
import os
from operator import itemgetter
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

load_dotenv()
#load local Vector DB
vectorstore = FAISS.load_local("./faiss_index2", OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"]), allow_dangerous_deserialization=True)
retriever   = vectorstore.as_retriever(search_kwargs={"k": 4})
llm         = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"], model="gpt-3.5-turbo", temperature=0)
prompt      = ChatPromptTemplate.from_messages([
    ("system", "Answer using only the context below.\n\nContext:\n{context}"),
    ("human",  "{question}"),
])

retrieve_docs = itemgetter("question") | retriever
#make the chain of retriving and asking question to the LLM
chain = RunnableParallel({
    "answer":      RunnablePassthrough.assign(context=retrieve_docs | (lambda docs: "\n\n".join(d.page_content for d in docs))) | prompt | llm | StrOutputParser(),
    "source_docs": retrieve_docs,
})
#take the questio from the user
question = input("Question: ")
#ask the question to the chain
result   = chain.invoke({"question": question})
print("\nAnswer:", result["answer"])
print("Sources:", {doc.metadata.get("source") for doc in result["source_docs"]})