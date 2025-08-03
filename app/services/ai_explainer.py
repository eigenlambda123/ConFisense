from dotenv import load_dotenv
import os
import cohere

load_dotenv()
key = os.getenv("COHERE_API_KEY")

if not key:
    raise RuntimeError("COHERE_API_KEY is missing in .env")

co = cohere.Client(key)


def generate_ai_explanation(scenario: str, input_data: dict, output_data: dict) -> str:
    """
    Generate a friendly, simple AI explanation based on the scenario type.
    """
    if scenario == "budgeting":
        prompt = f"""
You are a helpful financial assistant.

Explain the following **budgeting simulation** in plain English so the user understands what their result means.

User Inputs:
{input_data}

Simulation Summary:
{output_data['summary']}

Math Explanation:
{output_data['math_explanation']['sections']}

Write a short, clear explanation:
"""

    elif scenario == "emergency_fund":
        prompt = f"""
You are a helpful financial assistant.

Explain the following **emergency fund simulation** in simple, user-friendly language.

User Inputs:
{input_data}

Simulation Summary:
{output_data['data']['summary']}

Math Explanation:
{output_data['data']['math_explanation']['sections']}

Give a brief explanation of the results:
"""

    elif scenario == "debt":
        prompt = f"""
You are a helpful financial assistant.

This simulation estimates the user's debt payoff plan.

Inputs:
{input_data}

Summary of Simulation:
{output_data['summary']}

Math Explanation:
{output_data['math_explanation']['sections']}

Write a clear and encouraging explanation of the results:
"""

    elif scenario == "investing":
        prompt = f"""
You are a helpful financial assistant.

This simulation projects potential investment growth over time.

User Inputs:
{input_data}

Simulation Summary:
{output_data['summary']}

Math Explanation:
{output_data['math_explanation']['sections']}

Explain what the projection means and how it can help the user plan better:
"""

    elif scenario == "education":
        prompt = f"""
You are a helpful financial assistant.

This simulation calculates how much a user needs to save for future education expenses.

User Inputs:
{input_data}

Simulation Summary:
{output_data['summary']}

Math Explanation:
{output_data['math_explanation']['sections']}

Give a short and supportive explanation of the result:
"""

    elif scenario == "purchase":
        prompt = f"""
You are a helpful financial assistant.

This simulation helps the user plan for a major future purchase.

User Inputs:
{input_data}

Simulation Summary:
{output_data['summary']}

Math Explanation:
{output_data['math_explanation']['sections']}

Explain the savings plan and how achievable the target is:
"""

    else:
        prompt = f"""
You are a financial assistant. Here is a simulation result.

Inputs:
{input_data}

Summary:
{output_data['summary']}

Math:
{output_data['math_explanation']['sections']}

Please explain this result in simple terms:
"""

    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=300,
        temperature=0.7
    )

    return response.generations[0].text.strip()



def generate_ai_suggestions(scenario: str, input_data: dict, output_data: dict) -> list:
    """
    Generate a list of AI-powered suggestions based on the scenario and simulation results.
    """
    if scenario == "emergency_fund":
        prompt = f"""
You are a helpful financial assistant.

Based on the following emergency fund simulation, give 3 short, practical suggestions to help the user reach their goal faster or improve their financial safety net.

User Inputs:
{input_data}

Simulation Summary:
{output_data['summary'] if 'summary' in output_data else output_data['data']['summary']}

Math Explanation:
{output_data['math_explanation']['sections'] if 'math_explanation' in output_data else output_data['data']['math_explanation']['sections']}

Suggestions (as a numbered list):
"""
    else:
        prompt = f"""
You are a helpful financial assistant.

Based on this simulation, give 3 practical suggestions to help the user improve their financial outcome.

User Inputs:
{input_data}

Simulation Summary:
{output_data.get('summary', '')}

Suggestions (as a numbered list):
"""

    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=120,
        temperature=0.7
    )

    # Parse the response into a list (assuming Cohere returns a numbered list)
    suggestions = [
        line.strip()[3:].strip()  # Remove '1. ', '2. ', etc.
        for line in response.generations[0].text.strip().split('\n')
        if line.strip() and line.strip()[0].isdigit()
    ]
    return suggestions