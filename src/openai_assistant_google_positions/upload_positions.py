# src/openai_assistant_google_positions/upload_positions.py

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

client = OpenAI(api_key=OPENAI_API_KEY)

# Path to file
file_path = "src/positions.txt"

# Create vector store
print("🧠 Creating vector store...")
vector_store = client.vector_stores.create(name="Google Positions Store")

# Upload file to vector store (directly from file path)
print(f"📤 Uploading file to vector store: {file_path}")
with open(file_path, "rb") as f:
    client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id,
        files=[f]
    )

print(f"✅ File uploaded to vector store: {vector_store.id}")

# Update assistant
print("🔗 Updating assistant with vector store...")
assistant = client.beta.assistants.update(
    assistant_id=ASSISTANT_ID,
    tool_resources={
        "file_search": {
            "vector_store_ids": [vector_store.id]
        }
    }
)
print("✅ Assistant updated with vector store!")
