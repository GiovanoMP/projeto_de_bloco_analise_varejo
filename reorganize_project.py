import os
import shutil
from pathlib import Path

def create_directory_structure():
    """Cria a estrutura base de diretórios."""
    directories = [
        './notebooks/analysis',
        './notebooks/experiments',
        './src/utils',
        './src/visualization',
        './scripts'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Criado diretório: {directory}")

def move_files():
    """Move os arquivos para suas localizações corretas."""
    # Mapeamento de arquivos para seus destinos
    file_moves = {
        # Arquivos de configuração para raiz
        'src/.gitignore': './.gitignore',
        'src/requirements.txt': './requirements.txt',
        'src/runtime.txt': './runtime.txt',
        'src/Procfile': './Procfile',
        'src/README.md': './README.md',
        
        # Scripts de reorganização
        'src/reorganize.sh': './scripts/reorganize.sh',
        
        # Notebooks
        'notebooks/stackin_modelos.ipynb': './notebooks/experiments/stackin_modelos.ipynb'
    }
    
    # Realizar movimentação dos arquivos
    for source, dest in file_moves.items():
        try:
            if os.path.exists(source):
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.move(source, dest)
                print(f"Movido: {source} -> {dest}")
        except Exception as e:
            print(f"Erro ao mover {source}: {str(e)}")

def remove_unnecessary_files():
    """Remove arquivos desnecessários."""
    files_to_remove = [
        'src/bash.exe.stackdump',
    ]
    
    for file in files_to_remove:
        try:
            if os.path.exists(file):
                os.remove(file)
                print(f"Removido: {file}")
        except Exception as e:
            print(f"Erro ao remover {file}: {str(e)}")

def clean_empty_directories():
    """Remove diretórios vazios."""
    for dirpath, dirnames, filenames in os.walk('.', topdown=False):
        for dirname in dirnames:
            try:
                full_path = os.path.join(dirpath, dirname)
                if not os.listdir(full_path):  # se diretório estiver vazio
                    os.rmdir(full_path)
                    print(f"Removido diretório vazio: {full_path}")
            except Exception as e:
                print(f"Erro ao remover diretório {dirname}: {str(e)}")

def create_gitignore():
    """Cria um arquivo .gitignore atualizado."""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Jupyter Notebook
.ipynb_checkpoints
*/.ipynb_checkpoints/*

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Sistema
.DS_Store
Thumbs.db
*.stackdump

# Arquivos específicos do projeto
*.csv
*.xlsx
*.joblib
*.pkl

# Logs
*.log
logs/
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("Arquivo .gitignore criado/atualizado")

def main():
    """Função principal para executar a reorganização."""
    try:
        print("Iniciando reorganização do projeto...")
        
        # Criar backup (opcional)
        # shutil.copytree('.', '../project_backup', dirs_exist_ok=True)
        
        # Executar etapas de reorganização
        create_directory_structure()
        move_files()
        remove_unnecessary_files()
        clean_empty_directories()
        create_gitignore()
        
        print("\nReorganização concluída com sucesso!")
        print("\nEstrutura final do projeto:")
        os.system('tree -L 2 -I "__pycache__|*.pyc"')
        
    except Exception as e:
        print(f"Erro durante a reorganização: {str(e)}")

if __name__ == "__main__":
    main()