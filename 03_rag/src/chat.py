from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

#take user input
user_query = input("Ask something")

# relevant chunks from the vector db
search_results = vector_db.similarity_search(query=user_query)

context = "\n".join([f"Page content: {result.page_content} \n Page Number: {result.metadata['page_label']} \n File Location : {result.metadata['source']}" for result in search_results])

SYSTEM_PROMPT = f"""
You are an helpful AI assitant that answers to the query based on the available data that is fed to you. You strictly answer from the data provided/fed into to. You reply from the pdf file along with page_contents and page number.

context : {context}
"""

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role":"system", "content": SYSTEM_PROMPT},{
        "role" : "user",
        "content": user_query 
    }]
)

print(response.choices[0].message.content)
