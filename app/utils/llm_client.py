"""LLM client for document Q&A using Groq"""
from typing import Tuple
from groq import Groq
from app.config import settings


def chunk_text(text: str, chunk_size: int = 2000) -> list[str]:
    """
    Split text into chunks for context.
    
    Args:
        text: Text to chunk
        chunk_size: Maximum characters per chunk
        
    Returns:
        List of text chunks
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        word_length = len(word) + 1  # +1 for space
        if current_length + word_length > chunk_size and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = word_length
        else:
            current_chunk.append(word)
            current_length += word_length
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks


def find_relevant_chunks(question: str, chunks: list[str], max_chunks: int = 3) -> str:
    """
    Find most relevant chunks for the question.
    Simple keyword-based approach (can be enhanced with embeddings later).
    
    Args:
        question: User's question
        chunks: Text chunks
        max_chunks: Maximum chunks to return
        
    Returns:
        Combined relevant chunks
    """
    # Extract keywords from question
    keywords = set(question.lower().split())
    
    # Score chunks based on keyword overlap
    scored_chunks = []
    for chunk in chunks:
        chunk_lower = chunk.lower()
        score = sum(1 for keyword in keywords if keyword in chunk_lower)
        scored_chunks.append((score, chunk))
    
    # Sort by score and take top chunks
    scored_chunks.sort(reverse=True, key=lambda x: x[0])
    relevant_chunks = [chunk for _, chunk in scored_chunks[:max_chunks]]
    
    return "\n\n".join(relevant_chunks)


async def query_document(
    question: str,
    document_text: str,
    document_name: str
) -> Tuple[str, str]:
    """
    Query a document using Groq LLM.
    
    Args:
        question: User's question
        document_text: Full document text
        document_name: Name of the document
        
    Returns:
        Tuple of (answer, context_used)
    """
    # Check if API key is set
    if not settings.GROQ_API_KEY:
        return (
            "Groq API key not configured. Please set GROQ_API_KEY in your environment variables.",
            ""
        )
    
    try:
        # Initialize Groq client
        client = Groq(api_key=settings.GROQ_API_KEY)
        
        # Chunk document text
        chunks = chunk_text(document_text)
        
        # Find relevant chunks
        context = find_relevant_chunks(question, chunks, max_chunks=3)
        
        # Build prompt
        prompt = f"""You are a helpful financial analyst assistant. Answer the user's question based on the following document content.

Document: {document_name}

Context from document:
{context}

Question: {question}

Instructions:
- Answer based ONLY on the provided context
- If the context doesn't contain enough information, say so
- Be specific and cite relevant details from the document
- Keep your answer concise and focused

Answer:"""
        
        # Call Groq API
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful financial analyst assistant. Analyze documents and answer questions accurately."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1024
        )
        
        answer = response.choices[0].message.content.strip()
        
        return answer, context
        
    except Exception as e:
        error_msg = f"Error querying LLM: {str(e)}"
        return error_msg, ""

