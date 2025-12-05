import os
import time
from typing import Optional

import httpx
import jwt  # PyJWT
from dotenv import load_dotenv

load_dotenv()

GITHUB_APP_ID = os.getenv("GITHUB_APP_ID")
GITHUB_PRIVATE_KEY_PATH = os.getenv("GITHUB_PRIVATE_KEY_PATH")
GITHUB_INSTALLATION_ID = os.getenv("GITHUB_INSTALLATION_ID")

GITHUB_API_BASE = "https://api.github.com"


def _load_private_key() -> str:
    """Load the GitHub App private key from the .pem file."""
    if not GITHUB_PRIVATE_KEY_PATH:
        raise RuntimeError("GITHUB_PRIVATE_KEY_PATH is not set in .env")

    if not os.path.exists(GITHUB_PRIVATE_KEY_PATH):
        raise RuntimeError(f"Private key file not found: {GITHUB_PRIVATE_KEY_PATH}")

    with open(GITHUB_PRIVATE_KEY_PATH, "r", encoding="utf-8") as f:
        return f.read()


def create_jwt() -> str:
    """
    Create a JSON Web Token (JWT) for authenticating as the GitHub App.
    This JWT is used to request an installation access token.
    """
    if not GITHUB_APP_ID:
        raise RuntimeError("GITHUB_APP_ID is not set in .env")

    private_key = _load_private_key()

    now = int(time.time())
    payload = {
        # Issued at time
        "iat": now - 60,
        # JWT expiration time (max 10 minutes)
        "exp": now + (10 * 60),
        # GitHub App's identifier
        "iss": GITHUB_APP_ID,
    }

    encoded_jwt = jwt.encode(payload, private_key, algorithm="RS256")
    # PyJWT may return bytes in older versions; ensure string
    if isinstance(encoded_jwt, bytes):
        encoded_jwt = encoded_jwt.decode("utf-8")
    return encoded_jwt


def get_installation_access_token() -> str:
    """
    Use the App JWT to request an installation access token.
    This token is what we use to call GitHub REST APIs
    (e.g., fetch PR diff, post comments).
    """
    if not GITHUB_INSTALLATION_ID:
        raise RuntimeError("GITHUB_INSTALLATION_ID is not set in .env")

    jwt_token = create_jwt()

    url = f"{GITHUB_API_BASE}/app/installations/{GITHUB_INSTALLATION_ID}/access_tokens"

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json",
    }

    with httpx.Client() as client:
        resp = client.post(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        token = data.get("token")
        if not token:
            raise RuntimeError("No 'token' field in GitHub installation token response")
        return token


def fetch_pr_diff(repo_full_name: str, pr_number: int) -> str:
    """
    Fetch the full diff for a pull request as plain text.

    repo_full_name: "owner/repo" (e.g., "ganta/pr-reviewer-demo")
    pr_number: PR number (e.g., 1)
    """
    token = get_installation_access_token()

    url = f"{GITHUB_API_BASE}/repos/{repo_full_name}/pulls/{pr_number}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3.diff",  # ask for raw diff
        "User-Agent": "ai-pr-reviewer",
    }

    with httpx.Client() as client:
        resp = client.get(url, headers=headers)
        resp.raise_for_status()
        diff_text = resp.text

    return diff_text


def post_pr_comment(repo_full_name: str, pr_number: int, body: str) -> None:
    """
    Post a comment on a pull request.

    Note: For GitHub's API, PR comments use the "issues" comments endpoint.
    """
    token = get_installation_access_token()

    url = f"{GITHUB_API_BASE}/repos/{repo_full_name}/issues/{pr_number}/comments"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "ai-pr-reviewer",
    }

    json_data = {"body": body}

    with httpx.Client() as client:
        resp = client.post(url, headers=headers, json=json_data)
        resp.raise_for_status()
