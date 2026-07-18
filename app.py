from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from faster_whisper import WhisperModel

from google import genai

from dotenv import load_dotenv

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
async def upload_audio(
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

        segments, info = whisper_model.transcribe(
            file_path,
            language="en"
        )

        transcript = ""

        for segment in segments:

            transcript += segment.text

        transcript = transcript.strip()

        print(
            "Transcript:",
            transcript
        )

        # Gemini Prompt

        prompt = f"""

You are a banking voice assistant.

Analyze the English voice command.

Classify it into ONLY ONE intent.

Allowed intents:

1. Send_money
- User wants to transfer/send money.

2. Download_statement
- User wants bank account statement.

3. Pay_bill
- User wants to pay any bill.

4. Unknown
- If the command does not match above intents.


Return ONLY valid JSON.

Do not add markdown.
Do not add explanations.


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



User command:

{transcript}

"""

        print(
            "USING GEMINI MODEL: gemini-2.5-flash"
        )



        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        ai_result = response.text.strip()

        # Remove markdown if Gemini adds it

        if ai_result.startswith("```json"):

            ai_result = ai_result.replace(
                "```json",
                ""
            )

        if ai_result.endswith("```"):

            ai_result = ai_result.replace(
                "```",
                ""
            )

        ai_result = ai_result.strip()

        # Convert to JSON

        try:

            ai_json = json.loads(
                ai_result
            )


        except Exception:

            ai_json = {

                "raw_response": ai_result

            }

        return {


            "success": True,

            "filename": filename,

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