import os
import re
from collections import Counter

class DocumentChunk:
    """Classe para representar um chunk de documento."""
    def __init__(self, content, source, title=None):
        self.content = content
        self.source = source
        self.title = title or os.path.basename(source)

    def __str__(self):
        return f"{self.title} - {self.content[:50]}..."

def find_markdown_files(directory):
    """Encontra todos os arquivos markdown em um diretório e seus subdiretórios."""
    markdown_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def split_document(content, source, chunk_size=1000, overlap=200):
    """Divide um documento em chunks menores com sobreposição."""
    chunks = []

    # Extrair título do documento (primeira linha com #)
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else os.path.basename(source)

    # Dividir por parágrafos ou seções
    paragraphs = re.split(r'\n\s*\n', content)

    current_chunk = ""
    for paragraph in paragraphs:
        # Se adicionar este parágrafo exceder o tamanho do chunk, salve o chunk atual e comece um novo
        if len(current_chunk) + len(paragraph) > chunk_size and current_chunk:
            chunks.append(DocumentChunk(current_chunk, source, title))
            # Manter alguma sobreposição para contexto
            current_chunk = current_chunk[-overlap:] if overlap > 0 else ""

        current_chunk += paragraph + "\n\n"

    # Adicionar o último chunk se não estiver vazio
    if current_chunk.strip():
        chunks.append(DocumentChunk(current_chunk, source, title))

    return chunks

def load_knowledge_base(knowledge_base_dir):
    """Carrega e processa a base de conhecimento em chunks."""
    all_chunks = []
    knowledge_base_files = find_markdown_files(knowledge_base_dir)

    for file_path in knowledge_base_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Dividir o documento em chunks
                document_chunks = split_document(content, file_path)
                all_chunks.extend(document_chunks)
                print(f"Carregado: {file_path} - {len(document_chunks)} chunks")
        except Exception as e:
            print(f"Erro ao carregar {file_path}: {e}")

    return all_chunks

def tokenize(text):
    """Tokeniza o texto em palavras, removendo pontuação e convertendo para minúsculas."""
    # Remover pontuação e converter para minúsculas
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    # Dividir em palavras
    return text.split()

def get_relevant_context(user_question, knowledge_chunks, top_k=5, max_chars=8000):
    """Extrai contexto relevante da base de conhecimento usando uma busca simples baseada em palavras-chave."""
    if not knowledge_chunks:
        return "Base de conhecimento não disponível."

    # Tokenizar a pergunta
    question_tokens = tokenize(user_question)
    
    # Remover palavras muito comuns (stop words simples em português)
    stop_words = {'a', 'o', 'e', 'é', 'de', 'da', 'do', 'em', 'para', 'com', 'um', 'uma', 'os', 'as', 'que', 'no', 'na', 'se'}
    question_tokens = [token for token in question_tokens if token not in stop_words and len(token) > 2]
    
    # Calcular pontuação para cada chunk
    chunk_scores = []
    for i, chunk in enumerate(knowledge_chunks):
        chunk_tokens = tokenize(chunk.content)
        
        # Contar ocorrências de tokens da pergunta no chunk
        score = 0
        for token in question_tokens:
            score += chunk_tokens.count(token)
        
        chunk_scores.append((i, score))
    
    # Ordenar chunks por pontuação
    chunk_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Obter os top_k chunks mais relevantes
    top_indices = [idx for idx, score in chunk_scores[:top_k] if score > 0]
    
    # Construir o contexto com os chunks mais relevantes
    relevant_context = ""
    sources_used = set()
    
    for idx in top_indices:
        chunk = knowledge_chunks[idx]
        relevant_context += f"\n\n--- Trecho de {chunk.title} ---\n"
        relevant_context += chunk.content
        sources_used.add(chunk.source)
    
    # Se não encontrou nada relevante, use os primeiros chunks
    if not relevant_context:
        print("Nenhum conteúdo relevante encontrado, usando chunks padrão.")
        for i in range(min(3, len(knowledge_chunks))):
            chunk = knowledge_chunks[i]
            relevant_context += f"\n\n--- Trecho de {chunk.title} ---\n"
            relevant_context += chunk.content
    
    # Limitar o tamanho do contexto para não exceder limites de tokens
    if len(relevant_context) > max_chars:
        relevant_context = relevant_context[:max_chars]
    
    print(f"Fontes utilizadas: {', '.join([os.path.basename(src) for src in sources_used])}")
    return relevant_context
