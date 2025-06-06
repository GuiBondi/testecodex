"""Pydantic model representing scoring results."""
from pydantic import BaseModel
from typing import Dict, Any


class ScoreResult(BaseModel):
    """Output returned after processing a lead."""

    lead_id: int
    score: float
    valido_para_mcmv: bool
    indicadores: Dict[str, Any]
