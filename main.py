import sys
import os
from readers import ReaderFactory
from processors import LanguageProcessor
from database import DatabaseManager

def main():
    # Inicializa as dependências
    db = DatabaseManager()
    
    # Se você passar argumentos via terminal: python main.py arquivo.epub "Titulo"
    if len(sys.argv) > 1:
        caminho_arquivo = sys.argv[1]
        titulo = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(caminho_arquivo)
        
        print(f"🚀 Processando localmente: {titulo}...")
        
        try:
            # 1. Detecta o idioma (por enquanto fixo em 'fr')
            proc = LanguageProcessor('fr')
            
            # 2. Usa a Factory para pegar o leitor correto
            leitor = ReaderFactory.get_reader(caminho_arquivo)
            
            # 3. Extrai e Processa
            texto = leitor.extract_text(caminho_arquivo)
            stats = proc.get_detailed_stats(texto)
            
            # 4. Salva no SQL
            tipo = os.path.splitext(caminho_arquivo)[1][1:].upper() or "WEB"
            db.salvar_processamento(
                titulo=titulo,
                tipo=tipo,
                idioma="french",
                total=stats["total_count"],
                freq_dict=stats["word_frequencies"]
            )
            
            print(f"✅ Sucesso! Total de palavras processadas: {stats['total_count']}")
            
        except Exception as e:
            print(f"❌ Erro ao processar arquivo: {e}")
    
    else:
        # Se rodar apenas 'python main.py', ele mostra a estante atual
        print("\n--- 📚 Estante VocabStack ---")
        estante = db.listar_estante()
        if not estante:
            print("Sua estante está vazia. Suba um arquivo via API ou use: python main.py <arquivo>")
        for obra in estante:
            print(f"📖 {obra[0]} | Palavras: {obra[1]} | Lido em: {obra[2]}")

if __name__ == "__main__":
    main()