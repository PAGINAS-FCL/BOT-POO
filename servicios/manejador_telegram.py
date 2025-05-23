import httpx
from fastapi.responses import JSONResponse
from servicios.gestor_modulos import procesar_entrada_usuario

TOKEN_BOT = "7835514917:AAG0InbvhNg6c21gtm5QvVEd1KzMy9qFduE"
API_URL = f"https://api.telegram.org/bot{TOKEN_BOT}"

async def enviar_mensaje(chat_id, texto):
    async with httpx.AsyncClient() as client:
        await client.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": texto})

async def procesar_actualizacion_telegram(datos):
    mensaje = datos.get("message")
    if not mensaje:
        return JSONResponse(status_code=200, content={"ok": True})

    texto = mensaje.get("text", "").strip().lower()
    chat_id = mensaje["chat"]["id"]
    usuario_id = str(mensaje["from"]["id"])

    respuesta = procesar_entrada_usuario(usuario_id, texto)
    await enviar_mensaje(chat_id, respuesta)

    return JSONResponse(status_code=200, content={"ok": True})
