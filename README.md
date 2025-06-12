# 🤖 Asistente de Vacantes Google con OpenAI y GCP

Este proyecto es un chatbot personalizado construido con **OpenAI Assistants API**, desplegado en **Google Cloud Run**, que permite responder preguntas sobre vacantes de Google. Además, ofrece la funcionalidad de **registrar candidatos interesados en una hoja de cálculo de Google Sheets**.

## 🧠 Características

- Utiliza **GPT-4 Turbo** como modelo base.
- Puede responder preguntas sobre vacantes definidas en un archivo `positions.txt`.
- Integra una función personalizada: `register_applicant_to_sheets`.
- Desplegado en **Cloud Run** usando **Artifact Registry** y **Cloud Build**.
- Carga e indexa contenido como vector store (RAG) para respuestas más inteligentes.

## 📁 Estructura del proyecto
.
├── src/
│ ├── app.py # Aplicación principal (Streamlit)
│ ├── create_assistant.py # Crea o actualiza el Assistant de OpenAI
│ ├── upload_positions.py # Carga el archivo de vacantes y lo asocia al Assistant
│ ├── utils.py # Lógica auxiliar (ej. ejecución de funciones)
│ └── positions.txt # Descripción de vacantes
├── .devcontainer/ # Configuración para entorno remoto en VSCode
├── cloudbuild.yaml # Instrucciones para construir imagen en GCP
├── service.yaml # Configuración del servicio de Cloud Run
├── gcr-service-policy.yaml # Política para hacer el servicio público
├── requirements.txt # Dependencias del proyecto
└── README.md

## ⚙️ Requisitos

- Python 3.9+
- Cuenta de OpenAI con acceso a Assistants API
- Proyecto en Google Cloud Platform con:
  - Artifact Registry
  - Cloud Build
  - Cloud Run habilitado
- Habilitar APIs de Google Sheets si se desea registrar usuarios

## 🧪 Variables de entorno requeridas (.env)

> ⚠️ **Este archivo no debe subirse al repositorio (`.gitignore`)**

```env
OPENAI_API_KEY=sk-...
ASSISTANT_ID=asst_...
GOOGLE_SHEETS_ID=...
```

## 📌 Notas finales
El proyecto puede mantenerse activo sin necesidad de reconstrucción mientras la URL pública esté activa.

Si se modifica el código, es necesario re-hacer el build y redeploy.

Si se modifica el contenido del Assistant (tools o vector store), debes correr de nuevo create_assistant.py o upload_positions.py.

Desarrollado por [Carlos Sánchez] 💼
