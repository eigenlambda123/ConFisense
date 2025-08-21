from dotenv import load_dotenv
import os
import cohere
import tiktoken
import logging

# CONFIG
load_dotenv()
key = os.getenv("COHERE_API_KEY")
if not key:
    raise RuntimeError("COHERE_API_KEY is missing in .env")

co = cohere.Client(key)

MAX_CONTEXT_TOKENS = 4096  # Adjust per model
MAX_OUTPUT_TOKENS = 1000   # Upper bound for explanation
MAX_SUGGESTION_TOKENS = 120

tokenizer = tiktoken.get_encoding("cl100k_base")  # Approx for Cohere

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# UTILITIES
def count_tokens(text: str) -> int:
    """Count tokens in a string using tiktoken."""
    return len(tokenizer.encode(text or ""))

def safe_truncate_text(text: str, max_tokens: int) -> str:
    """Truncate text to fit within max_tokens."""
    tokens = tokenizer.encode(text or "")
    return tokenizer.decode(tokens[:max_tokens])

def safe_get(obj, keys, default=""):
    """Safely get nested keys from dict."""
    for k in keys:
        if isinstance(obj, dict):
            obj = obj.get(k, default)
        else:
            return default
    return obj or default

def peso_wrap_prompt(prompt: str) -> str:
    """Ensure Philippine peso clarification is added."""
    return (
        f"{prompt}\n\n"
        "IMPORTANT: All monetary amounts must be expressed in Philippine pesos (₱), "
        "not in US dollars or any other currency."
    )

# AI response Settings
def generate_response(prompt: str) -> str:
    peso_prompt = peso_wrap_prompt(prompt)
    prompt_tokens = count_tokens(peso_prompt)
    available = MAX_CONTEXT_TOKENS - prompt_tokens
    max_output_tokens = min(1200, available)  # be conservative

    response = co.generate(
        model="command",
        prompt=peso_prompt,
        max_tokens=max_output_tokens,
        temperature=0.7,
        truncate="END"
    )
    return response.generations[0].text.strip()
