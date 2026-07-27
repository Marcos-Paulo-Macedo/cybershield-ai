import os
from typing import List, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

class EstruturaAtaque(BaseModel):
    vetor: str = Field(description="Vetor de ataque empregado")
    canal: str = Field(description="Canal de comunicação utilizado")
    gatilho: str = Field(description="Gatilho comportamental explorado")

class DiagnosticoFraude(BaseModel):
    nome_incidente: str = Field(description="Nome técnico/popular do golpe")
    resumo_tecnico: str = Field(description="Descrição objetiva do evento")
    nivel_complexidade: int = Field(description="Nível de sofisticação de 1 a 10")
    detalhes: EstruturaAtaque
    medidas_preventivas: List[str] = Field(description="Ações para prevenção")
    protocolo_emergencia: List[str] = Field(description="Procedimentos de contenção")

class ProcessadorOcorrencia:
    def __init__(self, api_key: Optional[str] = None):
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError("Chave de API não localizada.")
        self.client = genai.Client(api_key=key)
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    def analisar_relato(self, relato: str, idioma: str = "pt") -> DiagnosticoFraude:
        mapeamento_idiomas = {
            "pt": "Português",
            "en": "Inglês (English)",
            "es": "Espanhol (Español)"
        }
        idioma_nome = mapeamento_idiomas.get(idioma, "Português")

        prompt = f"""
        Analise a ocorrência descrita abaixo sob a ótica de segurança da informação e prevenção a fraudes:

        "{relato}"

        REQUISITO OBRIGATÓRIO: Toda a resposta (incluindo nomes, descrições e listas) DEVE ser escrita estritamente no idioma: {idioma_nome}.

        Classifique o tipo de evento, extraia o vetor e canal utilizado, e liste os passos de contenção imediata e prevenção.
        """

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=DiagnosticoFraude,
                temperature=0.1,
            )
        )
        return DiagnosticoFraude.model_validate_json(response.text)