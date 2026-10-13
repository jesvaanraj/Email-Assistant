from flask import Flask, render_template, request, jsonify

from intent_module import detect_intent
from retrieval_module import load_emails, find_similar_email
from reply_module import generate_reply
from tone_module import improve_tone
from summary_module import summarize_email
from utils import save_reply

app = Flask(__name__)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Analyze customer email and generate AI reply
@app.route("/analyze", methods=["POST"])
def analyze_email():

    try:
        data = request.get_json(silent=True) or {}

        customer_name = data.get(
            "customer_name", ""
        ).strip()

        subject = data.get(
            "subject", ""
        ).strip()

        customer_email = data.get(
            "customer_email", ""
        ).strip()

        tone = data.get(
            "tone", "Formal"
        ).strip()

        # Validate input
        if not customer_name or not subject or not customer_email:
            return jsonify({
                "success": False,
                "error": "Please fill in all the email fields."
            }), 400

        if tone not in ["Friendly", "Formal", "Empathetic"]:
            tone = "Formal"

        # 1. Detect customer intent
        intent = detect_intent(
            subject,
            customer_email
        )

        # 2. Load historical email dataset
        history = load_emails()

        # 3. Retrieve similar historical email
        similar = find_similar_email(
            subject,
            customer_email,
            history
        )

        if similar:
            previous_email = similar.get(
                "Customer_Email", ""
            )

            previous_reply = similar.get(
                "Previous_Reply", ""
            )

        else:
            previous_email = "No similar historical email found."

            previous_reply = "No previous reply available."

        # 4. Generate AI reply
        generated_reply = generate_reply(
            customer_name,
            subject,
            customer_email,
            intent,
            similar
        )

        # 5. Improve reply using selected tone
        tone_reply = improve_tone(
            generated_reply,
            tone
        )

        # 6. Summarize customer email
        summary = summarize_email(
            subject,
            customer_email
        )

        # Return all results to the frontend
        return jsonify({
            "success": True,
            "customer_name": customer_name,
            "subject": subject,
            "customer_email": customer_email,
            "intent": intent,
            "previous_email": previous_email,
            "previous_reply": previous_reply,
            "generated_reply": generated_reply,
            "tone_reply": tone_reply,
            "tone": tone,
            "summary": summary
        })

    except Exception as error:

        app.logger.exception(
            "Email analysis failed"
        )

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# Improve reply tone separately
@app.route("/improve-tone", methods=["POST"])
def improve_email_tone():

    try:
        data = request.get_json(silent=True) or {}

        reply = data.get(
            "reply", ""
        ).strip()

        tone = data.get(
            "tone", ""
        ).strip()

        if not reply:
            return jsonify({
                "success": False,
                "error": "Please enter a reply before improving its tone."
            }), 400

        if tone not in ["Friendly", "Formal", "Empathetic"]:
            return jsonify({
                "success": False,
                "error": "Please select a valid tone."
            }), 400

        improved_reply = improve_tone(
            reply,
            tone
        )

        return jsonify({
            "success": True,
            "reply": improved_reply,
            "tone": tone
        })

    except Exception as error:

        app.logger.exception(
            "Tone improvement failed"
        )

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# Save generated reply
@app.route("/save", methods=["POST"])
def save_email_reply():

    try:
        data = request.get_json(silent=True) or {}

        customer_name = data.get(
            "customer_name", ""
        ).strip()

        subject = data.get(
            "subject", ""
        ).strip()

        customer_email = data.get(
            "customer_email", ""
        ).strip()

        intent = data.get(
            "intent", ""
        ).strip()

        generated_reply = data.get(
            "generated_reply", ""
        ).strip()

        # Validate the information received from JavaScript
        required_fields = [
            customer_name,
            subject,
            customer_email,
            intent,
            generated_reply
        ]

        if not all(required_fields):
            return jsonify({
                "success": False,
                "error": (
                    "Missing information. "
                    "Please provide the customer details "
                    "and a generated reply."
                )
            }), 400

        # Save to the local output file
        output_path = save_reply(
            customer_name=customer_name,
            subject=subject,
            customer_email=customer_email,
            generated_reply=generated_reply,
            intent=intent
        )

        return jsonify({
            "success": True,
            "message": "Reply saved successfully!",
            "file": str(output_path)
        })

    except Exception as error:

        app.logger.exception(
            "Saving reply failed"
        )

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )