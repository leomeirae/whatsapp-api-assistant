# Configuração do Gunicorn para produção

# Número de workers (processos) - geralmente (2 x núcleos) + 1
workers = 4

# Número de threads por worker
threads = 2

# Bind - endereço e porta para o servidor
bind = "0.0.0.0:5000"

# Timeout em segundos
timeout = 120

# Configurações de log
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"

# Configurações de segurança
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Configuração para o aplicativo Flask
wsgi_app = "src.main:app"
