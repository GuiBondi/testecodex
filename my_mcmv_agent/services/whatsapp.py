"""Send and receive WhatsApp messages using Twilio and Gemini."""
from twilio.rest import Client

from ..utils.config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_WHATSAPP_FROM,
)
from .llm_router import call_gemini
from ..models.lead_models import LeadValidated

_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_whatsapp_message(to: str, body: str) -> str:
    """Send a WhatsApp message and return Twilio message SID."""
    message = _client.messages.create(
        body=body,
        from_=f"whatsapp:{TWILIO_WHATSAPP_FROM}",
        to=f"whatsapp:{to}",
    )
    return message.sid


def reply_with_gemini(lead: LeadValidated, incoming_message: str) -> str:
    """Generate a reply using Gemini and send via WhatsApp."""
    prompt = (
        f"Mensagem do lead: {incoming_message}\n"
        f"Nome: {lead.nome}\n"
        f"Renda: {lead.renda_informada}\n"
        f"Perfil: {lead.perfil_socioeconomico}\n"
        "Responda de forma cordial ao lead sobre o programa Minha Casa Minha Vida."
    )
    resposta = call_gemini(prompt)
    send_whatsapp_message(lead.telefone, resposta)
    return resposta
