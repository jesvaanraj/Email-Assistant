from utils import ask_ollama


def improve_tone(reply, tone):

    allowed_tones = [
        "Friendly",
        "Formal",
        "Empathetic"
    ]

    if tone not in allowed_tones:

        raise ValueError(
            "Please select a valid tone."
        )

    prompt = f"""
Rewrite the following customer support email
in a {tone.lower()} tone.

Requirements:
- Preserve the original meaning.
- Maintain professional communication.
- Correct grammar where necessary.
- Do not invent facts or promises.
- Return only the rewritten email.

Original Email:
{reply}
"""

    improved_reply = ask_ollama(
        prompt,
        temperature=0.3
    )

    return improved_reply.strip()