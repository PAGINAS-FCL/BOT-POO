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
    ruta = ruta_progreso(usuario_id)
    if not os.path.exists(ruta):
        guardar_json(ruta, {
            "modulo": 0,
            "etapa": "inicio",
            "indice_pregunta": 0,
            "bienvenida_dada": True
        })
        return (
            "👋 ¡Bienvenido al curso de Programación Orientada a Objetos aplicada a HTML, CSS y JavaScript!\n"
            "Para comenzar, por favor escribe la palabra: **empezar**"
        )

    progreso = cargar_json(ruta)
    indice_modulo = progreso["modulo"]

    if indice_modulo >= len(modulos):
        return "🎉 ¡Felicitaciones! Has completado todos los módulos."

    modulo_actual = modulos[indice_modulo]
    etapa = progreso["etapa"]
    entrada = entrada.strip().lower()
    if etapa == "inicio":
        if entrada == "empezar":
            progreso["etapa"] = "textos"
            guardar_json(ruta, progreso)
            return (
                f"🎬 Video: {modulo_actual['video_url']}\n\n"
                f"📚 {modulo_actual['textos'][0]}\n\n"
                f"📚 {modulo_actual['textos'][1]}\n\n"
                f"NOTA: {modulo_actual['textos'][2]}"
            )
        else:
            return "❌ Para comenzar, debes escribir la palabra: **empezar**"
    elif etapa == "textos":
        if entrada == "seguir":
            progreso["etapa"] = "pregunta"
            guardar_json(ruta, progreso)
            return modulo_actual["preguntas"][0]["pregunta"]
        else:
            return "❌ Escribe la palabra **'seguir'** para continuar."
    elif etapa == "pregunta":
        i = progreso["indice_pregunta"]
        respuesta_correcta = modulo_actual["preguntas"][i]["respuesta"].strip().lower()

        if entrada == respuesta_correcta:
            i += 1
            if i >= len(modulo_actual["preguntas"]):
                progreso["modulo"] += 1
                progreso["etapa"] = "inicio"
                progreso["indice_pregunta"] = 0
                guardar_json(ruta, progreso)

                if progreso["modulo"] >= len(modulos):
                    return "🎉 ¡Felicitaciones! Has completado todos los módulos."

                return "✅ ¡Muy bien! Has terminado este módulo.\n\nEscribe **'empezar'** para continuar con el siguiente módulo."
            else:
                progreso["indice_pregunta"] = i
                guardar_json(ruta, progreso)
                return modulo_actual["preguntas"][i]["pregunta"]
        else:
            return "❌ Respuesta incorrecta. Intenta de nuevo."

    return "❌ Entrada no válida. Por favor, escribe una palabra correcta según la etapa."
