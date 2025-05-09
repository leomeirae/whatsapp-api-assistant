import sys
import os

# Adiciona o diretório raiz ao sys.path para permitir importações corretas
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Importar o aplicativo principal do src/main.py
from src.main import app

# Rota de teste adicional para verificar se a API está funcionando
@app.route("/api/test", methods=["GET"])
def test():
    """Rota de teste para API."""
    from flask import jsonify
    return jsonify({
        "status": "success",
        "message": "API está funcionando!"
    })
