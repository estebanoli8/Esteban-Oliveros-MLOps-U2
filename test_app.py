import os

import pytest

from app import app, clasificar_estado, ARCHIVO_PREDICCIONES


@pytest.fixture
def client(tmp_path, monkeypatch):
    archivo_temporal = tmp_path / "predicciones_test.jsonl"

    monkeypatch.setattr("app.ARCHIVO_PREDICCIONES", archivo_temporal)

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_modelo_retorna_las_cinco_categorias():
    casos = [
        ([36.7, 1, 1], "NO ENFERMO"),
        ([37.8, 4, 3], "ENFERMEDAD LEVE"),
        ([39.2, 8, 5], "ENFERMEDAD AGUDA"),
        ([37.8, 5, 45], "ENFERMEDAD CRÓNICA"),
        ([40.2, 9, 100], "ENFERMEDAD TERMINAL"),
    ]

    for valores, estado_esperado in casos:
        assert clasificar_estado(valores) == estado_esperado


def test_reporte_inicial_y_ultima_prediccion(client):
    reporte_inicial = client.get("/reporte")
    datos_iniciales = reporte_inicial.get_json()

    assert reporte_inicial.status_code == 200
    assert datos_iniciales["total_predicciones"] == 0
    assert datos_iniciales["fecha_ultima_prediccion"] is None

    prediccion = client.post(
        "/predecir",
        json={"valores": [40.2, 9, 100]},
    )

    datos_prediccion = prediccion.get_json()

    assert prediccion.status_code == 200
    assert datos_prediccion["estado"] == "ENFERMEDAD TERMINAL"

    reporte_final = client.get("/reporte")
    datos_reporte = reporte_final.get_json()

    assert datos_reporte["total_predicciones"] == 1
    assert datos_reporte["totales_por_categoria"]["ENFERMEDAD TERMINAL"] == 1
    assert datos_reporte["ultimas_5_predicciones"][-1]["estado"] == "ENFERMEDAD TERMINAL"
    assert datos_reporte["fecha_ultima_prediccion"] is not None
