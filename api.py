from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import sqlite3
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

@app.get("/stats")
def get_global_stats():
    # Em vez de sqlite3.connect(...), usamos o método do DatabaseManager
    # que garante que estamos no arquivo certo e com as tabelas criadas.
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Total de obras
            cursor.execute("SELECT COUNT(*) FROM obras")
            total_obras = cursor.fetchone()[0]
            
            # 2. Total de palavras ÚNICAS
            cursor.execute("SELECT COUNT(DISTINCT palavra) FROM palavras_vistas")
            vocabulario_unico = cursor.fetchone()[0]
            
            return {
                "total_obras": total_obras,
                "vocabulario_unico": vocabulario_unico
            }
    except Exception as e:
        # Isso vai nos ajudar a ver o erro no JSON da API se algo falhar
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats/top-words")
def get_top_words():
    with db._get_connection() as conn:
        cursor = conn.cursor()
        # Agrupa por palavra, soma as frequências e ordena do maior para o menor
        cursor.execute("""
            SELECT palavra, SUM(frequencia) as total 
            FROM palavras_vistas 
            GROUP BY palavra 
            ORDER BY total DESC 
            LIMIT 10
        """)
        return [{"word": row[0], "count": row[1]} for row in cursor.fetchall()]