from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from model import is_toxic

app = FastAPI()

# -------- HTTP API (for Swagger & testing) --------
class TextRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze_text(data: TextRequest):
    toxic, label, score = is_toxic(data.text)

    return {
         "toxic": toxic,
        "label": label,
        "confidence": score
    }

# -------- WebSocket (for live chat) --------
@app.websocket("/ws/chat")
async def chat_socket(websocket: WebSocket):
    await websocket.accept()

    while True:
        message = await websocket.receive_text()

        toxic, label, score = is_toxic(message)

        if toxic:
            await websocket.send_json({
                "status": "deleted",
                "reason": label,
                "confidence": round(score, 2),
                "message": message
            })
        else:
            await websocket.send_json({
                "status": "approved",
                "message": message
            })
