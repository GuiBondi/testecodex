"""Scoring services for leads."""
import pickle
from typing import Any, Dict

from ..models.lead_models import LeadValidated
from .llm_router import call_gemini

_model_cache: Any = None


def load_model() -> Any:
    """Load decision tree model from disk."""
    global _model_cache
    if _model_cache is None:
        with open("model.pkl", "rb") as f:
            _model_cache = pickle.load(f)
    return _model_cache


def calculate_score(lead: LeadValidated) -> float:
    """Calculate probability score for lead."""
    perfil_map = {"Alto": 3, "Médio": 2, "Baixo": 1, "Desconhecido": 0}
    perfil_code = perfil_map.get(lead.perfil_socioeconomico or "Desconhecido", 0)
    features = [[lead.renda_informada, perfil_code, lead.valor_venal_estimado or 0.0]]
    model = load_model()
    proba = model.predict_proba(features)[0][1]
    return float(proba)


def determine_mcmv(score: float) -> bool:
    """Determine if lead qualifies for MCMV based on score."""
    return score >= 0.6


def generate_indicators(lead: LeadValidated, score: float) -> Dict[str, str]:
    """Generate explanation using LLM."""
    prompt = (
        f"Nome: {lead.nome}\n"
        f"Renda: {lead.renda_informada}\n"
        f"Perfil: {lead.perfil_socioeconomico}\n"
        f"Valor venal: {lead.valor_venal_estimado}\n"
        f"CPF válido: {lead.cpf_valido}\n"
        f"Telefone válido: {lead.telefone_valido}\n"
        f"Endereço válido: {lead.endereco_valido}\n"
        f"Score: {score:.2f}\n"
        "Explique em até 60 palavras os pontos fortes e fracos deste lead para o programa Minha Casa Minha Vida."
    )
    texto = call_gemini(prompt)
    return {"explicacao_llm": texto}
