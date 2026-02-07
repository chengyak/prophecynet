import os
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
from typing import AsyncIterable

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="/Users/richardbot/code/prophecynet/app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="/Users/richardbot/code/prophecynet/app/templates")

# Configure Gemini API
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

async def generate_astrology_reading(birthday: str, birth_time: str, location: str) -> AsyncIterable[str]:
    if not GOOGLE_API_KEY:
        yield "Error: GOOGLE_API_KEY environment variable not set."
        return

    try:
        model = genai.GenerativeModel('gemini-2.5-flash-lite')

        prompt = (
            f"You are a wise Chinese astrologer. A person was born on {birthday} at {birth_time} "
            f"in {location}. "
            f"Using the principles of 'The Eight Characters' (Ba Zi) and Chinese astrology, "
            f"analyze their destiny. Discuss their personality, career, relationships, and health. "
            f"Provide the response in a mystical yet easy-to-understand style. "
            f"Format the output with HTML tags for structure (e.g., <h3>, <p>, <ul>, <li>)."
        )

        response = model.generate_content(prompt, stream=True)

        for chunk in response:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        yield f"An error occurred: {str(e)}"

@app.post("/predict")
async def predict_destiny(
    birthday: str = Form(...),
    birth_time: str = Form(...),
    location: str = Form(...)
):
    return StreamingResponse(
        generate_astrology_reading(birthday, birth_time, location),
        media_type="text/plain"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
