from flask import Flask, request, Response
import json
from datetime import datetime
from pathlib import Path
from collections import Counter

app = Flask(__name__)

ARCHIVO_PREDICCIONES = Path("predicciones.jsonl")

CATEGORIAS = [
    "NO ENFERMO",
    "ENFERMEDAD LEVE",
    "ENFERMEDAD AGUDA",
    "ENFERMEDAD CRÓNICA",
    "ENFERMEDAD TERMINAL"
]


def clasificar_estado(valores):
    """
    Función simulada que recibe una lista con tres valores:
    [temperatura, nivel_dolor, dias_sintomas]
    """

    temperatura = float(valores[0])
    nivel_dolor = float(valores[1])
    dias_sintomas = float(valores[2])

    if temperatura >= 40 or nivel_dolor >= 9 or (dias_sintomas >= 90 and nivel_dolor >= 7):
        return "ENFERMEDAD TERMINAL"

    if dias_sintomas >= 30 and (temperatura >= 37.5 or nivel_dolor >= 4):
        return "ENFERMEDAD CRÓNICA"

    if temperatura >= 39 or nivel_dolor >= 8 or (temperatura >= 38.5 and nivel_dolor >= 6):
        return "ENFERMEDAD AGUDA"

    if temperatura >= 37.5 or nivel_dolor >= 3 or dias_sintomas >= 3:
        return "ENFERMEDAD LEVE"

    return "NO ENFERMO"


def responder_json(contenido, codigo=200):
    return Response(
        json.dumps(contenido, ensure_ascii=False),
        status=codigo,
        content_type="application/json; charset=utf-8"
    )


def guardar_prediccion(registro):
    with ARCHIVO_PREDICCIONES.open("a", encoding="utf-8") as archivo:
        archivo.write(json.dumps(registro, ensure_ascii=False) + "\n")


def leer_predicciones():
    if not ARCHIVO_PREDICCIONES.exists():
        return []

    predicciones = []

    with ARCHIVO_PREDICCIONES.open("r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea:
                predicciones.append(json.loads(linea))

    return predicciones


@app.route("/", methods=["GET"])
def inicio():
    return responder_json({
        "mensaje": "Servicio de clasificación médica simulado activo",
        "endpoint_prediccion": "/predecir",
        "endpoint_reporte": "/reporte",
        "formato_entrada": {
            "valores": ["temperatura", "nivel_dolor", "dias_sintomas"]
        },
        "categorias": CATEGORIAS
    })


@app.route("/predecir", methods=["POST"])
def predecir():
    datos = request.get_json()

    if not datos or "valores" not in datos:
        return responder_json({
            "error": "Debe enviar un JSON con la clave 'valores'.",
            "ejemplo": {
                "valores": [37.8, 4, 3]
            }
        }, 400)

    valores = datos["valores"]

    if not isinstance(valores, list) or len(valores) != 3:
        return responder_json({
            "error": "La clave 'valores' debe contener una lista con exactamente 3 números.",
            "ejemplo": {
                "valores": [37.8, 4, 3]
            }
        }, 400)

    try:
        estado = clasificar_estado(valores)
    except ValueError:
        return responder_json({
            "error": "Todos los valores deben ser numéricos."
        }, 400)

    fecha_prediccion = datetime.now().isoformat(timespec="seconds")

    registro = {
        "estado": estado,
        "valores_recibidos": valores,
        "fecha_prediccion": fecha_prediccion
    }

    guardar_prediccion(registro)

    return responder_json({
        "estado": estado,
        "valores_recibidos": valores,
        "fecha_prediccion": fecha_prediccion,
        "nota": "Resultado simulado para fines académicos. No corresponde a diagnóstico médico real."
    })


@app.route("/reporte", methods=["GET"])
def reporte():
    predicciones = leer_predicciones()

    conteo = Counter(prediccion["estado"] for prediccion in predicciones)

    totales_por_categoria = {
        categoria: conteo.get(categoria, 0)
        for categoria in CATEGORIAS
    }

    ultimas_5 = predicciones[-5:]

    fecha_ultima_prediccion = None
    if predicciones:
        fecha_ultima_prediccion = predicciones[-1]["fecha_prediccion"]

    return responder_json({
        "total_predicciones": len(predicciones),
        "totales_por_categoria": totales_por_categoria,
        "ultimas_5_predicciones": ultimas_5,
        "fecha_ultima_prediccion": fecha_ultima_prediccion
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
