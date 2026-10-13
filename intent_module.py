from utils import ask_ollama


ALLOWED_INTENTS = [
    "Delivery Issue",
    "Refund Request",
    "Product Complaint",
    "Technical Support",
    "Order Cancellation",
    "General Inquiry"
]


def detect_intent(subject, customer_email):

    prompt = f"""
You are a customer support email classifier.

Classify the following email into exactly ONE
of these categories:

1. Delivery Issue
2. Refund Request
3. Product Complaint
4. Technical Support
5. Order Cancellation
6. General Inquiry

Return only the category name.

Subject:
{subject}

Customer Email:
{customer_email}
"""

    result = ask_ollama(
        prompt,
        temperature=0
    )

    result = result.strip().strip('"').strip("'")

    for intent in ALLOWED_INTENTS:

        if intent.lower() in result.lower():

            return intent

    return "General Inquiry"