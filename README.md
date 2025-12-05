**AI-Powered GitHub Pull Request Reviewer** - Automatically reviews PRs using LLMs and comments directly inside GitHub.
## Example:
<img width="653" height="466" alt="image" src="https://github.com/user-attachments/assets/9db0b2c8-3d1b-45a1-b9ba-3a52d250a83c" />

## 🚀 Features

**Automatic PR Review:** Reviews pull requests on GitHub as soon as they are opened or updated.

**LLM-Powered Insights:** Uses Groq’s high-speed LLMs (LLaMA / Mixtral) to analyze code diffs.

**Direct GitHub Comments:** Posts AI-generated review feedback directly onto the PR conversation.

**Secure GitHub App Authentication:** Uses GitHub App JWT + installation tokens for safe repo access.

**Webhook-Driven Architecture:** No polling. System reacts instantly to GitHub events.

## 🔍 How It Works (Simple Explanation)
1.	A developer opens or updates a pull request in the repository where the GitHub App is installed.
2.	GitHub triggers a pull_request webhook event and sends it to your FastAPI server.
3.	The backend extracts key information:
4.	PR number
5.	Repository name
6.	PR action (opened / synchronize / reopened)
7.	The backend uses the App’s private key + App ID to create a signed JWT.
8.	GitHub validates the JWT and returns a short-lived installation access token.
9.	Using this token, the backend fetches the raw PR diff from GitHub.
10.	The diff is sent to the Groq LLM using a custom prompt for code review.
11.	The LLM generates feedback on code style, bugs, improvements, and best practices.
12.	The backend posts this review feedback as a comment directly on the pull request.
**In short:**
GitHub event → FastAPI → Authenticate → Fetch diff → AI review → GitHub comment
**🛠️ Tech Stack**
**Backend:** Python, FastAPI – API server and webhook handler, uvicorn – FastAPI execution
**GitHub Integration:** GitHub App, Webhook events (pull_request), JWT Authentication using private key, Installation Access Tokens for GitHub REST API calls, httpx – HTTP client for GitHub API
**AI / LLM:**	Groq API, LLaMA 3 / Mixtral models, Custom prompt + diff analysis
**Security:** HMAC webhook secret (GitHub → backend), JWT signing (backend → GitHub)
**Development Tools:** ngrok – expose localhost for GitHub webhooks, python-dotenv – environment variable handling, PyJWT – sign GitHub App tokens

## ⚙️ Setup Instructions
Follow these steps to run the AI PR Reviewer locally and connect it to GitHub.
### 1. Clone the Repository
git clone https://github.com/<your-username>/ai-code-reviewer.git
cd ai-code-reviewer
### 2. Create & Activate Virtual Environment
python -m venv venv
venv\Scripts\activate
### 3. Install Dependencies
pip install -r requirements.txt
This installs FastAPI, httpx, Groq client, PyJWT, and other required libraries.
### 4. Create a GitHub App
Inside GitHub:
1.	Go to Settings → Developer Settings → GitHub Apps → New GitHub App
2.	Set a name (e.g., AI PR Reviewer)
3.	The Webhook URL will be filled later with your ngrok URL
4.	Enable Webhook event:
o	Pull request
5.	Set Permissions:
o	Pull requests → Read
o	Issues → Read & write
6.	Generate a Webhook Secret
7.	Download the Private Key (.pem) file
8.	Install the app on the repository you want to test
9.	Note the App ID and Installation ID
### 5. Add Private Key to Project
Place the downloaded .pem file in the project root and rename it:
ai-code-reviewer/
  github-app-private-key.pem
### 6. Create a .env File
Inside the project root:
GROQ_API_KEY=
GITHUB_APP_ID=
GITHUB_PRIVATE_KEY_PATH=github-app-private-key.pem
GITHUB_INSTALLATION_ID=
WEBHOOK_SECRET=
### 7.Run the FastAPI Server
uvicorn app.main:app --reload
### 8. Start ngrok to Expose Your Local Server
In another terminal:
.\ngrok http 8000
ngrok will generate a public URL like:
https://abc123.ngrok-free.dev
Use that URL as your GitHub App's webhook:
https://abc123.ngrok-free.dev/webhook
### 9. Test the AI PR Reviewer
Trigger any of the following in the repo where your GitHub App is installed:
•	Open a new pull request
•	Push new commits to the PR
•	Reopen a PR
Your backend will:
1.	Receive the webhook
2.	Fetch the PR diff
3.	Send it to Groq’s LLM
4.	Post an AI-generated comment directly on the pull request 🎉
Check the Conversation tab of the PR to see the bot's comment.

## 📦 **requirements.txt**

This file tells Python which packages your project needs.
```txt
fastapi
uvicorn
httpx
python-dotenv
PyJWT
cryptography
groq
