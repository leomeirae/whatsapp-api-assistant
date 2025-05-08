#!/bin/bash

# Criar diretório de logs se não existir
mkdir -p logs

# Ativar ambiente virtual (se estiver usando)
# source venv/bin/activate

# Exportar variáveis de ambiente (ou usar .env com python-dotenv)
# export FLASK_ENV=production

# Iniciar o Gunicorn com a configuração
gunicorn -c gunicorn_config.py src.main:app
