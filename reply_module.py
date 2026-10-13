from utils import ask_ollama


def generate_reply(
    customer_name,
    subject,
    customer_email,
    intent,
    similar_email=None
):

    previous_reply = "No previous reply available."

    if similar_email:
        previous_reply = similar_email.get(
            "Previous_Reply",
            previous_reply
        )

    prompt = f"""
You are a professional customer support agent.

Write a short, professional email reply.

Customer name: {customer_name}
Subject: {subject}
Customer email: {customer_email}
Detected intent: {intent}

Previous reply for reference:
{previous_reply}

Instructions:
1. Address the customer by their name.
2. Acknowledge their concern politely.
3. Explain the next step.
4. Do not invent shipment information or promises.
5. Keep the reply between 80 and 120 words.
6. Do not include explanations about your writing.
7. Do not include numbered lists.
8. Do not use placeholders such as [Your Name].
9. End with "Best regards," followed by "Customer Support Team".
10. Return only the email reply.
"""

    reply = ask_ollama(
        prompt,
        temperature=0.2
    )

    return reply.strip()