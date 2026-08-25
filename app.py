import base64
import json
import os
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI

app = FastAPI(title="CF7 Painel Online")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

PUBLIC = Path(__file__).parent / "public"
app.mount("/static", StaticFiles(directory=PUBLIC), name="static")

@app.get("/")
def home():
    return FileResponse(PUBLIC / "index.html")

@app.post("/api/analyze-bet")
async def analyze_bet(image: UploadFile = File(...)):
    if not os.environ.get("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY não configurada no servidor.")

    content = await image.read()
    if not content:
        raise HTTPException(status_code=400, detail="Imagem vazia.")
    if len(content) > 12 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Imagem muito grande.")

    mime = image.content_type or "image/jpeg"
    encoded = base64.b64encode(content).decode("ascii")
    data_url = f"data:{mime};base64,{encoded}"

    prompt = """
Analise o print de um bilhete de aposta esportiva e retorne SOMENTE JSON válido.
Não invente dados. Se algo não estiver legível, use null.
Formato:
{
  "bookmaker": "nome da casa ou null",
  "bet_type": "simples|multipla|outro|null",
  "event": "evento/jogo; se múltipla, resumo curto das seleções",
  "market": "mercado/seleção principal; se múltipla, resumo curto",
  "stake": 25.0,
  "odd": 1.75,
  "potential_return": 43.75,
  "status": "open|green|red|void|null",
  "confidence": 0.0
}
Valores monetários devem ser números, sem R$.
"status" é open se estiver em aberto; green/red/void somente se o print mostrar claramente o resultado final.
"""

    response = client.responses.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-5.6"),
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": prompt},
                {"type": "input_image", "image_url": data_url}
            ]
        }]
    )

    text = response.output_text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].strip()

    try:
        data = json.loads(text)
    except Exception:
        raise HTTPException(status_code=502, detail="A IA respondeu em formato inesperado.")

    return data
