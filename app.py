import os
import tempfile
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from threat_analyzer import ProcessadorOcorrencia, DiagnosticoFraude
from pdf_generator import GeradorRelatorio

load_dotenv()

app = FastAPI(title="WikiFraudes API")

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

processador = ProcessadorOcorrencia()
gerador_pdf = GeradorRelatorio()

cache_ocorrencia: Optional[DiagnosticoFraude] = None

class EntradaRelato(BaseModel):
    texto: str
    idioma: str = "pt"

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.post("/api/analisar")
def analisar(payload: EntradaRelato):
    global cache_ocorrencia
    if not payload.texto or len(payload.texto.strip()) < 10:
        raise HTTPException(status_code=400, detail="Relato muito curto para análise.")
    
    try:
        resultado = processador.analisar_relato(payload.texto, payload.idioma)
        cache_ocorrencia = resultado
        return resultado.model_dump()
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

@app.get("/api/exportar-pdf")
def exportar_pdf():
    global cache_ocorrencia
    if not cache_ocorrencia:
        raise HTTPException(status_code=400, detail="Sem registros para exportação.")
    
    diretorio_temp = tempfile.gettempdir()
    caminho_arquivo = os.path.join(diretorio_temp, "relatorio_ocorrencia.pdf")
    gerador_pdf.gerar_pdf(cache_ocorrencia, caminho_arquivo)
    
    nome_download = f"WikiFraudes_{cache_ocorrencia.nome_incidente.replace(' ', '_')}.pdf"
    return FileResponse(
        caminho_arquivo, 
        filename=nome_download,
        media_type="application/pdf"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)