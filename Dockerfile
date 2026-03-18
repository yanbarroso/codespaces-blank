# Multi-stage build para otimização
# Etapa 1: Build
FROM python:3.11-slim as builder

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema necessárias para compilar pacotes Python
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas o arquivo de requisitos primeiro (otimização de cache de camada)
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Baixa os modelos iniciais (Francês)
RUN python -m nltk.downloader stopwords && \
    python -m spacy download fr_core_news_sm

# Etapa 2: Runtime
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia as dependências instaladas da etapa de build
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copia o cache e dados da etapa de build (NLTK, spacy, etc.) para /nlp_data
RUN mkdir -p /nlp_data && chmod 755 /nlp_data
COPY --from=builder /root/nltk_data /nlp_data/nltk_data
COPY --from=builder /root/.cache /nlp_data/.cache

# Copia o restante do código do projeto
COPY . .

# Cria diretórios necessários com permissões apropriadas
RUN mkdir -p /app/data /app/tmp && \
    chmod 755 /app /nlp_data && \
    chmod 775 /app/data /app/tmp

# Cria usuário não privilegiado para rodar a aplicação
RUN useradd -m -u 1000 -s /sbin/nologin appuser && \
    chown -R appuser:appuser /app /nlp_data

# Configura variáveis de ambiente
ENV NLTK_DATA=/nlp_data/nltk_data
ENV HOME=/app
ENV PYTHONUNBUFFERED=1

# Define o usuário não privilegiado
USER appuser

# Expõe a porta que o FastAPI vai rodar
EXPOSE 8000

# Comando para rodar a API usando o Uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
