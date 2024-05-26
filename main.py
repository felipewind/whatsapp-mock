# main.py (mock project)
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests
import hmac
import hashlib
import json
import time

# --------------------------------------------------------------
# Load environment variables
# --------------------------------------------------------------
load_dotenv()
BOT_URL = os.getenv("BOT_URL")
APP_SECRET = os.getenv("APP_SECRET")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")


# --------------------------------------------------------------
# FastAPI App
# --------------------------------------------------------------
app = FastAPI()

# --------------------------------------------------------------
# Models
# --------------------------------------------------------------
class Message(BaseModel):
    messaging_product: str
    to: str
    type: str
    text: dict = None
    template: dict = None

class SendMessage(BaseModel):
    text: str
    profile_name: str

# --------------------------------------------------------------
# Helper Functions
# --------------------------------------------------------------
def generate_signature(secret: str, payload: bytes) -> str:
    mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256)
    return f"sha256={mac.hexdigest()}"

# --------------------------------------------------------------
# Endpoints
# --------------------------------------------------------------
@app.post("/{version}/{phone_number_id}/messages")
async def handle_messages(version: str, phone_number_id: str, message: Message, request: Request):
    if version != VERSION or phone_number_id != PHONE_NUMBER_ID:
        raise HTTPException(status_code=400, detail="Invalid version or phone number ID")
    
    # Log the incoming request
    request_body = await request.json()
    print(f"Received message: {request_body}")

    # Respond with a mock response
    return {
        "messages": [
            {
                "id": "gBEGkYiEB1VXAglK1ZEqA1YKPrU",
                "timestamp": "1618508490",
                "status": "sent",
                "recipient_id": RECIPIENT_WAID
            }
        ]
    }

@app.post("/send-message/")
def send_message_to_bot(message: SendMessage):
    # Get the current time in seconds since the epoch
    current_timestamp = int(time.time())
    # Prepare the data in the format expected by the bot's endpoint
    bot_data = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": RECIPIENT_WAID,
                                "phone_number_id": PHONE_NUMBER_ID
                            },
                            "contacts": [
                                {
                                    "profile": {
                                        "name": message.profile_name
                                    },
                                    "wa_id": RECIPIENT_WAID
                                }
                            ],
                            "messages": [
                                {
                                    "from": RECIPIENT_WAID,
                                    "id": "wamid.ID",
                                    "timestamp": current_timestamp,
                                    "text": {
                                        "body": message.text
                                    },
                                    "type": "text"
                                }
                            ]
                        },
                        "field": "messages"
                    }
                ]
            }
        ]
    }
    payload = bytes(json.dumps(bot_data), 'utf-8')
    signature = generate_signature(APP_SECRET, payload)

    # Send the data to the bot's webhook endpoint
    url = f"{BOT_URL}/webhook"
    headers = {
        "Content-Type": "application/json",
        "X-Hub-Signature-256": signature
    }
    response = requests.post(url, data=payload, headers=headers, verify=False)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

# --------------------------------------------------------------
# Run the FastAPI app
# --------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
