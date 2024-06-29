# admin_api.py

from fastapi import APIRouter, Path, Body
import logging
import requests
from dotenv import load_dotenv
import os


# --------------------------------------------------------------
# Set up logging
# --------------------------------------------------------------
logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

# --------------------------------------------------------------
# Load environment variables
# --------------------------------------------------------------
load_dotenv()
BOT_URL = os.getenv("BOT_URL")

# --------------------------------------------------------------
# Router
# --------------------------------------------------------------

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.post("/simulate_whatsapp_message/{phone_number}")
async def simulate_whatsapp_message(phone_number: str = Path(..., description="The recipient's phone number"),
                                    message: str = Body(..., embed=True,
                                                        description="The message to simulate")):
    logger.info(
        f'Simulating WhatsApp message for phone number: {phone_number} with message: {message}')

    simulated_payload = {
        'object': 'whatsapp_business_account',
        'entry': [{
            'id': '123456',
            'changes': [{
                'value': {
                    'messaging_product': 'whatsapp',
                    'metadata': {
                        'display_phone_number': '123456789',
                        'phone_number_id': '1234567890'
                    },
                    'contacts': [{
                        'profile': {'name': 'Test User'},
                        'wa_id': phone_number
                    }],
                    'messages': [{
                        'from': phone_number,
                        'id': 'wamid.test',
                        'timestamp': '1629387287',
                        'text': {'body': message},
                        'type': 'text'
                    }]
                },
                'field': 'messages'
            }]
        }]
    }

    webhook_url = f"{BOT_URL}/webhook"
    logger.info(
        f"Sending POST request to {webhook_url} with payload: {simulated_payload}")

    try:
        response = requests.post(
            webhook_url, json=simulated_payload, timeout=(5, 10))
        response.raise_for_status()
        logger.info("Simulated message successfully sent to webhook.")
        return {"status": "success", "message": "Simulated message sent to webhook."}
    except requests.exceptions.Timeout:
        logger.error(
            "Timeout occurred while sending simulated message to webhook.")
        return {"status": "failure", "message": "Timeout occurred while sending simulated message to webhook."}
    except requests.exceptions.RequestException as e:
        logger.error(
            f"Failed to send simulated message to webhook. Error: {e}")
        return {"status": "failure", "message": f"Failed to send simulated message to webhook. Error: {e}"}
