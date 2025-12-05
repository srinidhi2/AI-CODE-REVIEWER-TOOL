import os
from dotenv import load_dotenv
from groq import Groq

# Load keys from .env
load_dotenv()

# Create Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def review_code(diff: str) -> str:
    """
    Send a pull request diff to Groq and get back AI review feedback.
    """
    prompt = f"""
    You are an expert senior code reviewer.

    Given the following GitHub Pull Request diff, provide a clear review with:
    - Code quality issues
    - Possible bugs or edge cases
    - Any security concerns
    - Suggestions to improve readability and structure
    - Suggestions for tests that should be added

    Be concise but specific. Use bullet points.

    Pull Request diff:
    {diff}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",  # stable Groq model
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
    )

    # Newer Groq SDK returns message as an object with .content
    return response.choices[0].message.content
