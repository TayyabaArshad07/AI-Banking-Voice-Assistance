# AI Banking Voice Assistant

## Introduction

The AI Banking Voice Assistant is a voice-enabled web application that allows users to interact with banking services using natural language voice commands. Users can record their voice or upload an audio file. The application uses Faster-Whisper for speech-to-text conversion and Google Gemini to identify banking intents and extract relevant information. It supports both English and Urdu voice commands, automatically translates Hindi transcripts to Urdu when required, and includes rate limiting to prevent request spamming.

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
- SlowAPI
- Python-dotenv

---

## Project Workflow

1. The user records a voice command or uploads an audio file.
2. The audio is sent to the FastAPI backend.
3. Faster-Whisper converts speech into text and detects the language.
4. If the transcript is detected in Hindi, it is translated into Urdu.
5. Google Gemini identifies the banking intent and extracts the required information.
6. The application returns a structured JSON response.
7. Rate limiting prevents excessive requests and API spamming.

---

## Supported Voice Commands

### 1. Send Money

**Intent:** `Send_money`

**Information Extracted**
- Amount
- Receiver

**Example Commands**
- "Send 500 rupees to Ali."
- "Transfer 2,000 rupees to Ahmed."
- "Ali ko 5000 rupees bhejo."
- "علی کو 5000 روپے بھیجو۔"

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

**Intent:** `Download_statement`

**Example Commands**
- "Download my bank statement."
- "Generate my account statement."
- "Mera bank statement download karo."
- "میرا بینک اسٹیٹمنٹ ڈاؤن لوڈ کرو۔"

**Example Output**

```json
{
  "intent": "Download_statement",
  "amount": "",
  "receiver": "",
  "message": ""
}
```

---

### 3. Pay Bill

**Intent:** `Pay_bill`

**Example Commands**
- "Pay my electricity bill."
- "Pay my gas bill."
- "Bijli ka bill ada karo."
- "میرا بجلی کا بل ادا کرو۔"

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
