from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from app.core.config import EMBEDDING_MODEL_NAME, LLM_MODEL_NAME

_embedding_model = None
_tokenizer = None
_llm_model = None


def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _embedding_model


def get_llm_tokenizer():
    global _tokenizer
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME)
    return _tokenizer


def get_llm_model():
    global _llm_model
    if _llm_model is None:
        _llm_model = AutoModelForSeq2SeqLM.from_pretrained(LLM_MODEL_NAME)
    return _llm_model