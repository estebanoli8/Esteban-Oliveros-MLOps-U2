# Esteban-Oliveros-MLOps-U2

## Problema

En medicina existe una gran cantidad de información clínica de pacientes. Sin embargo, para algunas enfermedades poco comunes, conocidas como enfermedades huérfanas, los datos disponibles son escasos.

Este repositorio contiene una solución académica simplificada para simular un servicio de predicción médica usando MLOps, Python, Flask, Docker y GitHub.

## Propósito de la solución

El propósito es exponer un servicio web que recibe tres datos básicos del paciente y retorna una categoría simulada de estado de salud.

La solución no corresponde a un modelo médico real. Es una simulación académica para practicar despliegue, control de versiones, ramas, commits, pull requests y Docker.

## Estructura del repositorio

- app.py: contiene la aplicación Flask, la función simulada de clasificación, el endpoint /predecir y el endpoint /reporte.
- requirements.txt: contiene la dependencia principal del proyecto: Flask.
- Dockerfile: contiene las instrucciones para construir la imagen Docker.
- README.md: contiene la explicación del proyecto y las instrucciones de uso.

## Categorías de predicción

El servicio puede retornar cinco categorías:

- NO ENFERMO
- ENFERMEDAD LEVE
- ENFERMEDAD AGUDA
- ENFERMEDAD CRÓNICA
- ENFERMEDAD TERMINAL

## Entrada del modelo simulado

El médico debe enviar una lista con tres valores:

[temperatura, nivel_dolor, dias_sintomas]

Ejemplo de entrada JSON:

{
  "valores": [37.8, 4, 3]
}

## Construir la imagen Docker

Desde la carpeta del repositorio, ejecutar:

docker build -t clasificador-medico-simple:2.0 .

## Correr el contenedor

Ejecutar:

docker run --rm -p 5001:5000 clasificador-medico-simple:2.0

El servicio queda disponible en:

http://localhost:5001

## Endpoint de predicción

URL:

POST http://localhost:5001/predecir

Ejemplo:

curl -X POST http://localhost:5001/predecir \
  -H "Content-Type: application/json" \
  -d '{"valores": [37.8, 4, 3]}'

## Endpoint de reporte

URL:

GET http://localhost:5001/reporte

Ejemplo:

curl http://localhost:5001/reporte

El reporte retorna:

- número total de predicciones realizadas;
- número de predicciones realizadas por cada categoría;
- últimas 5 predicciones realizadas;
- fecha de la última predicción.

## Flujo de versionamiento usado

El repositorio fue construido mediante ramas, commits y pull requests:

- main: README inicial del proyecto.
- solución-inicial: incorporación inicial de app.py, requirements.txt, Dockerfile y actualización del README.md.
- PR #1: integración de solución-inicial a main.
- segunda-versión: incorporación de ENFERMEDAD TERMINAL y endpoint /reporte.
- PR #2: integración de segunda-versión a main.

## Conceptos MLOps aplicados

- Versionamiento de código con Git y GitHub.
- Uso de ramas para separar cambios.
- Pull requests para integrar nuevas versiones.
- Dockerfile para construir una imagen reproducible.
- Contenedor Docker para ejecutar el servicio.
- Endpoint /predecir para consumir el modelo simulado.
- Endpoint /reporte para observabilidad básica de las predicciones.
- README como documentación central del proyecto.

## Nota académica

Este proyecto es una simulación académica.

No debe usarse para diagnóstico clínico real.

## Pipeline CI/CD con GitHub Actions

La solución incluye un workflow de GitHub Actions definido en:

.github/workflows/ci-cd.yml

Este pipeline automatiza tareas de integración continua y despliegue continuo para la solución.

### Evento pull_request hacia main

Cuando se crea un pull request contra la rama main, el pipeline realiza las siguientes tareas:

- comenta automáticamente en el PR: "CI/CD en acción. Ejecutando tareas …";
- descarga el código del repositorio;
- configura Python;
- instala las dependencias;
- ejecuta pruebas unitarias con pytest;
- comenta automáticamente en el PR: "CI/CD terminado con éxito."

### Evento push hacia main

Cuando los cambios llegan a la rama main, el pipeline realiza las siguientes tareas:

- descarga el código del repositorio;
- configura Python;
- instala las dependencias;
- ejecuta nuevamente las pruebas unitarias;
- inicia sesión en GitHub Container Registry;
- construye la imagen Docker;
- publica la imagen en GitHub Packages.

### Pruebas unitarias

Las pruebas unitarias están definidas en el archivo:

test_app.py

Estas pruebas verifican:

- que el modelo simulado pueda retornar las cinco categorías;
- que el endpoint /reporte funcione correctamente después de una predicción.

### Imagen publicada

La imagen Docker publicada por el pipeline puede descargarse desde GitHub Container Registry con:

docker pull ghcr.io/estebanoli8/clasificador-medico-simple:latest

