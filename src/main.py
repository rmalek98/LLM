import os
from langchain_chroma import Chroma
from langchain_community import embeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

# Initialize the model
model_local = ChatOllama(model="mistral", use_cloud=False)

# Set up the embedding and vector store
# this is the directory where the vector store will be saved need to be changed to your own directory using mine here
persist_directory = '/Users/malek/Documents/AI_Projects/LLM_RAG/db'
embedding = embeddings.OllamaEmbeddings(model='nomic-embed-text')
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

# Define the RAG prompt template
after_rag_template = """Answer the question based only on the following context:
{context}
Question: {question}
"""
after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)

# Create a retriever from the vector store
retriever = vectordb.as_retriever()

# Define the RAG chain using the local model
after_rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | after_rag_prompt 
    | model_local
    | StrOutputParser()
)

def main():
    # Path to the directory containing the documents 
    docs_path = '/Users/malek/Documents/AI_Projects/LLM_RAG/docs/'

    # Check if the directory exists
    if not os.path.exists(docs_path):
        print(f"Directory not found: {docs_path}")
        return

    # Example invocation to test
    print("\n#######\n After RAG\n")
    response = after_rag_chain.invoke("Write a python script that says hello world")
    print(response)

    # Load documents
    loader = DirectoryLoader(docs_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    # Rebuild vector store from documents
    vectordb = Chroma.from_documents(documents=texts, embedding=embedding, persist_directory=persist_directory)
    
    # Reset vectordb to confirm persistence works
    vectordb = None
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

if __name__ == "__main__":
    main()
