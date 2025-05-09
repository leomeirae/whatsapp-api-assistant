FROM python:3.11-slim

WORKDIR /app

# Copiar apenas os arquivos necessários
COPY requirements-vercel.txt .
RUN pip install --no-cache-dir -r requirements-vercel.txt

# Copiar apenas os arquivos necessários
COPY api ./api
COPY src/static ./src/static
COPY src/templates ./src/templates
COPY src/knowledge_base ./src/knowledge_base
COPY src/vercel_main.py ./src/vercel_main.py
COPY src/simple_search.py ./src/simple_search.py

# Definir variáveis de ambiente
ENV PYTHONPATH=/app
ENV PORT=8080

# Expor a porta que o aplicativo usará
EXPOSE 8080

# Comando para iniciar o aplicativo
CMD ["python", "api/wsgi.py"]
