import sys
import os

# Adicione o diretório do projeto ao path
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importe o app Flask
from src.main import app as application

# Para executar localmente
if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5003)
