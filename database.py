import sqlite3
import os
from datetime import datetime

# Define o caminho do banco de dados com base no ambiente
# Usa o caminho relativo por padrão
db_path = os.getenv("DATABASE_URL", "data/vocabstack.db")

# Cria diretório se necessário e se for um caminho relativo ou acessível
db_dir = os.path.dirname(db_path)
if db_dir and db_dir != "":
    try:
        os.makedirs(db_dir, exist_ok=True)
    except (PermissionError, OSError):
        # Se não conseguir criar o diretório, usa um caminho alternativo
        db_path = "vocabstack.db"
DATABASE_URL = db_path


class DatabaseManager:
    def __init__(self):
        # No Docker, usamos a variável de ambiente definida no docker-compose
        db_path = os.getenv("DATABASE_URL", DATABASE_URL)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_name = db_path
        self._create_tables()

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def _create_tables(self):
        with self._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS obras (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT, tipo TEXT, idioma TEXT, total_palavras INTEGER, data_leitura TIMESTAMP
                )
            """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS palavras_vistas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    obra_id INTEGER, palavra TEXT, frequencia INTEGER,
                    FOREIGN KEY (obra_id) REFERENCES obras (id)
                )
            """
            )

    def salvar_processamento(self, titulo, tipo, idioma, total, freq_dict):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO obras (titulo, tipo, idioma, total_palavras, data_leitura) VALUES (?, ?, ?, ?, ?)",
                (titulo, tipo, idioma, total, datetime.now()),
            )
            obra_id = cursor.lastrowid
            dados = [(obra_id, p, f) for p, f in freq_dict.items()]
            cursor.executemany(
                "INSERT INTO palavras_vistas (obra_id, palavra, frequencia) VALUES (?, ?, ?)",
                dados,
            )
            conn.commit()

    def listar_estante(self):
        with self._get_connection() as conn:
            return conn.execute(
                "SELECT titulo, total_palavras, data_leitura FROM obras"
            ).fetchall()
