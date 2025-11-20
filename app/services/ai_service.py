import os
from groq import Groq
from dotenv import load_dotenv

# Load keys from .env file
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def review_code(diff: str) -> str:
    """
    This function sends the PR diff to Groq's LLM
    and returns AI-generated code review feedback.
    """
    prompt = f"""
    You are an expert code reviewer.
    Analyze the following GitHub Pull Request diff and provide:
    - Code quality issues
    - Potential bugs
    - Security concerns
    - Better coding practices
    - Missing test cases

    Code diff:
    {diff}
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message["content"]
