# Servicio Docker para clasificación médica simulada

## Finalidad

Este proyecto contiene un servicio sencillo en Python y Flask para simular el uso de un modelo de machine learning en el contexto de enfermedades comunes y enfermedades huérfanas.

El servicio recibe una lista con tres valores ingresados por el médico:

```text
[temperatura, nivel_dolor, dias_sintomas]
```

Con esos datos retorna uno de los siguientes estados:

- NO ENFERMO
- ENFERMEDAD LEVE
- ENFERMEDAD AGUDA
- ENFERMEDAD CRÓNICA

El modelo es una función simulada. No corresponde a un diagnóstico médico real.

## Estructura del directorio

```text
punto2_docker_simple/
├── app.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## Descripción de archivos

- `app.py`: contiene la aplicación Flask, el punto final `/predecir` y la función simulada `predecir_estado`.
- `requirements.txt`: contiene la dependencia necesaria para ejecutar la aplicación.
- `Dockerfile`: contiene las instrucciones para construir la imagen Docker.
- `README.md`: contiene las instrucciones de uso.

## Construir la imagen Docker

Desde la carpeta del proyecto, ejecutar:

```bash
docker build -t clasificador-medico-simple:1.0 .
```

## Correr el contenedor

Ejecutar:

```bash
docker run -p 5000:5000 clasificador-medico-simple:1.0
```

El servicio quedará disponible en:

```text
http://localhost:5000
```

## Obtener una respuesta del modelo

El médico debe enviar una solicitud `POST` al punto final:

```text
http://localhost:5000/predecir
```

El cuerpo de la solicitud debe tener la siguiente forma:

```json
{
  "valores": [37.8, 4, 3]
}
```

Donde:

1. `37.8` representa la temperatura corporal.
2. `4` representa el nivel de dolor en una escala de 0 a 10.
3. `3` representa los días con síntomas.

## Ejemplos de uso con curl

### 1. NO ENFERMO

```bash
curl -X POST http://localhost:5000/predecir \
  -H "Content-Type: application/json" \
  -d '{"valores": [36.5, 1, 1]}'
```

### 2. ENFERMEDAD LEVE

```bash
curl -X POST http://localhost:5000/predecir \
  -H "Content-Type: application/json" \
  -d '{"valores": [37.8, 4, 3]}'
```

### 3. ENFERMEDAD AGUDA

```bash
curl -X POST http://localhost:5000/predecir \
  -H "Content-Type: application/json" \
  -d '{"valores": [39.2, 8, 5]}'
```

### 4. ENFERMEDAD CRÓNICA

```bash
curl -X POST http://localhost:5000/predecir \
  -H "Content-Type: application/json" \
  -d '{"valores": [37.8, 5, 45]}'
```

## Respuesta esperada

El servicio responde en formato JSON. Ejemplo:

```json
{
  "estado": "ENFERMEDAD LEVE",
  "nota": "Modelo simulado con fines académicos. No corresponde a diagnóstico médico real.",
  "valores_recibidos": [37.8, 4, 3]
}
```

## Detener el contenedor

Para detener el contenedor, presionar `CTRL + C` en la terminal donde está corriendo.
