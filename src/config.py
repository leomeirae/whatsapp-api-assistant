import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Configurações do Flask
SECRET_KEY = os.getenv("SECRET_KEY", "chave_secreta_temporaria")

# Configurações do OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
