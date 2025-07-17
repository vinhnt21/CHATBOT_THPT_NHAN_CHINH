# Third-party imports
from openai import OpenAI

# Local imports
from src.configs import openai_config, deepseek_config
from src.database import get_context_by_query, chat_session_collection, error_log_collection
from src.models import ChatSession, ErrorLog, Message
from src.prompts import SYSTEM_PROMPT,  PHAN_HOI_KHI_LOI

deepseek_llm = OpenAI(api_key=deepseek_config.API_KEY, base_url=deepseek_config.BASE_URL)
openai_llm = OpenAI(api_key=openai_config.API_KEY)

def generate_response(session_id: str, query: str, namespace: str) -> str:
    """
    Generate response using RAG and chat history
    
    Args:
        session_id: Unique session identifier
        query: User query
        namespace: Pinecone namespace for context search
        
    Returns:
        Generated response string
    """
    try:
        # Get relevant context from vector database
        context = get_context_by_query(query, namespace)
        
        # Get or create chat session
        chat_session = chat_session_collection.get_session(session_id)
        if chat_session is None:
            chat_session = chat_session_collection.create_session(session_id, namespace)
        
        # Add user message to chat history
        user_message = Message(role="user", content=query)
        chat_session.messages.append(user_message)
        if not context:
            chat_session.messages.append(Message(role="assistant", content=PHAN_HOI_KHI_LOI))
            chat_session_collection.update_session(chat_session)
            return PHAN_HOI_KHI_LOI
        
        # Prepare messages for LLM
        llm_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": f"Context: {context}"},
        ]
        
        # Add chat history (keep last 10 messages for context)
        for message in chat_session.messages[-10:]:
            llm_messages.append({
                "role": message.role, 
                "content": message.content
            })
        
        # Generate response
        # response = deepseek_llm.chat.completions.create(
        #     model=deepseek_config.MODEL,
        #     messages=llm_messages,
        #     temperature=deepseek_config.TEMPERATURE
        # )
        response = openai_llm.chat.completions.create(
            model=openai_config.LLM_MODEL,
            messages=llm_messages,
            temperature=openai_config.TEMPERATURE
        )
        
        answer = response.choices[0].message.content
        
        # Add assistant response to chat history
        assistant_message = Message(role="assistant", content=answer)
        chat_session.messages.append(assistant_message)
        
        # Update session in database
        chat_session_collection.update_session(chat_session)
        
        return answer
        
    except Exception as e:
        error_msg = f"Error generating response: {str(e)}"
        print(error_msg)
        # Return fallback response
        return PHAN_HOI_KHI_LOI



