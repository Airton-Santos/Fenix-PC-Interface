import sys, os, asyncio, threading, uuid
from colorama import Fore, Style, init
import speech_recognition as sr
import edge_tts
import pygame

# Importações do seu projeto
from core.stt import capturar_voz
from core.config_audio import ConfigAudio
from core.system import obter_processos_pesados, saude_hardware, limpar_temporarios, encerrar_projeto, analisar_conexoes
from core.connect_api import chamar_feni_na_nuvem # Conecta com o Railway

init(autoreset=True)
pygame.mixer.init()

async def falar_async(texto):
    voice = "pt-BR-AntonioNeural"
    # Gera um nome único para evitar o erro de Permission Denied [Errno 13]
    id_sessao = str(uuid.uuid4())[:8]
    output_file = f"res_{id_sessao}.mp3"
    
    try:
        # 1. Gera o áudio via Edge-TTS
        communicate = edge_tts.Communicate(texto, voice)
        await communicate.save(output_file)
        
        # 2. Pequena pausa de segurança
        await asyncio.sleep(0.2) 

        if os.path.exists(output_file):
            # 3. Carrega e reproduz
            pygame.mixer.music.load(output_file)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
            
            # 4. LIBERA o arquivo (essencial para não dar erro de permissão depois)
            pygame.mixer.music.unload() 
            
            # 5. Remove o arquivo temporário
            try:
                os.remove(output_file)
            except:
                pass # Se falhar a remoção, não trava o sistema
    except Exception as e:
        print(f"{Fore.RED}Erro no protocolo de voz: {e}{Style.RESET_ALL}")

def falar(texto):
    # Roda o áudio em uma thread separada para não travar a interface
    threading.Thread(target=lambda: asyncio.run(falar_async(texto)), daemon=True).start()

class FenixBrain:
    def __init__(self, interface=None, nome_usuario="Airton"):
        self.nome_ia = "Feni"
        self.nome_projeto = "FENIX"
        self.nome_usuario = nome_usuario
        self.interface = interface 
        self.cfg = ConfigAudio()
        self.reconhecedor = sr.Recognizer()
        self.reconhecedor = self.cfg.configurar_reconhecedor(self.reconhecedor)

    def log(self, mensagem, cor=Fore.WHITE):
        print(f"{cor}{mensagem}{Style.RESET_ALL}")
        if self.interface:
            self.interface.log_msg(mensagem)

    def processar_comando_manual(self, comando):
        """MÉTODO DE CONEXÃO COM A INTERFACE (CARDS)"""
        self.log(f"COMANDO MANUAL: {comando.upper()}", Fore.CYAN)
        
        if comando == "processos":
            falar("Analisando processos pesados.")
            res = obter_processos_pesados()
            self.log(res, Fore.GREEN)
            falar(res)
            
        elif comando == "hardware":
            falar("Verificando saúde do hardware.")
            res = saude_hardware()
            self.log(res, Fore.GREEN)
            falar(res)
            
        elif comando == "limpeza":
            falar("Iniciando limpeza de arquivos temporários.")
            res = limpar_temporarios()
            self.log(res, Fore.GREEN)
            falar(res)
            
        elif comando == "rede":
            falar("Analisando conexões de rede.")
            res = analisar_conexoes()
            self.log(res, Fore.GREEN)
            falar(res)
            
        elif "set_volume" in comando:
            try:
                novo_vol = float(comando.split(":")[1])
                from core.system import ajustar_volume_app
                ajustar_volume_app(novo_vol)
            except:
                pass

    def executar_diagnostico(self):
        """Fluxo de voz para diagnóstico"""
        self.log("Aguardando instrução de diagnóstico...", Fore.YELLOW)
        falar("O que o senhor deseja verificar no sistema?") 
        
        escolha = capturar_voz(self.reconhecedor, timeout=7)
        if not escolha: return

        escolha = escolha.lower()
        if "processos" in escolha or "memória" in escolha:
            falar(obter_processos_pesados())
        elif "saúde" in escolha or "hardware" in escolha:
            falar(saude_hardware())
        elif "limpeza" in escolha or "temporários" in escolha:
            falar(limpar_temporarios())
        elif "rede" in escolha or "conexão" in escolha:
            falar(analisar_conexoes())
        else:
            falar("Entendido. Voltando para escuta passiva.")

    def start(self):
        self.log("Calibrando sensores acústicos...", Fore.YELLOW)
        with sr.Microphone() as source:
            # Ajuste dinâmico para o ambiente do Senhor
            self.reconhecedor.adjust_for_ambient_noise(source, duration=1)
            self.reconhecedor.dynamic_energy_threshold = True

        self.log(f"Núcleo {self.nome_projeto} online.", Fore.RED)
        falar(f"Sistema {self.nome_projeto} ativo. Às suas ordens, Senhor {self.nome_usuario}.")

        while True:
            if self.interface: self.interface.mudar_status("STANDBY", "#005555")
            
            ativacao = capturar_voz(self.reconhecedor, timeout=None, phrase_limit=5)
            
            if ativacao and any(word in ativacao.lower() for word in self.cfg.WAKE_WORDS):
                if self.interface: self.interface.mudar_status("OUVINDO", "#00fbff")
                falar("Sim Senhor.")
                
                while True:
                    comando = capturar_voz(self.reconhecedor, timeout=8, phrase_limit=10)
                    if not comando: break
                    
                    comando = comando.lower().strip()
                    self.log(f"[OUVIDO]: {comando}", Fore.BLUE)

                    if any(cmd in comando for cmd in self.cfg.CMD_DESLIGAR):
                        falar("Desativando núcleo neural. Até logo, Senhor.")
                        encerrar_projeto()

                    elif any(cmd in comando for cmd in self.cfg.CMD_DESATIVAR_VOZ):
                        falar("Entrando em modo de espera.")
                        break

                    elif "verificar computador" in comando:
                        self.executar_diagnostico()

                    else:
                        # CHAMA A INTELIGÊNCIA NA NUVEM (RAILWAY)
                        resposta = chamar_feni_na_nuvem(comando)
                        self.log(f"Feni: {resposta}", Fore.GREEN)
                        falar(resposta)