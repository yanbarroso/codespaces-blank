# 🚀 CI/CD Pipeline - Vocabulab

Este documento descreve a automatização de integração contínua e deploy contínuo (CI/CD) implementada neste projeto.

## 📋 Overview

A pipeline CI/CD automatiza:

1. **Testes** - Valida o código e executa testes unitários
2. **Build** - Constrói a imagem Docker
3. **Segurança** - Realiza scanning de vulnerabilidades
4. **Publish** - Publica a imagem em um registro (GitHub Container Registry)
5. **Notificação** - Notifica sobre o status da pipeline

## 🔄 Fluxo da Pipeline

```
┌─────────────────┐
│  Push/PR em    │
│   main/dev     │
└────────┬────────┘
         │
         ├──► ✅ Test (testes + linting)
         │
         ├──► 🐳 Build (Docker image)
         │
         ├──► 🔒 Security (Trivy + OWASP)
         │
         └──► 📦 Push (apenas em main)
             └──► 📢 Notify Success
```

## ⚙️ Configuração

### GitHub Secrets (Opcional)

Para publicar em registros privados, configure:

```bash
DOCKER_REGISTRY_USERNAME=seu_usuario
DOCKER_REGISTRY_PASSWORD=seu_token
DOCKER_REGISTRY=seu_registry.azurecr.io
```

### Triggers Automáticos

A pipeline roda em:

- **Push** para `main` ou `develop`
- **Pull Requests** para `main` ou `develop`

## 🛠️ Desenvolvimento Local

### Instalação

```bash
# Instalar dependências de produção
make install

# Instalar dependências de desenvolvimento
make install-dev
```

### Executar Testes

```bash
# Rodar todos os testes
make test

# Rodar com cobertura
make test-cov
```

### Verificação de Código

```bash
# Linting com flake8
make lint

# Verificar formatação com black
make format-check

# Formatar código
make format
```

### Docker

```bash
# Build das imagens
make build

# Iniciar containers
make run

# Parar containers
make stop

# Ver logs
make logs
```

## 📊 Jobs da Pipeline

### 1. Test Job

Executa:
- ✅ Instalação de dependências
- ✅ Linting com flake8
- ✅ Formatação com black
- ✅ Testes unitários com pytest
- ✅ Relatório de cobertura

**Status**: Obrigatório para passar ✋

### 2. Build Job

Executa:
- ✅ Setup do Docker Buildx
- ✅ Build multi-stage otimizado
- ✅ Teste da imagem criada
- ✅ Cache de camadas

**Status**: Requer que Test passe ✋

### 3. Security Job

Executa:
- ✅ Trivy (scanning de vulnerabilidades)
- ✅ OWASP Dependency-Check
- ✅ Upload para GitHub Security

**Status**: Informativo (não bloqueia) ℹ️

### 4. Push Job

Executa:
- ✅ Build e push da imagem
- ✅ Metadata com tags (latest, sha, semver)
- ✅ Publicação em GHCR

**Status**: Apenas em merge para main 📦

## 🔐 Segurança

### Scanning Implementado

1. **Trivy** - Vulnerabilidades em dependências e imagens
2. **OWASP Dependency-Check** - Verificação de dependências conhecidas como inseguras
3. **GitHub CodeQL** - Análise estática de código

### Relatórios

Os relatórios de segurança aparecem em:
- GitHub Security → Code scanning alerts
- GitHub Actions → Workflow run summary

## 📈 Cobertura de Testes

- Relatório em HTML: `htmlcov/index.html`
- Enviado para Codecov.io (se configurado)
- Objetivo: > 80% de cobertura

## 🚦 Status Checks

Todos os status checks devem passar antes de fazer merge:

- ✅ Test - Python testes
- ✅ Build - Docker build
- ✅ Security - Scanning

## 📝 Commits e Branches

### Nomes de Branch Recomendados

```
feature/nova-funcionalidade
bugfix/correcao-importante
hotfix/critico
docs/documentacao
```

### Mensagens de Commit

```
[FEATURE] Adicionar nova funcionalidade
[FIX] Corrigir bug crítico
[DOCS] Atualizar documentação
[TEST] Adicionar testes
```

## 🐛 Debugging da Pipeline

### Ver logs da workflow

1. Go to GitHub → Actions
2. Clique na workflow
3. Clique no job desejado
4. Expanda os steps

### Rodagem local

```bash
# Testar localmente antes de commitar
make test
make lint
make format-check

# Simular build Docker
docker build -t vocabulab-test .
```

## 🔗 Recursos

- GitHub Actions: https://docs.github.com/en/actions
- Docker Build: https://docs.docker.com/build/
- Trivy: https://github.com/aquasecurity/trivy
- Pytest: https://docs.pytest.org/

## 📞 Troubleshooting

### Testes falhando

```bash
# Rodar testes com output detalhado
pytest -vv

# Rodar apenas um teste específico
pytest tests/test_api.py::TestHealthCheck::test_stats_endpoint -vv
```

### Build Docker falhando

```bash
# Build sem cache
docker-compose build --no-cache

# Ver logs de build detalhados
DOCKER_BUILDKIT=1 docker build --progress=plain . 2>&1 | head -100
```

### Problemas de permissão

```bash
# Verificar usuario do container
docker run vocabulab whoami

# Verificar permissões de arquivos
docker run vocabulab ls -la /app
```

---

**Última atualização**: 2026-03-17
