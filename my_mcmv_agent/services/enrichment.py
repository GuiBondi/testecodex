"""Data enrichment services calling external APIs."""
from typing import Dict, Any
import requests

from ..utils.config import VIA_CEP_API_URL, DEMO_API_URL


def crawl_address(cep: str) -> Dict[str, Any]:
    """Fetch address data from ViaCEP."""
    try:
        resp = requests.get(f"{VIA_CEP_API_URL}/{cep}/json/", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return {
            "logradouro": data.get("logradouro"),
            "bairro": data.get("bairro"),
            "cidade": data.get("localidade"),
            "uf": data.get("uf"),
        }
    except Exception:
        return {"logradouro": None, "bairro": None, "cidade": None, "uf": None}


def fetch_demographic_profile(cep: str) -> Dict[str, Any]:
    """Fetch demographic profile from external API."""
    try:
        resp = requests.get(f"{DEMO_API_URL}?cep={cep}", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return {
            "perfil_socioeconomico": data.get("perfil_socioeconomico", "Desconhecido"),
            "valor_venal_estimado": float(data.get("valor_venal_estimado", 0.0)),
        }
    except Exception:
        return {"perfil_socioeconomico": "Desconhecido", "valor_venal_estimado": 0.0}
