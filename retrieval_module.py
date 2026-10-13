from pathlib import Path

import pandas as pd

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.metrics.pairwise import cosine_similarity


DATA_PATH = (
    Path(__file__).parent
    / "data"
    / "emails.csv"
)


def load_emails():

    if not DATA_PATH.exists():

        raise FileNotFoundError(
            "Dataset not found. "
            "Please create data/emails.csv."
        )

    df = pd.read_csv(
        DATA_PATH
    ).fillna("")

    required_columns = [
        "Customer_Email",
        "Previous_Reply"
    ]

    for column in required_columns:

        if column not in df.columns:

            raise ValueError(
                f"Missing required column: {column}"
            )

    return df


def find_similar_email(
    subject,
    customer_email,
    history
):

    if history.empty:

        return None

    if "Subject" in history.columns:

        subjects = history["Subject"].astype(str)

    else:

        subjects = pd.Series(
            [""] * len(history),
            index=history.index
        )

    emails = history[
        "Customer_Email"
    ].astype(str)

    historical_texts = (
        subjects + " " + emails
    ).tolist()

    query = f"{subject} {customer_email}"

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        matrix = vectorizer.fit_transform(
            historical_texts + [query]
        )

        similarities = cosine_similarity(
            matrix[-1],
            matrix[:-1]
        ).flatten()

        best_index = similarities.argmax()

        result = history.iloc[
            best_index
        ].to_dict()

        result["_similarity"] = float(
            similarities[best_index]
        )

        return result

    except ValueError:

        return None