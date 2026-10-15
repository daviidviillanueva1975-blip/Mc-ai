import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# Configuramos la IA con la llave de Google Gemini
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

class ChatRequest(BaseModel):
    mob: str
    prompt: str
    player_info: dict

@app.post("/chat")
def chat_with_mob(data: ChatRequest):
    try:
        system_instruction = f"""
        Eres un {data.mob} de Minecraft Bedrock. 
        Estás dentro del juego de bloques. Responde de forma inmersiva y fiel a tu naturaleza.
        OBLIGATORIO: Debes incluir acciones físicas o gestos entre asteriscos (ej: *te mira con desconfianza*, *salta alegremente*), seguidas de lo que dices.
        El jugador que te habla se llama {data.player_info['nombre']}, es de género {data.player_info['genero']} y su descripción física es: {data.player_info['apariencia']}. Trátalo acorde a eso.
        Sé breve, divertido y creativo.
        """
        
        prompt_final = f"{system_instruction}\n\nJugador dice: {data.prompt}"
        response = model.generate_content(prompt_final)
        
        return {"reply": response.text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
      
