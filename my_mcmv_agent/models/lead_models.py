"""Pydantic models representing lead data at various stages."""
from pydantic import BaseModel, validator, Field
from typing import Optional
import re


class LeadBase(BaseModel):
    """Base fields received from users."""

    nome: str
    telefone: str
    cpf: str
    cep: str
    renda_informada: float = Field(..., ge=0)

    @validator("cpf")
    def cpf_digits(cls, v: str) -> str:
        if not (v.isdigit() and len(v) == 11):
            raise ValueError("CPF deve conter 11 dígitos numéricos")
        return v

    @validator("telefone")
    def telefone_digits(cls, v: str) -> str:
        digits = re.sub(r"\D", "", v)
        if not (10 <= len(digits) <= 13):
            raise ValueError("Telefone deve conter entre 10 e 13 dígitos")
        return digits


class LeadEnriched(LeadBase):
    """Lead after enrichment with address and demographic data."""

    logradouro: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    perfil_socioeconomico: Optional[str] = None
    valor_venal_estimado: Optional[float] = None


class LeadValidated(LeadEnriched):
    """Lead with validation flags."""

    cpf_valido: bool
    telefone_valido: bool
    endereco_valido: bool
