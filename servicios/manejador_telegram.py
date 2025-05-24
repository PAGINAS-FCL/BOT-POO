from servicios.gestor_modulos import procesar_entrada_usuario as procesar_usuario
import httpx
import os

TOKEN_BOT = os.getenv("TOKEN_BOT")
API_URL = f"https://api.telegram.org/bot{TOKEN_BOT}"

async def enviar_mensaje(chat_id, texto):
    async with httpx.AsyncClient() as client:
        await client.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": texto})

async def procesar_actualizacion_telegram(datos: dict):
    mensaje = datos.get("message")
    if not mensaje:
        return {"status": "sin_mensaje"}

    remitente = mensaje.get("from", {})
    usuario_id = remitente.get("id")
    es_bot = remitente.get("is_bot", True)
    texto = mensaje.get("text", "")
    if es_bot:
        print(f"Bot detectado y bloqueado: ID {usuario_id}")
        return {"status": "bloqueado_por_ser_bot"}
    
    SPAM_KEYWORDS = ["vpn", "http", ".ru", "instagram", "youtube", "начать", "бесплатно"]
    if any(palabra in texto.lower() for palabra in SPAM_KEYWORDS):
        print(f"Mensaje sospechoso de {usuario_id}: {texto}")
        return {"status": "mensaje_spam_bloqueado"}

    print(f"Mensaje permitido de {usuario_id}: {texto}")

    respuesta = procesar_usuario(usuario_id, texto)
    await enviar_mensaje(usuario_id, respuesta)
    return {"status": "mensaje_procesado"}

