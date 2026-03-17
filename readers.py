import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import pdfplumber
import trafilatura

class BaseReader:
    def extract_text(self, file_path):
        raise NotImplementedError("Subclasses devem implementar extract_text")

class EpubReader(BaseReader):
    def extract_text(self, file_path):
        book = epub.read_epub(file_path)
        full_text = []
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            full_text.append(soup.get_text())
        return " ".join(full_text)

class PdfReader(BaseReader):
    def extract_text(self, file_path):
        with pdfplumber.open(file_path) as pdf:
            return " ".join([page.extract_text() or "" for page in pdf.pages])

class TxtReader(BaseReader):
    def extract_text(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

class WebReader(BaseReader):
    def extract_text(self, url):
        downloaded = trafilatura.fetch_url(url)
        return trafilatura.extract(downloaded) if downloaded else ""

class ReaderFactory:
    @staticmethod
    def get_reader(file_path):
        if file_path.startswith('http'): return WebReader()
        ext = os.path.splitext(file_path)[1].lower()
        mapping = {'.epub': EpubReader, '.pdf': PdfReader, '.txt': TxtReader}
        reader_class = mapping.get(ext)
        if not reader_class: raise ValueError(f"Extensão {ext} não suportada.")
        return reader_class()