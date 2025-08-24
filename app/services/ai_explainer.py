import os
import google.generativeai as genai
import logging
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini with the key
genai.configure(api_key=api_key)

# Instantiate the model once
model = genai.GenerativeModel('gemini-1.5-flash')

MAX_CONTEXT_TOKENS = 4096 
MAX_OUTPUT_TOKENS = 1000
MAX_SUGGESTION_TOKENS = 120

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# UTILITIES
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
    
    try:
        # Use the pre-instantiated model's token counter
        prompt_tokens = model.count_tokens(peso_prompt).total_tokens
        
        available = MAX_CONTEXT_TOKENS - prompt_tokens
        # Gemini uses max_output_tokens for max_tokens
        max_output_tokens = min(1200, available)
        
        # Check if there is enough context space for a response
        if max_output_tokens <= 0:
            logger.warning("Not enough token capacity for a response.")
            return "Unable to generate a response due to prompt size."
            
        response = model.generate_content(
            contents=peso_prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                max_output_tokens=max_output_tokens,
            )
        )
        # The generated text is in the 'text' attribute of the response
        return response.text.strip()
    
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return "An error occurred while generating the AI explanation."