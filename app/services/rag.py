from typing import List
from app.services.retriever import retrieve_chunks
from app.services.memory import save_message, get_history
from app.core.model_loader import get_llm_model, get_llm_tokenizer

# Get llm_model and tokernizer
llm_model = get_llm_model()
tokenizer = get_llm_tokenizer()

# llm helper for response generation
def llm_generate(prompt: str, max_new_tokens: int = 100) -> str:
    inputs = tokenizer(prompt, return_tensors= 'pt')
    output = llm_model.generate(**inputs, max_new_tokens = max_new_tokens)

    return tokenizer.decode(output[0], skip_special_tokens = True)


# Build context from chunks
def build_context(chunks: List[str]) -> str:
    return ("\n\n").join(chunks)
    

# format conversation history
def format_history(history: list) -> str:
    history_lines = []

    for msg in history:
        role = msg["role"].capitalize()
        content = msg["content"]
        history_lines.append(f"{role}: {content}")

    return "\n".join(history_lines)


# response pipeline
def generate_response(query: str, user_id: str):
    history = get_history(user_id)

    chunks = retrieve_chunks(query)
    context = build_context(chunks)
    history_text = format_history(history)
    
    #build prompt
    prompt = f"""
    Answer the question using only the provided context and conversation history.

    Give a short but complete answer in a full sentence.
    If the answer is not in the context, say exactly: I don't know
    
        Conversation History:
        {history_text}
        
        Context:
        {context}

        Question:
        {query}

        Answer:
    """

    response = llm_generate(prompt)

    # save memory
    save_message(user_id, "user", query)
    save_message(user_id, "assistant", response)

    return response




