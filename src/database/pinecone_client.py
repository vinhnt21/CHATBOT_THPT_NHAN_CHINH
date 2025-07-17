# Standard library imports
import uuid
from typing import List, Dict, Any
import json

# Third-party imports
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI

# Local imports
from src.configs import pinecone_config, openai_config
from src.utils import log
from src.models import Document

# Initialize clients
pc = Pinecone(api_key=pinecone_config.API_KEY)
openai_client = OpenAI(
    api_key=openai_config.API_KEY,
    base_url=openai_config.BASE_URL
)

# Create index if not exists (without auto-embedding)
if not pc.has_index(pinecone_config.INDEX_NAME):
    pc.create_index(
        name=pinecone_config.INDEX_NAME,
        dimension=pinecone_config.DIMENSION,  # 1536 for text-embedding-3-small, 3072 for text-embedding-3-large
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1",
        )
    )

    log.success(f"Pinecone index {pinecone_config.INDEX_NAME} created successfully")

index = pc.Index(pinecone_config.INDEX_NAME)
log.success(f"Pinecone index {pinecone_config.INDEX_NAME} loaded successfully")


def embed_text(text: str) -> List[float]:
    """
    Embed text using OpenAI embedding model
    Current config uses OpenAI models:
    - 'text-embedding-3-small' (dimension 1536) - Default
    - 'text-embedding-ada-002' (dimension 1536) - Alternative
    - 'text-embedding-3-large' (dimension 3072) - High quality
    """
    try:
        response = openai_client.embeddings.create(
            input=text,
            model=openai_config.EMBEDDING_MODEL  # Consider changing to 'text-embedding-3-small'
        )
        embedding = response.data[0].embedding
        return embedding
    except Exception as e:
        log.error(f"Error creating embedding: {str(e)}")
        raise e


def upsert_chunk_texts(chunk_texts: List[str], namespace: str, metadata: Document):
    """
    Embed chunk texts and upsert to Pinecone index
    """
    def _get_id(index: int):
        return f'{metadata.document_id}-{index}-{uuid.uuid4()}'
    
    vectors = []
    for idx, chunk_text in enumerate(chunk_texts):
        try:
            # Embed the chunk text
            embedding = embed_text(chunk_text)
            
            vectors.append({
                "id": _get_id(idx),
                "values": embedding,
                "metadata": {
                    "chunk_text": chunk_text,
                    "document_id": metadata.document_id,
                    "document_name": metadata.name,
                    "chunk_index": idx
                }
            })
        except Exception as e:
            log.error(f"Error processing chunk {idx}: {str(e)}")
            continue
    
    if vectors:
        index.upsert(vectors=vectors, namespace=namespace, batch_size=100)
        log.success(f"Upserted {len(vectors)} chunk texts to Pinecone index {pinecone_config.INDEX_NAME} successfully")
    else:
        log.warning("No vectors to upsert")


def get_chunk_texts_by_document_id(document_id: str, namespace: str) -> List[Dict[str, Any]]:
    """
    Get all chunk texts for a specific document
    """
    try:
        # Use query with filter instead of search
        response = index.query(
            namespace=namespace,
            filter={
                "document_id": {"$eq": document_id}
            },
            top_k=10000,  # Large number to get all chunks
            include_metadata=True
        )
        with open("response.json", "w", encoding="utf-8") as f:
            json.dump(response, f, ensure_ascii=False, indent=4)

        return response.matches
    except Exception as e:
        log.error(f"Error getting chunks by document_id: {str(e)}")
        return []


def get_context_by_query(query: str, namespace: str, top_k: int = None) -> str:
    """
    Get relevant context by embedding the query and searching similar vectors
    """
   
    
    try:
        # Embed the query
        query_embedding = embed_text(query)
        
        # Search for similar vectors
        response = index.query(
            namespace=namespace,
            vector=query_embedding,
            top_k=10,
            include_metadata=True
        )
        
        # Extract context from matches
        contexts = []
        for match in response.matches:
            if match.score > 0.2:  # Only include high similarity matches
                chunk_text = match.metadata.get('chunk_text', '')
                if chunk_text:
                    contexts.append(chunk_text)
        log.success(f"Retrieved {len(contexts)} relevant chunks for query")
        context = "\n\n".join(contexts)
        return context
        
    except Exception as e:
        log.error(f"Error getting context by query: {str(e)}")
        return ""


def delete_document_chunks(document_id: str, namespace: str) -> bool:
    """
    Delete all chunks for a specific document
    """
    try:
        # Get all chunk IDs for the document
        matches = get_chunk_texts_by_document_id(document_id, namespace)
        chunk_ids = [match.id for match in matches]
        
        if chunk_ids:
            index.delete(ids=chunk_ids, namespace=namespace)
            log.success(f"Deleted {len(chunk_ids)} chunks for document {document_id}")
            return True
        else:
            log.info(f"No chunks found for document {document_id}")
            return True
            
    except Exception as e:
        log.error(f"Error deleting document chunks: {str(e)}")
        return False


__all__ = [
    "embed_text",
    "upsert_chunk_texts", 
    "get_chunk_texts_by_document_id", 
    "get_context_by_query",
    "delete_document_chunks"
]
