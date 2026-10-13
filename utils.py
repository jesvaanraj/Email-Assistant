from datetime import datetime
from pathlib import Path

import requests


# Ollama configuration

OLLAMA_URL = "http://localhost:11434/api/generate"

OLLAMA_MODEL = "llama3.2"


# Output file location

OUTPUT_PATH = (
    Path(__file__).parent
    / "outputs"
    / "generated_reply.txt"
)


# ============================================
# CONNECT TO OLLAMA
# ============================================

def ask_ollama(prompt, temperature=0.3):

    try:

        response = requests.post(
            OLLAMA_URL,

            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,

                "options": {
                    "temperature": temperature
                }
            },

            timeout=180
        )

        response.raise_for_status()

    except requests.exceptions.ConnectionError as error:

        raise RuntimeError(
            "Cannot connect to Ollama. "
            "Make sure Ollama is running."
        ) from error

    except requests.exceptions.Timeout as error:

        raise RuntimeError(
            "Ollama took too long to respond. "
            "Please try again."
        ) from error

    except requests.exceptions.HTTPError as error:

        raise RuntimeError(
            "Ollama returned an error: "
            + response.text
        ) from error

    result = response.json().get(
        "response",
        ""
    ).strip()

    if not result:

        raise RuntimeError(
            "Ollama returned an empty response."
        )

    return result


# ============================================
# SAVE GENERATED REPLY
# ============================================

def save_reply(
    customer_name,
    subject,
    customer_email,
    generated_reply,
    intent
):

    # Create output folder if necessary

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    # Generate timestamp

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    # Prepare output content

    content = f"""
{'=' * 70}

Date and Time: {timestamp}

Customer Name: {customer_name}

Subject: {subject}

Detected Intent: {intent}

Customer Email:
{customer_email}

Generated Reply:
{generated_reply}

"""


    # Append the reply to the output file

    with open(
        OUTPUT_PATH,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(content)


    return OUTPUT_PATH