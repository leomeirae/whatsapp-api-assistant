from flask import Flask, jsonify

# Criar uma instância simples do Flask
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    """Rota de teste simples."""
    return "WhatsApp API Assistant está funcionando!"

@app.route("/api/test", methods=["GET"])
def test():
    """Rota de teste para API."""
    return jsonify({
        "status": "success",
        "message": "API está funcionando!"
    })
