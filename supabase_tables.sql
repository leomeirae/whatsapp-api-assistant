-- Criar tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar tabela de histórico de chat
CREATE TABLE IF NOT EXISTS chat_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar índices para melhorar a performance
CREATE INDEX IF NOT EXISTS idx_chat_history_user_id ON chat_history(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_created_at ON chat_history(created_at);

-- Configurar políticas de segurança (RLS - Row Level Security)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;

-- Políticas para a tabela de usuários
CREATE POLICY "Usuários podem ver apenas seus próprios dados" 
    ON users FOR SELECT 
    USING (auth.uid() = id);

CREATE POLICY "Usuários podem atualizar apenas seus próprios dados" 
    ON users FOR UPDATE 
    USING (auth.uid() = id);

-- Políticas para a tabela de histórico de chat
CREATE POLICY "Usuários podem ver apenas seu próprio histórico" 
    ON chat_history FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Usuários podem inserir apenas em seu próprio histórico" 
    ON chat_history FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

-- Permitir acesso anônimo para autenticação
CREATE POLICY "Acesso público para autenticação" 
    ON users FOR SELECT 
    USING (true);

CREATE POLICY "Inserção pública para registro" 
    ON users FOR INSERT 
    WITH CHECK (true);
