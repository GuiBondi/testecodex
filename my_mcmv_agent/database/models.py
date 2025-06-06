"""SQLAlchemy ORM models for persisting leads and scores."""
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship

from .session import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    cep = Column(String, nullable=False)
    renda_informada = Column(Float, nullable=False)
    logradouro = Column(String)
    bairro = Column(String)
    cidade = Column(String)
    uf = Column(String)
    perfil_socioeconomico = Column(String)
    valor_venal_estimado = Column(Float)
    cpf_valido = Column(Boolean, nullable=False)
    telefone_valido = Column(Boolean, nullable=False)
    endereco_valido = Column(Boolean, nullable=False)

    scores = relationship("Score", back_populates="lead")


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    score = Column(Float, nullable=False)
    valido_para_mcmv = Column(Boolean, nullable=False)
    indicadores = Column(JSON)

    lead = relationship("Lead", back_populates="scores")
