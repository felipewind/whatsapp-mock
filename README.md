# whatsapp-mock
Mock of WhatsApp APIs and Webhooks

Starting the WhatsApp mock

fastapi dev main.py --reload --port 8010


Calling the application webhook
```
curl -X POST "http://localhost:8010/send-message/" -H "Content-Type: application/json" -d '{"text": "Hello, this is a test message.", "profile_name": "NAME"}'
```