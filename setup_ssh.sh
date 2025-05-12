#!/bin/bash

# Este script configura a chave SSH no servidor remoto

# Chave pública a ser adicionada
SSH_KEY="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJFRz+0JjUdlbenp6uCRgHNFAQY1oUe3UV58lHSUlAlZ leonardo@darwinai.com.br"

# Servidor remoto
SERVER="ubuntu@157.180.32.249"

# Comando a ser executado no servidor remoto
REMOTE_COMMAND="mkdir -p ~/.ssh && echo \"$SSH_KEY\" >> ~/.ssh/authorized_keys && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys && echo 'Chave SSH configurada com sucesso!'"

# Executar o comando no servidor remoto
echo "Configurando chave SSH no servidor $SERVER..."
echo "Você precisará digitar a senha do servidor quando solicitado."
ssh $SERVER "$REMOTE_COMMAND"

echo "Configuração concluída. Tentando fazer login com a chave SSH..."
ssh -i ~/.ssh/id_ed25519 $SERVER "echo 'Login com chave SSH bem-sucedido!'"
