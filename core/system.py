import os
from pathlib import Path
import difflib

class SystemFenix:
    def __init__(self, supabase_client=None):
        self.supabase = supabase_client
        # Usando Pathlib para caminhos inteligentes
        self.home = Path.home()
        self.base_path = self.home / "Documents" / "FENIX_FILES"
        self.base_path.mkdir(parents=True, exist_ok=True)

    #FUNÇÂO 1
    def _resolver_caminho_humano(self, termo):
        """Traduz termos humanos (Downloads, Desktop) para caminhos reais sem gambiarra."""
        # Pastas do sistema que o usuário costuma citar
        pastas_sistema = {
            "downloads": self.home / "Downloads",
            "documentos": self.home / "Documents",
            "desktop": self.home / "Desktop",
            "área de trabalho": self.home / "Desktop",
            "projetos": self.base_path / "PROJETOS",
            "fenix": self.base_path
        }
        
        termo_limpo = termo.lower().strip()
        # Busca aproximada: se você falar "Download", ele acha "Downloads"
        match = difflib.get_close_matches(termo_limpo, pastas_sistema.keys(), n=1, cutoff=0.6)
        
        if match:
            return pastas_sistema[match[0]]
        return Path(termo) # Se não for atalho, assume que é um caminho direto

    #FUNÇÂO 2
    def onde_estou(self):
        caminho = Path.cwd()
        # Humanizando para a voz: troca barras por pausas e remove o "C:"
        partes = list(caminho.parts)
        if "C:\\" in partes[0]: partes[0] = "Disco Local C"
        
        texto_humano = ", ".join(partes)
        return f"Senhor, atualmente estou operando em: {texto_humano}."

    #FUNÇÂO 3
    def mudar_diretorio(self, novo_caminho):
        try:
            alvo = self._resolver_caminho_humano(novo_caminho)
            if alvo.exists() and alvo.is_dir():
                os.chdir(alvo)
                return f"Entendido. Já me movi para a pasta {alvo.name}. O que deseja fazer aqui?"
            return f"Senhor, não encontrei a pasta {novo_caminho}. Gostaria que eu fizesse uma busca profunda?"
        except Exception as e:
            return f"Não foi possível acessar esse local. Erro: {e}"

    #FUNÇÂO 4
    def listar_diretorio(self, caminho=None):
        try:
            alvo = Path(caminho) if caminho else Path.cwd()
            itens = list(alvo.iterdir())

            if not itens:
                return f"A pasta {alvo.name} está vazia, Senhor."

            pastas = [f.name for f in itens if f.is_dir()]
            arquivos = [f.name for f in itens if f.is_file()]

            # Resposta para a voz: mais humana, menos técnica
            res = f"Nesta pasta encontrei {len(pastas)} pastas e {len(arquivos)} arquivos. "
            if arquivos:
                # Remove extensões chatas da fala como .py, .txt para soar natural
                lista_voz = [a.split('.')[0] for a in arquivos]
                res += f"Os principais arquivos são: {', '.join(lista_voz[:5])}."
            
            return res
        except Exception as e:
            return f"Erro ao escanear o local: {e}"
        
    #FUNÇÂO 5
    def protocolo_novo_projeto(self, nome, info="Sem descrição"):
        if not self.supabase:
            return "O banco de dados não está conectado, Senhor."

        try:
            caminho_projeto = self.base_path / "PROJETOS" / nome
            caminho_projeto.mkdir(parents=True, exist_ok=True)

            dados = {
                "nome": nome,
                "informacao": info,
                "anotacoes": "Projeto iniciado via comando de voz.",
                "versao": "1.0.0",
                "criador": "Fenix (Airton)"
            }
            
            self.supabase.table("projetos_fenix").insert(dados).execute()
            return f"O protocolo foi concluído. O projeto {nome} já está na base de dados e a pasta foi criada."
        except Exception as e:
            return f"Falha ao oficializar projeto: {e}"

# --- FUNÇÃO 6: CRIAR APENAS PASTA (NO LOCAL ATUAL) ---
    def criar_pasta_avulsa(self, nome_pasta):
        try:
            nome_limpo = nome_pasta.strip().capitalize()
            # Path.cwd() garante que a pasta nasce onde o Fenix está agora
            caminho_completo = Path.cwd() / nome_limpo
            
            if caminho_completo.exists():
                return f"Senhor, a pasta {nome_limpo} já existe aqui."
            
            caminho_completo.mkdir(parents=True, exist_ok=True)
            return f"Feito! Pasta {nome_limpo} criada no diretório atual."
        except Exception as e:
            return f"Erro ao criar pasta: {e}"

    # --- FUNÇÃO 7: CRIAR APENAS ARQUIVO (NO LOCAL ATUAL) ---
    def criar_arquivo_avulso(self, nome_arquivo, conteudo=""):
        try:
            # Novamente, Path.cwd() para não mandar para a FENIX_FILES
            caminho_completo = Path.cwd() / nome_arquivo.strip()
            caminho_completo.write_text(conteudo, encoding="utf-8")
            return f"Arquivo {nome_arquivo} gerado aqui mesmo."
        except Exception as e:
            return f"Erro ao gerar arquivo: {e}"

    # --- FUNÇÃO 8: REMOVER ITEM ---
    def remover_item(self, nome_item):
        try:
            # Tenta achar no local atual ou na base_path
            alvo = Path.cwd() / nome_item
            if not alvo.exists():
                alvo = self.base_path / nome_item
            
            if alvo.exists():
                if alvo.is_dir():
                    alvo.rmdir() # Só remove se vazia
                else:
                    alvo.unlink()
                return f"Item {nome_item} removido, Senhor."
            return "Não encontrei o item para remover."
        except Exception as e:
            return f"Erro ao remover: {e}"