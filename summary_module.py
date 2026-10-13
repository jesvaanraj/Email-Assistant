from utils import ask_ollama


def summarize_email(
    subject,
    customer_email
):

    prompt = f"""
Summarize the customer's issue in 50 words or fewer.

Include:
- The main problem.
- The customer's concern.
- The assistance requested.

Do not invent information.

Subject:
{subject}

Customer Email:
{customer_email}

Return only the summary.
"""

    summary = ask_ollama(
        prompt,
        temperature=0.2
    )

    return summary.strip()