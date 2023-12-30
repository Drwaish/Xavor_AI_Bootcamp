import os
import pandas as pd
from tqdm import tqdm
from uuid import uuid4
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from  dotenv import load_dotenv
import pinecone

load_dotenv()
os.environ.get("OPENAI_API_KEY") # outputs test

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
YOUR_ENV = 'gcp-starter'
INDEX_NAME = 'temp'
# Initialize Pinecone client
pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=YOUR_ENV
)
demo_index = pinecone.Index('temp')

BATCH_SIZE = 4
MODEL_NAME = 'text-embedding-ada-002'
EMBED = OpenAIEmbeddings(
    model=MODEL_NAME,
)
def chunk_by_size(text: str, size: int = 1500):
    """
    Chunk up text recursively.

    param text: Text to be chunked up
    return: List of Document items (i.e. chunks).|
    """
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = size,
    chunk_overlap = 0,
    add_start_index = True,
)
    return text_splitter.create_documents([text])

def pad_text(text):
    padded_text = text.ljust(1500, 'X')
    return padded_text

def csv_to_list(file_path):
  df_path = pd.read_csv(file_path)
  data_list = []
  for i in range(len(df_path)):
    data = f"History: \n {df_path['History'][i]}\n Primary_Daignose: \n  {df_path['Body_Vitals'][i]}\n Description \n {df_path['Description'][i]}"
    if len(data)<1500:
        data = pad_text(data)
    data_list.append(data)
  return data_list



def create_chunks_metadata_embeddings(dataset) -> list[dict]:
    """
    Given a dataset, split text data into chunks, extract metadata, create embeddings for each chunk.

    :param dataset: Data we want to process.
    :return: List of data objects to upsert into our Pinecone index.
    """
    data_objs = []

    # For each row in our dataset:
    for data in tqdm(dataset):  # (tqdm library prints status of for-loop to console)
        # Create chunks
        chunked_text = chunk_by_size(data)

        # Extract just the string content from the chunk
        chunked_text = [c.page_content for c in chunked_text]

        # Extract some metadata, create an ID, and generate an embedding for the chunk.
        # Wrap that all in a dictionary, and append that dictionary to a list (`data_objs`).
        for idx, text in enumerate(chunked_text):
            payload = {
                "metadata": {
                    "diseases": 'dengue-fever',
                    "text_content": text  # there are 248 chars in this chunk of text
                },
             "id": str(uuid4()),
            "values": EMBED.embed_documents([text])[0] # --> list of len 248, each item of those 248 has a len of 1536
            }
            

            data_objs.append(payload)

    # Return list of dictionaries, each containing our metadata, ID, and embedding, per chunk.
    return data_objs

def batch_upsert(data: list[dict], index, namespace: str):
    """
    Upsert data objects to a Pinecone index in batches.

    :param data: Data objects we want to upsert.
    :param index: Index into which we want to upsert our data objects.
    :namespace: Namespace within our index into which we want to upsert our data objects.
    """
    for i in range(0, len(data), BATCH_SIZE):
        batch = data[i:i+BATCH_SIZE]
        # print(batch)
        index.upsert(vectors=batch, namespace=namespace)

def main(file_path : list[str], name_space : list[str]):
    """
    Function to execute complete business.

    Parameters
    ----------
    file_path
        List of all files insert in pinecone vector database.

    Return
    ------
    None

    """
    for i,file in enumerate(file_path):
        chunks = csv_to_list(file)
        data = create_chunks_metadata_embeddings(chunks)
        batch_upsert(data, index= demo_index, namespace= name_space[i])

if __name__ == "__main__":
    file_names = [ 'dengue_df.csv']
    name_spaces = ['dengue']
    main(file_names, name_spaces)
