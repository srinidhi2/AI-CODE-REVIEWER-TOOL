from fastapi import APIRouter, Request, Header
from app.services.github_service import fetch_pr_diff, post_pr_comment
from app.services.ai_service import review_code

router = APIRouter()

@router.post("/webhook")
async def handle_webhook(
    request: Request,
    x_github_event: str = Header(None),
):
    """
    This endpoint receives webhook events from GitHub.

    Flow now:
    - Check it's a pull_request event
    - Extract repo name, PR number, and action
    - For certain actions (opened, synchronize, reopened):
        * Fetch PR diff from GitHub
        * Send diff to AI for review
        * Log AI feedback (for now)
    """
    payload = await request.json()

    print("\n🔔 Webhook event received")
    print(f"X-GitHub-Event: {x_github_event}")
    print(f"Action: {payload.get('action')}")

    # We only care about pull_request events
    if x_github_event == "pull_request":
        action = payload.get("action")
        pr = payload.get("pull_request", {})
        repo = payload.get("repository", {})

        pr_number = pr.get("number")
        repo_full_name = repo.get("full_name")

        print(f"➡ PR Event: action={action}, repo={repo_full_name}, pr_number={pr_number}")

        # We'll only run review on certain actions
        if action in ("opened", "synchronize", "reopened"):
            if repo_full_name and pr_number:
                try:
                    print("📥 Fetching PR diff from GitHub...")
                    diff_text = fetch_pr_diff(repo_full_name, pr_number)

                    print("🧠 Sending diff to AI for review...")
                    ai_feedback = review_code(diff_text)

                    print("\n✅ AI review generated:")
                    print(ai_feedback)
                    print("✅ End of AI review\n")

                    # Post the AI feedback as a comment on the PR
                    comment_body = (
                        "🤖 **AI Code Review Summary**\n\n"
                        + ai_feedback
                    )

                    print("💬 Posting AI review as GitHub PR comment...")
                    post_pr_comment(repo_full_name, pr_number, comment_body)
                    print("✅ Comment posted.")


                    # Step 6.5: later we will post this as a PR comment
                except Exception as e:
                    print(f"❌ Error while processing PR review: {e}")

    # Always respond 200 OK to GitHub
    return {"message": "Webhook received"}
