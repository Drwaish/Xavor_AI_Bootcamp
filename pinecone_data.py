''' Driver file to run the code'''
import os
from langchain.llms import OpenAI

from dotenv import load_dotenv
import pandas as pd
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
load_dotenv()
os.environ.get("OPENAI_API_KEY") # outputs test
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

# os.environ['OPENAI_API_KEY'] =  os.getenv('OPENAI_API_KEY')
client = OpenAI()
# PINECONE_API_KEY = os.getenv("PINECONE_API") #read pinecone api
# Find ENV (cloud region) next to API key in console
YOUR_ENV = 'gcp-starter'
INDEX_NAME = 'temp'
# Initialize Pinecone client
pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=YOUR_ENV
)
demo_index = pinecone.Index('temp')
model_name = 'text-embedding-ada-002'
embed = OpenAIEmbeddings(
    model=model_name,
)
def get_context(query,name_space, embed = embed, demo_index = demo_index ):
    vec_query = embed.embed_documents([query])[0]
    description = demo_index.query(vector=vec_query,
                                 top_k=3, include_metadata=True,
                                 namespace=name_space)

    return (description['matches'][0]['metadata']['text_content'],
          description['matches'][1]['metadata']['text_content'],
          description['matches'][2]['metadata']['text_content'])
#Initialize API Key
# # Create index
# pinecone.create_index(
#     name=INDEX_NAME,
#     metric='cosine',
#     dimension=1536)

