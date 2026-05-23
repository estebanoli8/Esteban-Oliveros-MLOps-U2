from flask import Flask, request, Response
import json

app = Flask(__name__)

def clasificar_estado(valores):
    """
    Función simulada que recibe una lista con tres valores:
    [temperatura, nivel_dolor, dias_sintomas]
    """

    temperatura = float(valores[0])
    nivel_dolor = float(valores[1])
    dias_sintomas = float(valores[2])

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


@app.route("/", methods=["GET"])
def inicio():
    return responder_json({
        "mensaje": "Servicio de clasificación médica simulado activo",
        "endpoint": "/predecir",
        "formato_entrada": {
            "valores": ["temperatura", "nivel_dolor", "dias_sintomas"]
        }
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

    return responder_json({
        "estado": estado,
        "valores_recibidos": valores,
        "nota": "Resultado simulado para fines académicos. No corresponde a diagnóstico médico real."
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
