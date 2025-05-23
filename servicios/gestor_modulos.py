import os
from utilidades.json_utils import cargar_json, guardar_json

RUTA_MODULOS = "modulos/modulos.json"
RUTA_PROGRESO = "progreso"

modulos = cargar_json(RUTA_MODULOS)

def ruta_progreso(usuario_id):
    return f"{RUTA_PROGRESO}/usuario_{usuario_id}.json"

def inicializar_usuario(usuario_id):
    ruta = ruta_progreso(usuario_id)
    if not os.path.exists(ruta):
        guardar_json(ruta, {"modulo": 0, "etapa": "inicio", "indice_pregunta": 0})
    return cargar_json(ruta)

def procesar_entrada_usuario(usuario_id, entrada):
    progreso = inicializar_usuario(usuario_id)
    indice_modulo = progreso["modulo"]

    if indice_modulo >= len(modulos):
        return "🎉 ¡Felicitaciones! Has completado todos los módulos."

    modulo_actual = modulos[indice_modulo]
    etapa = progreso["etapa"]
    entrada = entrada.strip().lower()

    if etapa == "inicio":
        if entrada == "empezar":
            progreso["etapa"] = "textos"
            guardar_json(ruta_progreso(usuario_id), progreso)
            return f"🎬 Video: {modulo_actual['video_url']}\n\n📚 {modulo_actual['textos'][0]}\n\n📚 {modulo_actual['textos'][1]}"
        else:
            return "❌ Debes escribir la palabra: 'empezar'"

    elif etapa == "textos":
        if entrada == "seguir":
            progreso["etapa"] = "pregunta"
            guardar_json(ruta_progreso(usuario_id), progreso)
            return modulo_actual["preguntas"][0]["pregunta"]
        else:
            return "❌ Escribe 'seguir' para continuar."

    elif etapa == "pregunta":
        i = progreso["indice_pregunta"]
        respuesta_correcta = modulo_actual["preguntas"][i]["respuesta"]

        if entrada == respuesta_correcta.lower():
            i += 1
            if i >= len(modulo_actual["preguntas"]):
                progreso["modulo"] += 1
                progreso["etapa"] = "inicio"
                progreso["indice_pregunta"] = 0
                guardar_json(ruta_progreso(usuario_id), progreso)
                return "✅ ¡Muy bien! Has terminado este módulo. Escribe 'siguiente modulo' para continuar."
            else:
                progreso["indice_pregunta"] = i
                guardar_json(ruta_progreso(usuario_id), progreso)
                return modulo_actual["preguntas"][i]["pregunta"]
        else:
            return "❌ Respuesta incorrecta. Intenta de nuevo."

    elif etapa == "inicio" and entrada == "siguiente modulo":
        return "🔄 Iniciando siguiente módulo...\n\nEscribe 'empezar' para continuar."

    return "❌ Entrada no válida. Por favor, escribe una palabra correcta según la etapa."
