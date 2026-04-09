from typing import List
from services.retriever import retrieve_chunks
from services.memory import save_message, get_history
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

llm_model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

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




