import sys, os, asyncio, threading, uuid
from colorama import Fore, Style, init
import speech_recognition as sr
import edge_tts
import pygame

# Importações do seu projeto
from core.stt import capturar_voz
from core.config_audio import ConfigAudio
from core.system import obter_processos_pesados, saude_hardware, limpar_temporarios, encerrar_projeto, analisar_conexoes
from core.connect_api import chamar_fenix_na_nuvem 

init(autoreset=True)
pygame.mixer.init()

class FenixBrain:
    def __init__(self, interface=None, nome_usuario="Airton"):
        self.esta_falando = False  
        self.mic_ativo = True      # Controle de estado para desligar/ligar o mic
        self.nome_ia = "Fenix"
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

    async def falar_async(self, texto):
        self.esta_falando = True 
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
                
                pygame.mixer.music.unload() # Libera o arquivo para exclusão
                
                # LIMPEZA RIGOROSA DO ARQUIVO
                if os.path.exists(output_file):
                    os.remove(output_file)
                    
        except Exception as e:
            self.log(f"Erro no áudio ou limpeza: {e}", Fore.RED)
        finally:
            await asyncio.sleep(0.6) # Espera o som dissipar no ambiente
            self.esta_falando = False 

    def falar(self, texto):
        threading.Thread(target=lambda: asyncio.run(self.falar_async(texto)), daemon=True).start()

    def processar_comando_manual(self, comando):
        self.log(f"COMANDO MANUAL: {comando.upper()}", Fore.CYAN)
        if comando == "processos":
            self.falar(obter_processos_pesados())
        elif comando == "hardware":
            self.falar(saude_hardware())
        elif comando == "limpeza":
            self.falar(limpar_temporarios())
        elif comando == "rede":
            self.falar(analisar_conexoes())

    def executar_diagnostico(self):
        self.falar("O que o senhor deseja verificar no sistema?") 
        while self.esta_falando: asyncio.run(asyncio.sleep(0.1))
        
        escolha = capturar_voz(self.reconhecedor, timeout=7)
        if not escolha: return
        escolha = escolha.lower()
        
        if "processos" in escolha or "memória" in escolha:
            self.falar(obter_processos_pesados())
        elif "saúde" in escolha or "hardware" in escolha:
            self.falar(saude_hardware())
        elif "limpeza" in escolha or "temporários" in escolha:
            self.falar(limpar_temporarios())
        elif "rede" in escolha or "conexão" in escolha:
            self.falar(analisar_conexoes())

    def start(self):
        self.log("Calibrando sensores acústicos...", Fore.YELLOW)
        with sr.Microphone() as source:
            self.reconhecedor.adjust_for_ambient_noise(source, duration=1)
        
        self.log(f"Núcleo {self.nome_projeto} online.", Fore.RED)
        self.falar(f"Sistema {self.nome_projeto} ativo. Às suas ordens, Senhor {self.nome_usuario}.")

        while True:
            # SÓ ESCUTA SE: Mic estiver ativo via voz E IA não estiver falando
            if not self.esta_falando:
                if self.mic_ativo:
                    if self.interface: self.interface.mudar_status("STANDBY", "#005555")
                    
                    ativacao = capturar_voz(self.reconhecedor, timeout=None)
                    
                    if ativacao:
                        msg = ativacao.lower()
                        self.log(f"DEBUG - Ouvido: {msg}", Fore.YELLOW)

                        # COMANDO PARA DESLIGAR O MICROFONE
                        if "desligar microfone" in msg:
                            self.falar("Entendido. Desligando captação de áudio.")
                            self.mic_ativo = False
                            if self.interface: self.interface.mudar_status("MIC OFF", "#800000")
                            continue

                        # GATILHO DE ATIVAÇÃO
                        if any(word in msg for word in self.cfg.WAKE_WORDS):
                            if self.interface: self.interface.mudar_status("OUVINDO", "#00fbff")
                            self.falar("Sim Senhor.")
                            while self.esta_falando: asyncio.run(asyncio.sleep(0.1))

                            while True:
                                comando = capturar_voz(self.reconhecedor, timeout=8)
                                if not comando: break
                                self.log(f"[OUVIDO]: {comando}", Fore.BLUE)

                                if any(cmd in comando.lower() for cmd in self.cfg.CMD_DESLIGAR):
                                    self.falar("Desativando núcleo neural. Até logo.")
                                    encerrar_projeto()
                                elif any(cmd in comando.lower() for cmd in self.cfg.CMD_DESATIVAR_VOZ):
                                    self.falar("Entrando em modo de espera.")
                                    break
                                elif "verificar computador" in comando.lower():
                                    self.executar_diagnostico()
                                    while self.esta_falando: asyncio.run(asyncio.sleep(0.1))
                                else:
                                    if self.interface: self.interface.mudar_status("PENSANDO", "#FFA500")
                                    resposta = chamar_fenix_na_nuvem(comando)
                                    self.log(f"Fenix: {resposta}", Fore.GREEN)
                                    self.falar(resposta)
                                    while self.esta_falando: asyncio.run(asyncio.sleep(0.1))
                else:
                    # Se o mic está inativo, ele só volta a escutar se ouvir "Fenix"
                    # ou comando de ativação (escuta mínima)
                    escuta_reativacao = capturar_voz(self.reconhecedor, timeout=2)
                    if escuta_reativacao and any(word in escuta_reativacao.lower() for word in self.cfg.WAKE_WORDS):
                        self.mic_ativo = True
                        self.falar("Microfone reativado. Como posso ajudar?")
            else:
                asyncio.run(asyncio.sleep(0.2))