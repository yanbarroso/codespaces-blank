from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from readers import ReaderFactory
from processors import LanguageProcessor
from database import DatabaseManager

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

db = DatabaseManager()
proc = LanguageProcessor('fr')

@app.post("/upload")
async def upload_obra(titulo: str = Form(...), arquivo: UploadFile = File(...)):
    temp_path = f"data/temp_{arquivo.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(arquivo.file, buffer)
    
    try:
        leitor = ReaderFactory.get_reader(temp_path)
        texto = leitor.extract_text(temp_path)
        stats = proc.get_detailed_stats(texto)
        
        tipo = os.path.splitext(arquivo.filename)[1][1:].upper()
        db.salvar_processamento(titulo, tipo, "french", stats["total_count"], stats["word_frequencies"])
        return {"status": "success", "titulo": titulo}
    finally:
        if os.path.exists(temp_path): os.remove(temp_path)

@app.get("/estante")
async def get_estante():
    return [{"titulo": r[0], "total": r[1], "data": r[2]} for r in db.listar_estante()]