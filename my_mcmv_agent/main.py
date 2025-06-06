"""Main application for processing leads."""
import json
from typing import Dict

from .database.session import SessionLocal, engine, Base
from .database.models import Lead, Score
from .models.lead_models import LeadBase, LeadEnriched, LeadValidated
from .models.score_models import ScoreResult
from .services.enrichment import crawl_address, fetch_demographic_profile
from .services.validation import validate_cpf, validate_phone
from .services.scoring import calculate_score, determine_mcmv, generate_indicators
from .services.whatsapp import reply_with_gemini


# Initialize database
Base.metadata.create_all(bind=engine)
print("Banco de dados inicializado.")


def process_lead(input_json: Dict) -> Dict:
    """Process a lead through all stages and persist results."""
    lead_base = LeadBase.parse_obj(input_json)
    address = crawl_address(lead_base.cep)
    profile = fetch_demographic_profile(lead_base.cep)
    lead_enriched = LeadEnriched(**lead_base.dict(), **address, **profile)

    cpf_ok = validate_cpf(lead_enriched.cpf)
    phone_ok = validate_phone(lead_enriched.telefone)
    endereco_ok = all(
        [lead_enriched.logradouro, lead_enriched.bairro, lead_enriched.cidade, lead_enriched.uf]
    )

    lead_validated = LeadValidated(
        **lead_enriched.dict(),
        cpf_valido=cpf_ok,
        telefone_valido=phone_ok,
        endereco_valido=endereco_ok,
    )

    db = SessionLocal()
    try:
        db_lead = Lead(**lead_validated.dict())
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)

        score_value = calculate_score(lead_validated)
        is_valid = determine_mcmv(score_value)
        indicadores = generate_indicators(lead_validated, score_value)

        db_score = Score(
            lead_id=db_lead.id,
            score=score_value,
            valido_para_mcmv=is_valid,
            indicadores=indicadores,
        )
        db.add(db_score)
        db.commit()
        db.refresh(db_score)
    finally:
        db.close()

    result = ScoreResult(
        lead_id=db_lead.id,
        score=score_value,
        valido_para_mcmv=is_valid,
        indicadores=indicadores,
    )
    return result.dict()


if __name__ == "__main__":
    exemplo = {
        "nome": "Mariana Oliveira",
        "telefone": "+5511988887777",
        "cpf": "12345678909",
        "cep": "01001000",
        "renda_informada": 2800.00,
    }
    resultado = process_lead(exemplo)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))

    # Example of replying to the lead via WhatsApp using Gemini
    db = SessionLocal()
    try:
        db_lead = db.query(Lead).get(resultado["lead_id"])
        if db_lead:
            lead_data = {
                k: getattr(db_lead, k)
                for k in [
                    "nome",
                    "telefone",
                    "cpf",
                    "cep",
                    "renda_informada",
                    "logradouro",
                    "bairro",
                    "cidade",
                    "uf",
                    "perfil_socioeconomico",
                    "valor_venal_estimado",
                    "cpf_valido",
                    "telefone_valido",
                    "endereco_valido",
                ]
            }
            lead_validated = LeadValidated(**lead_data)
            reply_with_gemini(lead_validated, "Olá, posso participar do programa?")
    finally:
        db.close()
