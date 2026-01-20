import sys, os, asyncio, threading, uuid
from colorama import Fore, Style, init
import speech_recognition as sr
import edge_tts
import pygame

# --- IMPORTAÇÕES DE MÓDULOS INTERNOS ---
from core.stt import capturar_voz
from core.config_audio import ConfigAudio
from core.system import (
    obter_processos_pesados, saude_hardware, limpar_temporarios, 
    encerrar_projeto, analisar_conexoes, processar_intencao_sistema
)
from core.connect_api import chamar_fenix_na_nuvem 
from core.audio_engine import processo_falar

# Inicialização de bibliotecas gráficas e de áudio
init(autoreset=True)
pygame.mixer.init()

class FenixBrain:
    def __init__(self, interface=None, nome_usuario="Airton"):
        # Estados de controle
        self.esta_falando = False  
        self.mic_ativo = True      
        
        # Identidade do Projeto
        self.nome_ia = "Fenix"
        self.nome_projeto = "FENIX"
        self.nome_usuario = nome_usuario
        
        # Componentes de áudio e reconhecimento
        self.interface = interface 
        self.cfg = ConfigAudio()
        self.reconhecedor = sr.Recognizer()
        self.reconhecedor = self.cfg.configurar_reconhecedor(self.reconhecedor)

    def log(self, mensagem, cor=Fore.WHITE):
        """Exibe mensagens no terminal e na interface visual"""
        print(f"{cor}{mensagem}{Style.RESET_ALL}")
        if self.interface:
            self.interface.log_msg(mensagem)

    # --- MOTOR DE VOZ ---
    def falar(self, texto):
        """Dispara a voz em uma Thread separada para não travar o código"""
        def rodar():
            self.esta_falando = True
            asyncio.run(processo_falar(texto))
            self.esta_falando = False

        threading.Thread(target=rodar, daemon=True).start()

    # --- COMANDOS VIA TEXTO/BOTÃO ---
    def processar_comando_manual(self, comando):
        """Executa funções de sistema diretamente, sem usar voz"""
        self.log(f"COMANDO MANUAL: {comando.upper()}", Fore.CYAN)
        if comando == "processos":
            self.falar(obter_processos_pesados())
        elif comando == "hardware":
            self.falar(saude_hardware())
        elif comando == "limpeza":
            self.falar(limpar_temporarios())
        elif comando == "rede":
            self.falar(analisar_conexoes())

    # --- LÓGICA DE DIAGNÓSTICO POR VOZ ---
    def executar_diagnostico(self):
        """Inicia o diálogo de verificação de hardware"""
        self.falar("O que deseja verificar?")
        while self.esta_falando: asyncio.run(asyncio.sleep(0.1))
        
        escolha = capturar_voz(self.reconhecedor)
        if escolha:
            # Envia a voz para o system.py decidir qual função rodar
            resultado = processar_intencao_sistema(escolha)
            
            if resultado:
                self.falar(resultado)
            else:
                self.falar("Não identifiquei esse protocolo de diagnóstico.")

    # --- NÚCLEO DE OPERAÇÃO (LOOP PRINCIPAL) ---
    def start(self):
        """Inicia a calibração e o loop infinito de escuta"""
        self.log("Calibrando sensores acústicos...", Fore.YELLOW)
        with sr.Microphone() as source:
            self.reconhecedor.adjust_for_ambient_noise(source, duration=1)
        
        self.log(f"Núcleo {self.nome_projeto} online.", Fore.RED)
        self.falar(f"Sistema {self.nome_projeto} ativo. Às suas ordens, Senhor {self.nome_usuario}.")

        while True:
            # BLOCO 1: Verificação de silêncio (IA não fala e Mic está ON)
            if not self.esta_falando:
                if self.mic_ativo:
                    if self.interface: self.interface.mudar_status("STANDBY", "#005555")
                    
                    # Escuta passiva aguardando a Wake Word (Palavra de ativação)
                    ativacao = capturar_voz(self.reconhecedor, timeout=None)
                    
                    if ativacao:
                        msg = ativacao.lower()
                        self.log(f"DEBUG - Ouvido: {msg}", Fore.YELLOW)

                        # Ação: Desligar captação
                        if "desligar microfone" in msg:
                            self.falar("Entendido. Desligando captação de áudio.")
                            self.mic_ativo = False
                            if self.interface: self.interface.mudar_status("MIC OFF", "#800000")
                            continue

                        # BLOCO 2: Se a Wake Word for detectada, entra no modo de COMANDO
                        if any(word in msg for word in self.cfg.WAKE_WORDS):
                            if self.interface: self.interface.mudar_status("OUVINDO", "#00fbff")
                            self.falar("Sim Senhor.")
                            while self.esta_falando: asyncio.run(asyncio.sleep(0.1))

                            # Loop de interação contínua (Conversa aberta)
                            while True:
                                comando = capturar_voz(self.reconhecedor, timeout=8)
                                if not comando: break # Sai do loop se houver silêncio longo
                                self.log(f"[OUVIDO]: {comando}", Fore.BLUE)

                                # Verificação de comandos críticos
                                if any(cmd in comando.lower() for cmd in self.cfg.CMD_DESLIGAR):
                                    self.falar("Desativando núcleo neural. Até logo.")
                                    encerrar_projeto()
                                
                                elif any(cmd in comando.lower() for cmd in self.cfg.CMD_DESATIVAR_VOZ):
                                    self.falar("Entrando em modo de espera.")
                                    break # Volta para o standby
                                
                                elif "verificar computador" in comando.lower():
                                    self.executar_diagnostico()
                                    while self.esta_falando: asyncio.run(asyncio.sleep(0.1))
                                
                                # Processamento de Inteligência Artificial na Nuvem
                                else:
                                    if self.interface: self.interface.mudar_status("PENSANDO", "#FFA500")
                                    resposta = chamar_fenix_na_nuvem(comando)
                                    self.log(f"Fenix: {resposta}", Fore.GREEN)
                                    self.falar(resposta)
                                    while self.esta_falando: asyncio.run(asyncio.sleep(0.1))
                
                # BLOCO 3: Caso o microfone esteja desligado, aguarda reativação
                else:
                    escuta_reativacao = capturar_voz(self.reconhecedor, timeout=2)
                    if escuta_reativacao and any(word in escuta_reativacao.lower() for word in self.cfg.WAKE_WORDS):
                        self.mic_ativo = True
                        self.falar("Microfone reativado. Como posso ajudar?")
            
            # BLOCO 4: Pequena pausa para não sobrecarregar o processador
            else:
                asyncio.run(asyncio.sleep(0.2))