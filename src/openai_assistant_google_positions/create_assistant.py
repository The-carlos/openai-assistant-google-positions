# src/openai_assistant_google_positions/create_assistant.py

import openai
from dotenv import load_dotenv
import os

ENV_PATH = ".env"
ASSISTANT_NAME = "Asistente Google Positions"

# Leer las vacantes desde el archivo y agregarlas al contexto del assistant
POSITIONS_FILE_PATH = "src/positions.txt"
with open(POSITIONS_FILE_PATH, "r", encoding="utf-8") as f:
    positions_text = f.read()


INSTRUCTIONS = (
    "Eres un asistente personalizado creado por Carlos Sánchez. "
    "Siempre comienza presentandote como un asistente programado por Carlos. "
    "Tu función es responder preguntas sobre una vacante de Google proporcionada como archivo. Debes responder preguntas sobre las posiciones diponibles en Google"
    "Estas son las posiciones disponibles:\n\n"
    + positions_text +
    "\n\nResponde las preguntas de los usuarios basándote en esta información."
)


# Cargar variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

def update_env_variable(key, value, path=ENV_PATH):
    """Sobrescribe o agrega una variable al archivo .env"""
    lines = []
    found = False

    # Leer líneas existentes
    if os.path.exists(path):
        with open(path, "r") as f:
            lines = f.readlines()

    # Modificar si ya existe
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            found = True
            break

    # Agregar si no existe
    if not found:
        lines.append(f"{key}={value}\n")

    # Guardar archivo
    with open(path, "w") as f:
        f.writelines(lines)


if assistant_id:
    print("🔁 Assistant ID found in .env, updating assistant...")

    updated = openai.beta.assistants.update(
        assistant_id=assistant_id,
        instructions=INSTRUCTIONS,
        tools=[
    {
        "type": "function",
        "function": {
            "name": "register_applicant_to_sheets",
            "description": "Register an applicant in a Google Sheet for job follow-up.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Applicant's full name"
                    },
                    "email": {
                        "type": "string",
                        "description": "Applicant's email address"
                    },
                    "interest": {
                        "type": "string",
                        "description": "Job position or field of interest"
                    }
                },
                "required": ["name", "email", "interest"]
            }
        }
    }
],
        name=ASSISTANT_NAME
    )

    print("✅ Assistant updated:", updated.id)

else:
    print("🆕 No ASSISTANT_ID found. Creating new assistant...")

    assistant = openai.beta.assistants.create(
        name=ASSISTANT_NAME,
        instructions=INSTRUCTIONS,
        model="gpt-4-turbo",
        tools=[
    {
        "type": "function",
        "function": {
            "name": "register_applicant_to_sheets",
            "description": "Register an applicant in a Google Sheet for job follow-up.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Applicant's full name"
                    },
                    "email": {
                        "type": "string",
                        "description": "Applicant's email address"
                    },
                    "interest": {
                        "type": "string",
                        "description": "Job position or field of interest"
                    }
                },
                "required": ["name", "email", "interest"]
            }
        }
    }
]
    )

    print("✅ Assistant created:", assistant.id)

    # Guardar nuevo ID en .env
    update_env_variable("ASSISTANT_ID", assistant.id)
    print("💾 Saved ASSISTANT_ID to .env")
