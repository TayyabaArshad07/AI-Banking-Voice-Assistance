from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from faster_whisper import WhisperModel

from google import genai

from dotenv import load_dotenv

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

import os
import json
import traceback

# Load Environment Variables

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    raise Exception(
        "Gemini API key not found. Add GEMINI_API_KEY in .env file"
    )

# Gemini Client

client = genai.Client(
    api_key=GEMINI_API_KEY
)

# FastAPI Setup
app = FastAPI()

# Rate Limiter

limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):

    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "message": "Too many requests. Please wait one minute before trying again."
        }
    )

# Static Files

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

# Templates

templates = Jinja2Templates(
    directory="templates"
)

# Load Whisper

print("Loading Whisper Model...")

whisper_model = WhisperModel(
     "base",
    device="cpu",
    compute_type="int8"
)
print("Whisper Model Loaded!")

# Home Page

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

# Upload Audio

@app.post("/upload")
@limiter.limit("5/minute")
async def upload_audio(
    request: Request,
    audio: UploadFile = File(...)
):

    try:

        if audio is None:
            raise HTTPException(
                status_code=400,
                detail="No audio file received"
            )

        # Create uploads folder

        os.makedirs(
            "uploads",
            exist_ok=True
        )

        filename = audio.filename

        if filename == "" or filename is None:
            filename = "recording.webm"

        file_path = os.path.join(
            "uploads",
            filename
        )

        # Save audio

        with open(
            file_path,
            "wb"
        ) as buffer:

            content = await audio.read()

            buffer.write(content)

        print("Audio saved:", file_path)

        # Whisper Transcription
    
        print("Transcribing...")

        # Auto detect English / Urdu
        segments, info = whisper_model.transcribe(
            file_path
        )

        transcript = ""

        for segment in segments:
            transcript += segment.text

        transcript = transcript.strip()

        detected_language = info.language

        print("Detected Language:", detected_language)
        print("Transcript:", transcript)

        if detected_language == "hi" and transcript:


            translate_prompt = f"""
Translate the following Hindi text into Urdu.

Return ONLY the Urdu translation.
Do not add explanations.

Hindi:
{transcript}
"""

            translation_response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=translate_prompt
         )

            transcript = translation_response.text.strip()

            print("Translated Urdu:", transcript)

        # Gemini Prompt

        prompt = f"""

You are an AI Banking Voice Assistant.

The user may speak in English or Urdu.

If the transcript has already been translated from Hindi to Urdu, process it normally.

Understand the user's request regardless of language.

Classify it into ONLY ONE of the following intents:

1. Send_money
- User wants to transfer money.

2. Download_statement
- User wants to download a bank statement.

3. Pay_bill
- User wants to pay a utility or other bill.

4. Unknown
- Command does not match any intent.

Return ONLY valid JSON.

Do not use markdown.

JSON format:

{{
    "intent":"",
    "amount":"",
    "receiver":"",
    "message":""
}}

Examples:

User:
Send 5000 rupees to Ali

Output:
{{
    "intent":"Send_money",
    "amount":"5000",
    "receiver":"Ali",
    "message":""
}}

User:
Download my bank statement

Output:
{{
    "intent":"Download_statement",
    "amount":"",
    "receiver":"",
    "message":""
}}

User:
Pay my electricity bill

Output:
{{
    "intent":"Pay_bill",
    "amount":"",
    "receiver":"",
    "message":""
}}

User:
علی کو 5000 روپے بھیجو

Output:
{{
    "intent":"Send_money",
    "amount":"5000",
    "receiver":"Ali",
    "message":""
}}

User:
میرا بینک اسٹیٹمنٹ ڈاؤن لوڈ کرو

Output:
{{
    "intent":"Download_statement",
    "amount":"",
    "receiver":"",
    "message":""
}}

User:
میرا بجلی کا بل ادا کرو

Output:
{{
    "intent":"Pay_bill",
    "amount":"",
    "receiver":"",
    "message":""
}}

User command:

{transcript}

"""

        print("USING GEMINI MODEL: gemini-2.5-flash")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        ai_result = response.text.strip()

        # Remove markdown if Gemini returns it

        if ai_result.startswith("```json"):
            ai_result = ai_result.replace("```json", "")

        if ai_result.endswith("```"):
            ai_result = ai_result.replace("```", "")

        ai_result = ai_result.strip()

        # Convert JSON

        try:

            ai_json = json.loads(ai_result)

        except Exception:

            ai_json = {
                "raw_response": ai_result
            }

        return {

            "success": True,

            "filename": filename,

            "language": detected_language,

            "transcription": transcript,

            "result": ai_json

        }

    except Exception as e:

        print("\nERROR")

        traceback.print_exc()

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )
    

