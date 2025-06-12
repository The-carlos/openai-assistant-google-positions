from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
assistant_id = os.getenv("ASSISTANT_ID")

# Crear nuevo thread
thread = client.beta.threads.create()

# Enviar mensaje al assistant
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="¿Cuáles son los requisitos para la vacante de Data Engineer?"
)

# Ejecutar assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id
)

# Esperar a que termine (polling)
import time
while True:
    run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    if run_status.status in ["completed", "failed"]:
        break
    time.sleep(1)

# Leer la respuesta
messages = client.beta.threads.messages.list(thread_id=thread.id)
for msg in messages.data:
    print(f"{msg.role.upper()}: {msg.content[0].text.value}")
