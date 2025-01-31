from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai  # Nutzt GPT für die Textgenerierung
import os
from fastapi.middleware.cors import CORSMiddleware

# Initialisiere die FastAPI-Anwendung
app = FastAPI()

# CORS aktivieren, damit Frontend die API nutzen kann
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Kann auf spezifische Domains begrenzt werden
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definiere das Datenmodell für die Anfrage
class YESCodeRequest(BaseModel):
    thema: str
    absicht: str
    kernbotschaft: str

# GPT-API Schlüssel aus Umgebungsvariablen laden
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY ist nicht gesetzt. Stelle sicher, dass die Umgebungsvariable korrekt definiert ist.")

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# API-Endpoint zur Generierung des Y.E.S. Codes
@app.post("/generate_yes_code")
def generate_yes_code(request: YESCodeRequest):
    try:
        # Baue den Anfrage-Prompt für GPT
        prompt = (
            f"Erstelle einen kraftvollen Y.E.S. Code in der IST-Form. "
            f"Thema: {request.thema}. "
            f"Absicht: {request.absicht}. "
            f"Kernbotschaft: {request.kernbotschaft}. "
            f"Formuliere es zu einem harmonischen, motivierenden Satz."
        )
        
        # GPT-API-Aufruf mit richtiger Syntax
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Du bist ein Experte für motivierende Sprache."},
                {"role": "user", "content": prompt}
            ]
        )
        
        yes_code = response.choices[0].message.content
        
        return {"yes_code": yes_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler bei der Verarbeitung: {str(e)}")
