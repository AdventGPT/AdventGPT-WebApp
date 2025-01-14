import weaviate
import os
from vectordb.weaviate_client import WeaviateWCS, WeaviateIndexer

# Pretty printer
from rich import print

# # DotENV
# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv(), override=True)

COLLECTION_NAME = "egw_books"

def create_client():
    api_key = os.getenv('WEAVIATE_API_KEY')
    endpoint = os.getenv('WEAVIATE_ENDPOINT')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    client = WeaviateWCS(endpoint=endpoint, api_key=api_key, 
                        openai_api_key=openai_api_key,
                        model_name="text-embedding-3-large",
                        dimensions=1024*3,
                        return_properties =['content', 'doc_id', "book", "chapter_title", "chapter_number", "sentence_number"])
    return client

def vector_search(client,request):
    return client.vector_search(request=request,
                      collection_name = "egw_books",
                      limit = 50)

