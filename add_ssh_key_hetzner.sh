#!/bin/bash

# Este script adiciona uma chave SSH à sua conta Hetzner usando a API

# Substitua YOUR_API_TOKEN pelo seu token de API da Hetzner
HETZNER_API_TOKEN="YOUR_API_TOKEN"

# Chave SSH a ser adicionada
SSH_KEY="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJFRz+0JjUdlbenp6uCRgHNFAQY1oUe3UV58lHSUlAlZ leonardo@darwinai.com.br"

# Nome da chave SSH
KEY_NAME="MacBook Pro $(date +%Y-%m-%d)"

# Adicionar a chave SSH usando a API da Hetzner
curl -X POST \
  -H "Authorization: Bearer $HETZNER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"$KEY_NAME\",\"public_key\":\"$SSH_KEY\"}" \
  "https://api.hetzner.cloud/v1/ssh_keys"

echo "Chave SSH adicionada com sucesso!"
