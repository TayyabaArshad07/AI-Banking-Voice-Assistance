# AI Banking Voice Assistant

## Introduction

The **AI Banking Voice Assistant** is a voice-enabled web application that allows users to interact with banking services using natural language voice commands. Users can either record their voice through the browser or upload an audio file.

The application converts speech into text using **Faster-Whisper** and then uses **Google Gemini** to understand the user's request, identify the banking intent, and extract relevant information such as the transaction amount and recipient. The extracted information is returned in a structured JSON format.

This project demonstrates the integration of **Speech-to-Text (STT)**, **Natural Language Processing (NLP)**, and **Large Language Models (LLMs)** in a banking use case.

---

## Technologies Used

### Backend
- Python
- FastAPI
- Uvicorn

### AI & Speech Recognition
- Faster-Whisper
- Google Gemini API

### Frontend
- HTML
- CSS
- JavaScript

### Additional Libraries
- Jinja2
- Python Multipart

---

## Project Workflow

1. The user records a voice command or uploads an audio file.
2. The audio file is sent to the FastAPI backend.
3. Faster-Whisper converts the speech into text.
4. The transcription is passed to Google Gemini.
5. Gemini identifies the banking intent and extracts the required information.
6. The application returns a structured JSON response containing the detected intent and extracted entities.

---

## Supported Voice Commands

### 1. Send Money

Transfers money to another person.

**Intent:** `Send_money`

**Information Extracted**
- Amount
- Receiver

**Example Commands**
- "Send 500 rupees to Ali."
- "Transfer 2,000 rupees to Ahmed."
- "Please send 1,500 rupees to Sara."
- "Send five thousand rupees to John."

**Example Output**

```json
{
  "intent": "Send_money",
  "amount": "500",
  "receiver": "Ali",
  "message": ""
}
```

---

### 2. Download Bank Statement

Downloads or generates the user's bank statement.

**Intent:** `Download_bank_statement`

**Example Commands**
- "Download my bank statement."
- "Generate my account statement."
- "I need my bank statement."
- "Show my account statement."

**Example Output**

```json
{
  "intent": "Download_bank_statement",
  "amount": "",
  "receiver": "",
  "message": ""
}
```

---

### 3. Pay Bill

Recognizes utility or service bill payment requests.

**Intent:** `Pay_bill`

**Example Commands**
- "Pay my electricity bill."
- "Pay my gas bill."
- "Pay my internet bill."
- "Pay my water bill."

**Example Output**

```json
{
  "intent": "Pay_bill",
  "amount": "",
  "receiver": "",
  "message": ""
}
```

---

### 4. Unknown Commands

Commands unrelated to the supported banking operations are classified as unknown.

**Intent:** `Unknown`

**Example Commands**
- "Play some music."
- "What's the weather today?"
- "Open YouTube."
- "Tell me a joke."

**Example Output**

```json
{
  "intent": "Unknown",
  "amount": "",
  "receiver": "",
  "message": ""
}
```