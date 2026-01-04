import sys, os, asyncio, threading, uuid
from colorama import Fore, Style, init
import speech_recognition as sr
import edge_tts
import pygame

# Importações do seu projeto
from core.stt import capturar_voz
from core.config_audio import ConfigAudio
from core.system import obter_processos_pesados, saude_hardware, limpar_temporarios, encerrar_projeto, analisar_conexoes
from core.connect_api import chamar_feni_na_nuvem 

init(autoreset=True)
pygame.mixer.init()

async def falar_async(texto):
    voice = "pt-BR-AntonioNeural"
    id_sessao = str(uuid.uuid4())[:8]
    output_file = f"res_{id_sessao}.mp3"
    
    try:
        communicate = edge_tts.Communicate(texto, voice)
        await communicate.save(output_file)
        await asyncio.sleep(0.2) 

        if os.path.exists(output_file):
            pygame.mixer.music.load(output_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
            pygame.mixer.music.unload() 
            try:
                os.remove(output_file)
            except:
                pass
    except Exception as e:
        print(f"{Fore.RED}Erro no protocolo de voz: {e}{Style.RESET_ALL}")

def falar(texto):
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
        self.log(f"COMANDO MANUAL: {comando.upper()}", Fore.CYAN)
        if comando == "processos":
            falar("Analisando processos pesados.")
            falar(obter_processos_pesados())
        elif comando == "hardware":
            falar("Verificando saúde do hardware.")
            falar(saude_hardware())
        elif comando == "limpeza":
            falar("Iniciando limpeza de arquivos temporários.")
            falar(limpar_temporarios())
        elif comando == "rede":
            falar("Analisando conexões de rede.")
            falar(analisar_conexoes())

    def executar_diagnostico(self):
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

    def start(self):
        self.log("Calibrando sensores acústicos...", Fore.YELLOW)
        with sr.Microphone() as source:
            self.reconhecedor.adjust_for_ambient_noise(source, duration=1)
        
        self.log(f"Núcleo {self.nome_projeto} online (Via Groq Cloud).", Fore.RED)
        falar(f"Sistema {self.nome_projeto} ativo. Às suas ordens, Senhor {self.nome_usuario}.")

        while True:
            if self.interface: self.interface.mudar_status("STANDBY", "#005555")
            
            ativacao = capturar_voz(self.reconhecedor, timeout=None)
            
            if ativacao and any(word in ativacao.lower() for word in self.cfg.WAKE_WORDS):
                if self.interface: self.interface.mudar_status("OUVINDO", "#00fbff")
                falar("Sim Senhor.")
                
                while True:
                    comando = capturar_voz(self.reconhecedor, timeout=8)
                    if not comando: break
                    
                    self.log(f"[OUVIDO]: {comando}", Fore.BLUE)

                    # Comandos Críticos
                    if any(cmd in comando.lower() for cmd in self.cfg.CMD_DESLIGAR):
                        falar("Desativando núcleo neural. Até logo.")
                        encerrar_projeto()
                    elif any(cmd in comando.lower() for cmd in self.cfg.CMD_DESATIVAR_VOZ):
                        falar("Entrando em modo de espera.")
                        break
                    elif "verificar computador" in comando.lower():
                        self.executar_diagnostico()
                    else:
                        # Envio direto para a Groq (via Railway)
                        if self.interface: self.interface.mudar_status("PENSANDO", "#FFA500")
                        resposta = chamar_feni_na_nuvem(comando)
                        
                        if self.interface: self.interface.mudar_status("FENI ONLINE", "#00fbff")
                        self.log(f"Feni: {resposta}", Fore.GREEN)
                        falar(resposta)