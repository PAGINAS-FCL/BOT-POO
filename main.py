from fastapi import FastAPI, Request
from servicios.manejador_telegram import procesar_actualizacion_telegram

app = FastAPI()

@app.post("/webhook")
async def webhook_telegram(request: Request):
    datos = await request.json()
    return await procesar_actualizacion_telegram(datos)
