import os
import json
import time
from datetime import datetime

# Diretório para armazenar os arquivos de histórico
HISTORY_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Garantir que o diretório existe
if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)

class LocalStorage:
    """Classe para gerenciar o armazenamento local de dados."""
    
    @staticmethod
    def save_message(user_id, role, content):
        """Salva uma mensagem no histórico local."""
        try:
            # Criar nome do arquivo baseado no ID do usuário
            filename = os.path.join(HISTORY_DIR, f"{user_id}.json")
            
            # Carregar histórico existente ou criar um novo
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            else:
                history = []
            
            # Adicionar nova mensagem
            message = {
                'id': str(int(time.time() * 1000)),  # ID único baseado no timestamp
                'user_id': user_id,
                'role': role,
                'content': content,
                'created_at': datetime.now().isoformat()
            }
            
            history.append(message)
            
            # Salvar histórico atualizado
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Erro ao salvar mensagem localmente: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def get_user_history(user_id, limit=50):
        """Obtém o histórico de conversas de um usuário do armazenamento local."""
        try:
            # Criar nome do arquivo baseado no ID do usuário
            filename = os.path.join(HISTORY_DIR, f"{user_id}.json")
            
            # Verificar se o arquivo existe
            if not os.path.exists(filename):
                return []
            
            # Carregar histórico
            with open(filename, 'r', encoding='utf-8') as f:
                history = json.load(f)
            
            # Ordenar por data de criação e limitar o número de mensagens
            history.sort(key=lambda x: x.get('created_at', ''))
            
            return history[-limit:] if len(history) > limit else history
        except Exception as e:
            print(f"Erro ao obter histórico local: {e}")
            import traceback
            traceback.print_exc()
            return []
