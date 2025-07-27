from dotenv import load_dotenv
import os
import cohere

load_dotenv()

key = os.getenv("COHERE_API_KEY")
print("Key loaded:", key)  # Should not be None

co = cohere.Client(key)
response = co.generate(prompt="Explain the 50/30/20 rule for budgeting.", model="command")
print(response.generations[0].text)
