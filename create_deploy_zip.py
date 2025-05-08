import os
import zipfile
import sys

def create_deploy_zip(output_filename='whatsapp_api_deploy.zip'):
    """
    Cria um arquivo ZIP do projeto para deploy, excluindo arquivos e diretórios
    especificados no .gitignore
    """
    # Ler o arquivo .gitignore
    ignore_patterns = []
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignore_patterns.append(line)
    
    # Adicionar padrões específicos para o deploy
    ignore_patterns.extend([
        '.git/', 
        '.gitignore',
        output_filename,
        'create_deploy_zip.py'
    ])
    
    # Função para verificar se um arquivo deve ser ignorado
    def should_ignore(file_path):
        # Converter para caminho relativo
        rel_path = os.path.relpath(file_path, '.')
        
        # Verificar padrões exatos
        if rel_path in ignore_patterns:
            return True
        
        # Verificar diretórios e padrões com wildcard
        for pattern in ignore_patterns:
            # Diretórios
            if pattern.endswith('/') and rel_path.startswith(pattern):
                return True
            # Arquivos com extensão específica
            if pattern.startswith('*.') and rel_path.endswith(pattern[1:]):
                return True
            # Qualquer arquivo em um diretório específico
            if pattern.endswith('/*') and rel_path.startswith(pattern[:-1]):
                return True
        
        return False
    
    # Criar o arquivo ZIP
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            # Filtrar diretórios
            dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d))]
            
            # Adicionar arquivos
            for file in files:
                file_path = os.path.join(root, file)
                if not should_ignore(file_path):
                    arcname = os.path.relpath(file_path, '.')
                    zipf.write(file_path, arcname)
    
    print(f"Arquivo ZIP criado: {output_filename}")
    print(f"Tamanho: {os.path.getsize(output_filename) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    output_file = 'whatsapp_api_deploy.zip'
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    
    create_deploy_zip(output_file)
