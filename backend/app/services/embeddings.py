import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import os
from typing import List, Dict, Optional
from PIL import Image
import numpy as np
from PyPDF2 import PdfReader

class EmbeddingsService:
    """Service for managing embeddings and vector search"""

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chroma_client = chromadb.Client(Settings(
            persist_directory="./chroma_db",
            anonymized_telemetry=False
        ))
        self.collection = None
        self.case_dir = "../Kyron_Horman"

    async def initialize(self):
        """Initialize or load the vector database"""
        try:
            self.collection = self.chroma_client.get_collection("cold_case_documents")
            print("Loaded existing collection")
        except:
            self.collection = self.chroma_client.create_collection(
                name="cold_case_documents",
                metadata={"description": "Cold case documents and evidence"}
            )
            print("Created new collection")
            await self.index_all_documents()

    async def index_all_documents(self):
        """Index all documents from the case directory"""
        print("Indexing all documents...")
        documents = []
        metadatas = []
        ids = []

        # Index text files
        text_dirs = {
            "podcast_topics": os.path.join(self.case_dir, "podcast_topics"),
            "scraped_sources": os.path.join(self.case_dir, "scraped_sources"),
            "texts": os.path.join(self.case_dir, "texts")
        }

        doc_id = 0
        for content_type, dir_path in text_dirs.items():
            if os.path.exists(dir_path):
                for filename in os.listdir(dir_path):
                    if filename.endswith('.txt'):
                        file_path = os.path.join(dir_path, filename)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read().strip()
                                if content:
                                    documents.append(content)
                                    metadatas.append({
                                        "filename": filename,
                                        "content_type": content_type,
                                        "file_type": "text",
                                        "path": file_path
                                    })
                                    ids.append(f"doc_{doc_id}")
                                    doc_id += 1
                        except Exception as e:
                            print(f"Error reading {filename}: {e}")

        # Index PDF files
        pdf_dir = os.path.join(self.case_dir, "official_documents")
        if os.path.exists(pdf_dir):
            for filename in os.listdir(pdf_dir):
                if filename.lower().endswith('.pdf'):
                    file_path = os.path.join(pdf_dir, filename)
                    try:
                        reader = PdfReader(file_path)
                        all_text = ""
                        for page in reader.pages:
                            text = page.extract_text()
                            if text:
                                all_text += text.strip() + " "

                        if all_text.strip():
                            documents.append(all_text.strip())
                            metadatas.append({
                                "filename": filename,
                                "content_type": "official_document",
                                "file_type": "pdf",
                                "path": file_path
                            })
                            ids.append(f"doc_{doc_id}")
                            doc_id += 1
                    except Exception as e:
                        print(f"Error reading PDF {filename}: {e}")

        # Add documents to collection
        if documents:
            # Generate embeddings
            embeddings = self.model.encode(documents).tolist()

            # Add to ChromaDB
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            print(f"Indexed {len(documents)} documents")
        else:
            print("No documents to index")

    async def search(
        self,
        query: str,
        n_results: int = 5,
        content_types: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Search for relevant documents

        Args:
            query: Search query
            n_results: Number of results to return
            content_types: Filter by content types

        Returns:
            List of relevant documents with metadata
        """
        # Generate query embedding
        query_embedding = self.model.encode([query]).tolist()

        # Build filter
        where = None
        if content_types:
            where = {"content_type": {"$in": content_types}}

        # Search
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            where=where
        )

        # Format results
        formatted_results = []
        if results and results['documents']:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if results.get('distances') else None
                })

        return formatted_results

    async def get_all_documents(self) -> List[Dict]:
        """Get all indexed documents"""
        results = self.collection.get()

        formatted_results = []
        if results and results['documents']:
            for i in range(len(results['documents'])):
                formatted_results.append({
                    "id": results['ids'][i],
                    "content": results['documents'][i],
                    "metadata": results['metadatas'][i]
                })

        return formatted_results
