from dotenv import load_dotenv
import os
import cohere
import tiktoken
import logging


# Config
load_dotenv()
key = os.getenv("COHERE_API_KEY")

if not key:
    raise RuntimeError("COHERE_API_KEY is missing in .env")

co = cohere.Client(key)

# Cohere "command" models often have a 4096 or 8192 token limit.
# Adjust this if you are using a larger-context model.
MAX_CONTEXT_TOKENS = 4096  

# Use OpenAI's cl100k_base tokenizer (approximate for Cohere)
tokenizer = tiktoken.get_encoding("cl100k_base")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Utility Functions
def count_tokens(text: str) -> int:
    """Count tokens in a string using tiktoken."""
    return len(tokenizer.encode(text))

def safe_truncate_text(text: str, max_tokens: int) -> str:
    """Truncate text to fit within max_tokens."""
    tokens = tokenizer.encode(text)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
    return tokenizer.decode(tokens)

def build_prompt(scenario: str, input_data: dict, output_data: dict) -> str:
    """Builds the prompt string depending on scenario, truncating if needed."""
    
    def safe_section(section, limit_tokens=300):
        """Convert to string and truncate safely."""
        if isinstance(section, list):
            section = "\n".join(map(str, section))
        elif not isinstance(section, str):
            section = str(section or "")
        return safe_truncate_text(section, limit_tokens)

    input_str = safe_section(input_data, 300)

    # Extract summary & math explanation robustly
    if "data" in output_data:  # emergency_fund case
        summary_str = safe_section(output_data["data"].get("summary", ""), 300)
        math_str = safe_section(
            output_data["data"].get("math_explanation", {}).get("sections", ""),
            500
        )
    else:
        summary_str = safe_section(output_data.get("summary", ""), 300)
        math_str = safe_section(
            output_data.get("math_explanation", {}).get("sections", ""),
            500
        )

    # Scenario-specific templates
    prompts = {
        "budgeting": f"""
You are a helpful financial assistant.

Explain the following **budgeting simulation** in plain English so the user understands what their result means.

User Inputs:
{input_str}

Simulation Summary:
{summary_str}

Math Explanation:
{math_str}

Write a short, clear explanation:
""",
        "emergency_fund": f"""
You are a helpful financial assistant.

Explain the following **emergency fund simulation** in simple, user-friendly language.

User Inputs:
{input_str}

Simulation Summary:
{summary_str}

Math Explanation:
{math_str}

Give a brief explanation of the results:
""",
        "debt": f"""
You are a helpful financial assistant.

This simulation estimates the user's debt payoff plan.

Inputs:
{input_str}

Summary of Simulation:
{summary_str}

Math Explanation:
{math_str}

Write a clear and encouraging explanation of the results:
""",
        "investing": f"""
You are a helpful financial assistant.

This simulation projects potential investment growth over time.

User Inputs:
{input_str}

Simulation Summary:
{summary_str}

Math Explanation:
{math_str}

Explain what the projection means and how it can help the user plan better:
""",
        "education": f"""
You are a helpful financial assistant.

This simulation calculates how much a user needs to save for future education expenses.

User Inputs:
{input_str}

Simulation Summary:
{summary_str}

Math Explanation:
{math_str}

Give a short and supportive explanation of the result:
""",
        "purchase": f"""
You are a helpful financial assistant.

This simulation helps the user plan for a major future purchase.

User Inputs:
{input_str}

Simulation Summary:
{summary_str}

Math Explanation:
{math_str}

Explain the savings plan and how achievable the target is:
"""
    }

    return prompts.get(scenario, f"""
You are a financial assistant. Here is a simulation result.

Inputs:
{input_str}

Summary:
{summary_str}

Math:
{math_str}

Please explain this result in simple terms:
""")



# AI Functions
def generate_ai_explanation(scenario: str, input_data: dict, output_data: dict) -> str:
    """Generate a friendly, simple AI explanation based on the scenario type."""
    
    prompt = build_prompt(scenario, input_data, output_data)

    # Count prompt tokens
    prompt_tokens = count_tokens(prompt)

    # Adjust max_tokens to fit within context
    available_for_output = MAX_CONTEXT_TOKENS - prompt_tokens
    if available_for_output <= 0:
        logger.warning("Prompt is too long; truncating further to fit context limit.")
        prompt = safe_truncate_text(prompt, MAX_CONTEXT_TOKENS // 2)  # aggressive cut
        prompt_tokens = count_tokens(prompt)
        available_for_output = MAX_CONTEXT_TOKENS - prompt_tokens

    max_output_tokens = min(1000, available_for_output)

    logger.info(f"Prompt tokens: {prompt_tokens}, Output max tokens: {max_output_tokens}")

    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=max_output_tokens,
        temperature=0.7
    )

    return response.generations[0].text.strip()

def generate_ai_suggestions(scenario: str, input_data: dict, output_data: dict) -> list:
    """Generate a list of AI-powered suggestions based on the scenario and simulation results."""

    # Reuse build_prompt but shorten instructions
    input_str = safe_truncate_text(str(input_data), 300)
    if "data" in output_data:
        summary_str = safe_truncate_text(output_data["data"].get("summary", ""), 300)
        math_str = safe_truncate_text(output_data["data"]["math_explanation"]["sections"], 300)
    else:
        summary_str = safe_truncate_text(output_data.get("summary", ""), 300)
        math_str = safe_truncate_text(output_data.get("math_explanation", {}).get("sections", ""), 300)

    prompt = f"""
You are a helpful financial assistant.

Based on the following simulation, give 3 short, practical suggestions to improve the user's outcome.

User Inputs:
{input_str}

Simulation Summary:
{summary_str}

Math Explanation:
{math_str}

Suggestions (as a numbered list):
"""

    prompt_tokens = count_tokens(prompt)
    available_for_output = MAX_CONTEXT_TOKENS - prompt_tokens
    max_output_tokens = min(120, available_for_output)

    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=max_output_tokens,
        temperature=0.7
    )

    # Parse into numbered list
    suggestions = [
        line.strip()[3:].strip()
        for line in response.generations[0].text.strip().split("\n")
        if line.strip() and line.strip()[0].isdigit()
    ]
    return suggestions
