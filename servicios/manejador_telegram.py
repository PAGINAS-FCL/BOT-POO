import httpx
from fastapi.responses import JSONResponse
from servicios.gestor_modulos import procesar_entrada_usuario

TOKEN_BOT = "7242930029:AAFH_MrBB4UFVwDSJH6Nagqy7E75JkjD5QE"
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
    return {"status": "mensaje_procesado"}

