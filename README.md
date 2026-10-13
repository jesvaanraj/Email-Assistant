# Intelligent Email Assistant Using Ollama

An AI-powered web application that helps customer support teams analyze customer emails, retrieve similar historical conversations, generate professional email replies, improve response tone, and summarize customer concerns.

The application uses Flask for the backend, HTML, CSS, and JavaScript for the frontend, and Ollama to run the language model locally.

## Overview

Customer support teams often handle large volumes of emails related to delivery delays, refund requests, technical issues, and product complaints. Responding to these emails manually can be time-consuming.

The Intelligent Email Assistant simplifies this process by analyzing incoming emails, identifying customer intent, retrieving similar historical conversations, and generating context-aware responses.

The application also allows users to rewrite replies in different tones, summarize customer concerns, and save generated replies locally.

## Features

- **Customer Email Input:** Enter the customer name, email subject, and message.
- **Intent Detection:** Automatically identify the customer's intent using an AI model.
- **Similar Email Retrieval:** Retrieve relevant historical emails and their previous replies from a CSV dataset.
- **AI Reply Generation:** Generate professional and context-aware customer support responses.
- **Tone Improvement:** Rewrite responses in Friendly, Formal, or Empathetic tones.
- **Conversation Summarization:** Generate concise summaries of customer concerns.
- **Save Replies:** Store generated replies, customer details, detected intent, and timestamps in a local text file.
- **Copy Reply:** Copy generated responses for convenient reuse.
- **Local AI Processing:** Use Ollama without relying on a cloud-based language model API.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Flask | Backend web framework |
| Ollama | Local language model runtime |
| Llama 3.2 | AI-powered text generation |
| Pandas | CSV dataset processing |
| Scikit-learn | TF-IDF vectorization and cosine similarity |
| HTML | Web page structure |
| CSS | User interface styling |
| JavaScript | Frontend interactions and API requests |
| CSV | Historical email dataset |
| TXT | Storage of generated replies |

## System Architecture

The application follows a modular architecture.

1. **Input Module:** Collects the customer name, subject, and email.
2. **Intent Module:** Detects the intent of the customer email.
3. **Retrieval Module:** Finds the most similar historical email and previous reply.
4. **Reply Module:** Generates an AI-based customer response.
5. **Tone Module:** Improves the response using the selected tone.
6. **Summary Module:** Generates a concise summary of the customer email.
7. **Save Module:** Saves the generated reply, intent, and timestamp to a local file.

### Workflow

```text
Customer Email
      |
      v
Input Module
      |
      v
Intent Detection
      |
      v
Historical Email Retrieval
      |
      v
AI Reply Generation
      |
      v
Tone Improvement
      |
      v
Conversation Summary
      |
      v
Save Generated Reply
```

## Project Structure

```text
EmailAssistant/
│
├── app.py
├── input_module.py
├── intent_module.py
├── retrieval_module.py
├── reply_module.py
├── tone_module.py
├── summary_module.py
├── utils.py
├── requirements.txt
│
├── data/
│   └── emails.csv
│
├── outputs/
│   └── generated_reply.txt
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js
```

## Prerequisites

Install the following software before running the application:

- Python 3.10 or later
- Ollama
- Git
- A code editor such as Visual Studio Code

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/jesvaanraj/Email-Assistant.git
```

Navigate into the project directory:

```bash
cd Email-Assistant
```

### 2. Create a Virtual Environment

On Windows:

```bash
python -m venv .venv
```

Activate the environment:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

Download Ollama from its official website:

https://ollama.com/download

Install the application and ensure that the Ollama service is running.

### 5. Download the Language Model

Run:

```bash
ollama pull llama3.2
```

Verify that the model is installed:

```bash
ollama list
```

The application is configured to use the `llama3.2` model.

### 6. Prepare the Dataset

Ensure that the historical email dataset is available at:

```text
data/emails.csv
```

The CSV dataset should contain the following columns:

- `Email_ID`
- `Customer_Name`
- `Email_Date`
- `Category`
- `Priority`
- `Subject`
- `Customer_Email`
- `Intent`
- `Sentiment`
- `Previous_Reply`
- `Status`
- `Agent_Name`

The retrieval module requires the `Customer_Email` and `Previous_Reply` columns. The `Subject` column is used when available.

Use only anonymized or authorized data when publishing the dataset.

### 7. Run the Application

Start the Flask server:

```bash
python app.py
```

Open your browser and visit:

http://127.0.0.1:5000

The Intelligent Email Assistant web interface should now be available.

## Usage

### Step 1: Enter Customer Details

Provide the following information:

- Customer Name
- Email Subject
- Customer Email

### Step 2: Generate AI Response

Click **Generate AI Response**.

The application analyzes the email, detects the customer's intent, searches for similar historical emails, generates a professional response, and creates a summary.

### Step 3: Improve the Reply

Choose one of the following tones:

- Friendly
- Formal
- Empathetic

Click **Improve Tone** to rewrite the generated response.

### Step 4: Save the Reply

Click **Save Reply** to save the response locally.

The generated reply is stored in:

```text
outputs/generated_reply.txt
```

Each saved record includes the timestamp, customer information, detected intent, original email, and generated response.

## Example Input

**Customer Name**

```text
Joh
```

**Email Subject**

```text
Delivery Delay
```

**Customer Email**

```text
My package has not arrived yet.
```

**Reply Tone**

```text
Formal
```

## Expected Output

The application should display:

- Detected intent, such as Delivery Issue.
- A similar historical customer email.
- The corresponding previous reply.
- An AI-generated professional response.
- A tone-improved response.
- A concise conversation summary.
- A confirmation message when the reply is saved successfully.

The exact response depends on the language model and the historical dataset.

## Error Handling

### Ollama Connection Error

Ensure that Ollama is installed and running.

Check the installed models:

```bash
ollama list
```

Test the configured model:

```bash
ollama run llama3.2
```

### Missing Dataset

Verify that `data/emails.csv` exists and contains the required columns.

### Missing Python Packages

Install the dependencies again:

```bash
pip install -r requirements.txt
```

## Limitations

- Generated responses may require human review before use.
- Reply quality depends on the language model and historical dataset.
- Historical email retrieval depends on textual similarity.
- The application saves replies locally and does not send emails automatically.
- The AI model must be installed separately through Ollama.

## Future Enhancements

- Email integration with Gmail or Outlook.
- Support for additional customer intent categories.
- Improved semantic retrieval using sentence embeddings.
- Persistent database storage for customer interactions.
- Authentication and user management.
- Email analytics and reporting dashboard.
- Automated evaluation of generated reply quality.

## Author

**Jesvaan Raj**

GitHub: https://github.com/jesvaanraj

Project Repository: https://github.com/jesvaanraj/Email-Assistant

## License

This project is intended for educational and demonstration purposes.
