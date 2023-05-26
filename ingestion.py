import os

from langchain.document_loaders import GitLoader
from git import Repo
from langchain.embeddings import OpenAIEmbeddings, VertexAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
import pinecone

pinecone.init(
    api_key=os.environ["G_PINECONE_API_KEY"],
    environment=os.environ["G_PINECONE_ENVIRONMENT_REGION"],
)


def ingest_docs():
    to_path = "./wordblend-ai"
    repo = Repo.clone_from(
        "https://github.com/g-emarco/wordblend-ai", to_path=to_path, branch="main"
    )
    loader = GitLoader(repo_path=to_path)
    raw_documents = loader.load()

    print(f"loaded {len(raw_documents)} documents")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=150,
    )

    for doc in raw_documents:
        source = doc.metadata["source"]
        cleaned_source = "/".join(source.split("/")[1:])
        doc.page_content = (
            "FILE NAME: "
            + cleaned_source
            + "\n###\n"
            + doc.page_content.replace("\u0000", "")
        )

    documents = text_splitter.split_documents(raw_documents)

    embeddings = OpenAIEmbeddings()
    print(f"Going to add {len(documents)} to Pinecone")
    Pinecone.from_documents(
        documents, embeddings, index_name=os.environ["PINECONE_INDEX_NAME"]
    )
    print("****Loading to vectorestore done ***")


def ingest_docs_g():
    to_path = "./wordblend-ai"
    repo = Repo.clone_from(
        "https://github.com/g-emarco/wordblend-ai", to_path=to_path, branch="main"
    )
    loader = GitLoader(repo_path=to_path)
    raw_documents = loader.load()

    print(f"loaded {len(raw_documents)} documents")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=150,
    )

    for doc in raw_documents:
        source = doc.metadata["source"]
        cleaned_source = "/".join(source.split("/")[1:])
        doc.page_content = (
            "FILE NAME: "
            + cleaned_source
            + "\n###\n"
            + doc.page_content.replace("\u0000", "")
        )

    documents = text_splitter.split_documents(raw_documents)
    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"
    ] = "/Users/emarco/GithubProjects/github-assistant/vertex-sa-key.json"

    embeddings = VertexAIEmbeddings()  # Dimention 768
    print(f"Going to add {len(documents)} to Pinecone")
    chunk_size = 5
    for i in range(0, len(documents), chunk_size):
        chunked_documents = documents[i : i + chunk_size]
        Pinecone.from_documents(
            chunked_documents, embeddings, index_name=os.environ["PINECONE_INDEX_NAME"]
        )
    print("****Loading to vectorestore done ***")


if __name__ == "__main__":
    ingest_docs()
