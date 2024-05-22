# main.py (mock project)
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests

# --------------------------------------------------------------
# Load environment variables
# --------------------------------------------------------------
load_dotenv()
WHATSAPP_URL = os.getenv("WHATSAPP_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")
BOT_URL = os.getenv("BOT_URL")

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

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
    recipient: str
    text: str

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
    # Prepare the data in the format expected by the bot's endpoint
    bot_data = {
        "object": "whatsapp",
        "entry": [
            {
                "id": "entry_id",
                "changes": [
                    {
                        "value": {
                            "messages": [
                                {
                                    "from": message.recipient,
                                    "text": {
                                        "body": message.text
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }

    # Send the data to the bot's webhook endpoint
    url = f"{BOT_URL}/webhook"
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=bot_data, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

# --------------------------------------------------------------
# Run the FastAPI app
# --------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
