import asyncio
import sys # Para encerrar o processo
import threading
import speech_recognition as sr
from core.stt import capturar_voz
from core.config_audio import ConfigAudio # Sua classe de config
from core.connect_api import chamar_fenix_na_nuvem 
from core.audio_engine import processo_falar
from core.system import SystemFenix  # Importando suas novas funções

class FenixBrain:
    def __init__(self, interface=None, nome_usuario="Airton", supabase_client=None):
        self.interface = interface
        self.nome_usuario = nome_usuario
        self.esta_falando = False
        self.mic_ativo = True
        
        # Identidade
        self.nome_projeto = "FENIX"

        # 1. Carregar Configurações de Áudio e Comandos Críticos
        self.cfg = ConfigAudio()
        self.reconhecedor = self.cfg.configurar_reconhecedor(sr.Recognizer())
        
        # Inicializa o Sistema Operacional do Fenix
        # Passamos o cliente supabase para o SystemFenix conseguir salvar os projetos
        self.system = SystemFenix(supabase_client=supabase_client)
        
        # Áudio e Reconhecimento
        self.cfg = ConfigAudio()
        self.reconhecedor = self.cfg.configurar_reconhecedor(sr.Recognizer())

    def log(self, mensagem):
        print(f"[LOG]: {mensagem}")
        if self.interface:
            self.interface.log_msg(mensagem)

    def falar(self, texto):
        if not texto: return
        def rodar():
            self.esta_falando = True
            asyncio.run(processo_falar(texto))
            self.esta_falando = False
        threading.Thread(target=rodar, daemon=True).start()

    def filtrar_comandos_sistema(self, msg):
        """
        Analisa a mensagem ANTES de mandar para a nuvem.
        Retorna a resposta do sistema ou None se não for um comando local.
        """
        # 1. Navegação
        if "onde você está" in msg or "diretório atual" in msg:
            return self.system.onde_estou()
        
        if "o que tem aqui" in msg or "listar arquivos" in msg:
            return self.system.listar_diretorio()

        if "vá para" in msg or "entrar na pasta" in msg:
            destino = msg.split("para")[-1].strip() if "para" in msg else msg.split("pasta")[-1].strip()
            return self.system.mudar_diretorio(destino)

        # 2. Gestão de Arquivos/Pastas
        if "novo projeto" in msg:
            nome = msg.split("projeto")[-1].strip()
            return self.system.protocolo_novo_projeto(nome)

        if "criar arquivo" in msg:
            nome = msg.split("arquivo")[-1].strip()
            return self.system.criar_arquivo_avulso(nome, "# Criado pelo Fenix")

        if "criar pasta" in msg:
            nome = msg.split("pasta")[-1].strip()
            return self.system.criar_pasta_avulsa(nome)

        if "remover" in msg:
            alvo = msg.split("remover")[-1].strip()
            return self.system.remover_item(alvo)

        return None # Se não caiu em nenhum comando, segue para a nuvem

    def processar_comando_manual(self, texto_digitado):
        if self.interface: self.interface.mudar_status("PENSANDO", "#FFA500")
        
        # Tenta executar como comando de sistema primeiro
        resposta_local = self.filtrar_comandos_sistema(texto_digitado.lower())
        
        if resposta_local:
            resposta = resposta_local
        else:
            resposta = chamar_fenix_na_nuvem(texto_digitado)
            
        self.log(f"Fenix: {resposta}")
        self.falar(resposta)

    def verificar_comandos_criticos(self, msg):
        """Verifica se o usuário deu ordem para desligar o sistema"""
        if any(cmd in msg for cmd in self.cfg.CMD_DESLIGAR):
            self.log("Encerrando Núcleo Fenix por comando de voz...")
            self.falar("Entendido, Senhor. Desligando sistemas. Até logo.")
            # Pequeno delay para a voz terminar e fechar o programa
            asyncio.run(asyncio.sleep(3))
            sys.exit() # Fecha o script Python completamente

    def start(self):
            self.log("Calibrando microfone com Energy Threshold fixo...")
            try:
                with sr.Microphone() as source:
                    # Usamos a duração de 0.5 apenas para ajuste inicial de ruído
                    self.reconhecedor.adjust_for_ambient_noise(source, duration=0.5)
            except Exception as e:
                self.log(f"Erro de Hardware: {e}")
                return

            self.log(f"Núcleo {self.nome_projeto} Online (Sensibilidade: {self.cfg.ENERGY_THRESHOLD}).")
            self.falar(f"Sistema ativo. Estou pronto, Senhor {self.nome_usuario}.")

            while True:
                if not self.esta_falando and self.mic_ativo:
                    if self.interface: self.interface.mudar_status("STANDBY", "#005555")
                    
                    fala_usuario = capturar_voz(self.reconhecedor)
                    
                    if fala_usuario:
                        msg = fala_usuario.lower()
                        self.log(f"Você: {fala_usuario}")

                        # --- ORDEM DE PRIORIDADE DOS COMANDOS ---
                        
                        # A. COMANDOS CRÍTICOS (Desligar)
                        self.verificar_comandos_criticos(msg)

                        # B. PALAVRA DE ATIVAÇÃO
                        if "fênix" in msg or "fenix" in msg:
                            if self.interface: self.interface.mudar_status("OUVINDO", "#00fbff")
                            
                            # C. COMANDOS DE SISTEMA (Locais)
                            resposta_sistema = self.filtrar_comandos_sistema(msg)
                            
                            if resposta_sistema:
                                resposta = resposta_sistema
                            else:
                                # D. CÉREBRO NA NUVEM (IA)
                                if self.interface: self.interface.mudar_status("PENSANDO", "#FFA500")
                                resposta = chamar_fenix_na_nuvem(fala_usuario)
                            
                            self.log(f"Fenix: {resposta}")
                            self.falar(resposta)
                
                asyncio.run(asyncio.sleep(0.3))