from supabase import create_client
from src.config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_KEY

# Inicializar cliente Supabase com a chave anônima (para autenticação)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Inicializar cliente Supabase com a chave de serviço (para contornar RLS)
supabase_admin = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

class User:
    """Classe para representar um usuário."""

    def __init__(self, id=None, email=None, is_authenticated=False):
        self.id = id
        self.email = email
        self.is_authenticated = is_authenticated
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return str(self.id)

    @staticmethod
    def get_by_id(user_id):
        """Busca um usuário pelo ID."""
        try:
            # Usar a API REST do Supabase para buscar o usuário
            response = supabase.table('users').select('*').eq('id', user_id).execute()
            print(f"Resposta da busca por ID: {response}")

            if response.data and len(response.data) > 0:
                user_data = response.data[0]
                return User(
                    id=user_data['id'],
                    email=user_data['email'],
                    is_authenticated=True
                )
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            import traceback
            traceback.print_exc()
        return None

    @staticmethod
    def get_by_email(email):
        """Busca um usuário pelo email."""
        try:
            # Usar a API REST do Supabase para buscar o usuário
            response = supabase.table('users').select('*').eq('email', email).execute()
            print(f"Resposta da busca por email: {response}")

            if response.data and len(response.data) > 0:
                user_data = response.data[0]
                return User(
                    id=user_data['id'],
                    email=user_data['email'],
                    is_authenticated=True
                )
        except Exception as e:
            print(f"Erro ao buscar usuário por email: {e}")
            import traceback
            traceback.print_exc()
        return None

class ChatHistory:
    """Classe para gerenciar o histórico de conversas."""

    @staticmethod
    def save_message(user_id, role, content):
        """Salva uma mensagem no histórico."""
        try:
            # Preparar os dados para inserção
            data = {
                'user_id': user_id,
                'role': role,  # 'user' ou 'assistant'
                'content': content
            }

            # Usar o cliente admin com a chave de serviço para contornar RLS
            response = supabase_admin.table('chat_history').insert(data).execute()
            print(f"Resposta ao salvar mensagem: {response}")
            return True
        except Exception as e:
            print(f"Erro ao salvar mensagem: {e}")
            import traceback
            traceback.print_exc()
            return None

    @staticmethod
    def get_user_history(user_id, limit=50):
        """Obtém o histórico de conversas de um usuário."""
        try:
            # Usar o cliente admin com a chave de serviço para contornar RLS
            response = supabase_admin.table('chat_history') \
                .select('*') \
                .eq('user_id', user_id) \
                .order('created_at', desc=False) \
                .limit(limit) \
                .execute()

            print(f"Resposta ao obter histórico: {response}")

            if hasattr(response, 'data') and response.data:
                return response.data
            return []
        except Exception as e:
            print(f"Erro ao obter histórico: {e}")
            import traceback
            traceback.print_exc()
            return []
