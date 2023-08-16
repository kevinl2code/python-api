from typing import List, TypedDict
import pinecone
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader
from dotenv import dotenv_values
import uuid

config = dotenv_values(".env")
PINECONE_API_KEY = config["PINECONE_API_KEY"]
PINECONE_ENV = config["PINECONE_ENV"]
OPENAI_API_KEY = config["OPENAI_API_KEY"]

pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENV,
)

index = pinecone.Index("skuup")


class TypedPineconeMetaData(TypedDict):
    category: str
    start_date: int
    end_date: int
    latitude: float
    longitude: float
    paid: bool
    max_impressions: int


class PineconeMetaData:
    def __init__(self, category: str, start_date: int, end_date: int, latitude: float, longitude: float, paid: bool, max_impressions: int):
        self.category = category
        self.start_date = start_date
        self.end_date = end_date
        self.latitude = latitude
        self.longitude = longitude
        self.paid = paid
        self.max_impressions = max_impressions

    def to_dict(self) -> TypedPineconeMetaData:
        return {
            "category": self.category,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "paid": self.paid,
            "max_impressions": self.max_impressions
        }


current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "../sdk/cultural_event.txt")
loader = TextLoader(file_path)
documents = loader.load()


def add_extra_metadata(texts):
    for i, text in enumerate(texts):
        text.metadata['category'] = i
        text.metadata['start_date'] = 1692388800
        text.metadata['end_date'] = 1692603000
        text.metadata['latitude'] = 30.266666
        text.metadata['longitude'] = -97.733330
        text.metadata['paid'] = True
        text.metadata['max_impressions'] = 1000
    return texts


def add_new_vectors(documents: List):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600,
                                                   chunk_overlap=80)
    split_docs = text_splitter.split_documents(
        documents)

    ids = []
    text = []
    meta_data = []

    for doc in split_docs:
        ids.append(str(uuid.uuid4()))
        text.append(doc.page_content)
        meta_data.append({
            "category": 'culteral_event',
            "start_date": 1692388800,
            "end_date": 1692603000,
            "latitude": 30.266666,
            "longitude": -97.73333,
            "paid": True,
            "max_impressions": 1000
        })

    embeddings = OpenAIEmbeddings(
        openai_api_key=OPENAI_API_KEY
    )
    vectorstore = Pinecone(index, embeddings.embed_query, "text")
    vectorstore.add_texts(ids=ids, texts=text, metadatas=meta_data)


embeddings = OpenAIEmbeddings(
    openai_api_key=OPENAI_API_KEY
)
docsearch = Pinecone.from_existing_index("skuup", embeddings)


def test_pinecone():
    # add_new_vectors(documents)
    #     print('documents', len(documents))
    #     print('texts', len(texts))
    response = docsearch.similarity_search(
        query='Will the Austin Adventure Carnival have games?')
    print('response', response)
    # docsearch.delete(delete_all=True)
