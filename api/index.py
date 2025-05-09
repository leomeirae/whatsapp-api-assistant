import sys
import os
from dotenv import load_dotenv

# Configurar variáveis de ambiente a partir de .env se existir
load_dotenv()

# Adicionar o diretório raiz ao path para permitir importações
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar a aplicação Flask
from src.main import app
