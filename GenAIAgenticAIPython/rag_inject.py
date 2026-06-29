import os,argparse # argparse is to take input from the terminal 
from dotenv import load_dotenv # reads API key 
from langchain_community.document_loaders import PyPDFLoader #Read PDF file
from langchain.text_splitter import RecursiveCharacterTextSplitter #Split large text into small chunks 
from langchain_openai import OpenAIEmbeddings #Convert text → vectors (numbers) 
from langchain_community.vectorstores import FAISS # stores vectors in FAISS DB 
load_dotenv #reads .env file 
# take all the needed pdf file path
parser = argparse.ArgumentParser()
parser.add_argument("--pdf", required=True)
args = parser.parse_args()

#convert the PDF into smaller chunks
pages  = PyPDFLoader(args.pdf).load()
chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(pages)
embeddings = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"])

if os.path.exists("./faiss_index2"):
    db = FAISS.load_local("./faiss_index2", embeddings, allow_dangerous_deserialization=True)
    db.add_documents(chunks)
else:
    db = FAISS.from_documents(chunks, embeddings)

#place the chunks into the local database
db.save_local("./faiss_index2")
print(f"✓ Indexed {len(chunks)} chunks from {args.pdf}")

