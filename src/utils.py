# utils.py

import pandas as pd
import pygsheets
import os
import json
from time import sleep
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read credentials from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID")
SERVICE_ACCOUNT_PATH = 'src/project-openai-gcp-positions-01fd668408b0.json'  # You should store your JSON key here

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


# --------------------------------------------------------------------------------------------------
# Register an interested applicant into a Google Sheet
# --------------------------------------------------------------------------------------------------

def register_applicant_to_sheets(name: str, email: str, interest: str) -> bool:
    """
    Appends a new row to a Google Sheets document with applicant info.

    Parameters:
        name (str): Applicant's name.
        email (str): Applicant's email address.
        interest (str): Position or program of interest.

    Returns:
        bool: True if the registration was successful, False otherwise.
    """
    try:
        # Connect to Google Sheets via service account
        gc = pygsheets.authorize(service_file=SERVICE_ACCOUNT_PATH)
        sheet_url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEETS_ID}/edit"
        sh = gc.open_by_url(sheet_url)
        wks = sh[0]

        # Load existing data and append new entry
        df = wks.get_as_df()
        new_entry = {"id": len(df) + 1, "name": name, "email": email, "interest": interest}
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)

        # Save updated DataFrame to Google Sheets
        wks.set_dataframe(df, (1, 1))
        return True

    except Exception as e:
        print(f"[ERROR] Failed to register applicant: {e}")
        return False


# --------------------------------------------------------------------------------------------------
# Wait and handle tool calls (function executions) from the Assistant
# --------------------------------------------------------------------------------------------------

def run_executor(run):
    """
    Polls OpenAI's API until the run is complete, and handles any tool calls requested.

    Parameters:
        run: The OpenAI Assistant run object.

    Returns:
        None
    """
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=run.thread_id,
            run_id=run.id
        )

        if run_status.status == "completed":
            print("[INFO] Run completed.")
            break

        elif run_status.status == "requires_action":
            print("[INFO] Assistant requested tool execution.")

            actions = run_status.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []

            for action in actions:
                function_name = action.function.name
                arguments = json.loads(action.function.arguments)

                if function_name == "register_applicant_to_sheets":
                    success = register_applicant_to_sheets(
                        arguments["name"],
                        arguments["email"],
                        arguments["interest"]
                    )
                    tool_outputs.append({
                        "tool_call_id": action.id,
                        "output": str(success)
                    })

                else:
                    print(f"[WARNING] Unknown function requested: {function_name}")

            client.beta.threads.runs.submit_tool_outputs(
                thread_id=run.thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        else:
            print("[INFO] Waiting for assistant...")
            sleep(1)
