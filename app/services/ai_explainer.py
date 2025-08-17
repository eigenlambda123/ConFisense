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

# PROMPT BUILDER
def build_prompt(scenario: str, input_data: dict, output_data: dict) -> str:
    """Build simulation explanation prompt based on scenario type."""
    def safe_section(section, limit_tokens=300):
        if isinstance(section, list):
            section = "\n".join(map(str, section))
        elif not isinstance(section, str):
            section = str(section or "")
        return safe_truncate_text(section, limit_tokens)

    input_str = safe_section(input_data, 300)

    summary_str = safe_section(
        safe_get(output_data, ["data", "summary"], safe_get(output_data, ["summary"], "")),
        300
    )
    math_str = safe_section(
        safe_get(output_data, ["data", "math_explanation", "sections"], safe_get(output_data, ["math_explanation", "sections"], "")),
        500
    )

    templates = {
        "budgeting": "Explain the following budgeting simulation in plain English so the user understands their result.",
        "emergency_fund": "Explain the following emergency fund simulation in simple, user-friendly language.",
        "debt": "Write a clear and encouraging explanation of the user's debt payoff plan.",
        "investing": "Explain the projected investment growth and how it can help the user plan better.",
        "education": "Explain how much the user needs to save for future education expenses.",
        "purchase": "Explain the savings plan for a major future purchase."
    }

    instructions = templates.get(scenario, "Please explain this financial simulation in simple terms.")
    
    return peso_wrap_prompt(f"""
You are a helpful financial assistant.

{instructions}

User Inputs:
{input_str}

Simulation Summary:
{summary_str}

Math Explanation:
{math_str}
    
Write a short, clear explanation:
""")

# AI FUNCTIONS
def generate_ai_explanation(scenario: str, input_data: dict, output_data: dict) -> str:
    prompt = build_prompt(scenario, input_data, output_data)

    prompt_tokens = count_tokens(prompt)
    available_for_output = MAX_CONTEXT_TOKENS - prompt_tokens
    if available_for_output <= 0:
        logger.warning("Prompt too long; truncating aggressively.")
        prompt = safe_truncate_text(prompt, MAX_CONTEXT_TOKENS // 2)
        prompt_tokens = count_tokens(prompt)
        available_for_output = MAX_CONTEXT_TOKENS - prompt_tokens

    max_output_tokens = min(MAX_OUTPUT_TOKENS, available_for_output)
    logger.info(f"[AI Explanation] Prompt tokens: {prompt_tokens}, Max output tokens: {max_output_tokens}")

    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=max_output_tokens,
        temperature=0.7
    )

    return response.generations[0].text.strip()

def generate_ai_suggestions(scenario: str, input_data: dict, output_data: dict) -> list:
    input_str = safe_truncate_text(str(input_data), 300)
    summary_str = safe_truncate_text(
        safe_get(output_data, ["data", "summary"], safe_get(output_data, ["summary"], "")),
        300
    )
    math_str = safe_truncate_text(
        safe_get(output_data, ["data", "math_explanation", "sections"], safe_get(output_data, ["math_explanation", "sections"], "")),
        300
    )

    prompt = peso_wrap_prompt(f"""
You are a helpful financial assistant.

Based on the following simulation, give 3 short, practical suggestions to improve the user's outcome.

User Inputs:
{input_str}

Simulation Summary:
{summary_str}

Math Explanation:
{math_str}

Suggestions (as a numbered list):
""")

    prompt_tokens = count_tokens(prompt)
    available_for_output = MAX_CONTEXT_TOKENS - prompt_tokens
    max_output_tokens = min(MAX_SUGGESTION_TOKENS, available_for_output)
    logger.info(f"[AI Suggestions] Prompt tokens: {prompt_tokens}, Max output tokens: {max_output_tokens}")

    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=max_output_tokens,
        temperature=0.7
    )

    return [
        line.strip()[3:].strip()
        for line in response.generations[0].text.strip().split("\n")
        if line.strip() and line.strip()[0].isdigit()
    ]

# DIRECT PESO CALL
def generate_peso_response(prompt: str) -> str:
    """Generic Cohere call ensuring pesos in output."""
    peso_prompt = peso_wrap_prompt(prompt)
    response = co.generate(
        model="command",
        prompt=peso_prompt,
        max_tokens=2000,
        temperature=0.7,
        stop_sequences=["\n\n"],
        truncate="NONE"
    )
    return response.generations[0].text.strip()
