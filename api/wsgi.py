import os
from index import app

# Necessário para o Vercel e Docker
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
