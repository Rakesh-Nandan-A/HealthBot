import pandas as pd
import chromadb
import uuid
from langchain_community.document_loaders import WebBaseLoader

class HealthKnowledgeBase:
    def __init__(self, file_path="App/resource/health_articles.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="health_knowledge")

    def scrape_summary_from_url(self, url):
        try:
            loader = WebBaseLoader(url)
            doc = loader.load()[0].page_content
            return doc[:1500]  # Limit to 1500 characters
        except Exception as e:
            return f"Failed to load content from {url}: {e}"

    def load_knowledge(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                if "URL" in row:
                    summary = self.scrape_summary_from_url(row["URL"])
                    self.collection.add(
                        documents=summary,
                        metadatas={"url": row["URL"]},
                        ids=[str(uuid.uuid4())]
                    )

    def reset_knowledge(self):
        self.chroma_client.delete_collection(name="health_knowledge")
        self.collection = self.chroma_client.get_or_create_collection(name="health_knowledge")

    def query_articles(self, query_terms):
        results = self.collection.query(query_texts=query_terms, n_results=2)
        documents = results.get('documents', [])[0] if results.get('documents') else []
        metadatas = results.get('metadatas', [])[0] if results.get('metadatas') else []
        return list(zip(documents, metadatas))