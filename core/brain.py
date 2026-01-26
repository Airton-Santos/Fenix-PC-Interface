import asyncio
import threading
import speech_recognition as sr
from core.stt import capturar_voz
from core.config_audio import ConfigAudio
from core.connect_api import chamar_fenix_na_nuvem 
from core.audio_engine import processo_falar

class FenixBrain:
    def __init__(self, interface=None, nome_usuario="Airton"):
        self.interface = interface
        self.nome_usuario = nome_usuario
        self.esta_falando = False
        self.mic_ativo = True
        
        # Identidade
        self.nome_projeto = "FENIX"
        
        # Áudio e Reconhecimento
        self.cfg = ConfigAudio()
        self.reconhecedor = self.cfg.configurar_reconhecedor(sr.Recognizer())

    def log(self, mensagem):
        """Exibe logs no console e na interface Flet"""
        print(f"[LOG]: {mensagem}")
        if self.interface:
            self.interface.log_msg(mensagem)

    def falar(self, texto):
        """Motor de voz assíncrono"""
        if not texto: return
        
        def rodar():
            self.esta_falando = True
            asyncio.run(processo_falar(texto))
            self.esta_falando = False

        threading.Thread(target=rodar, daemon=True).start()

    def processar_comando_manual(self, texto_digitado):
        """Para quando você digitar algo na interface em vez de falar"""
        if self.interface: self.interface.mudar_status("PENSANDO", "#FFA500")
        resposta = chamar_fenix_na_nuvem(texto_digitado)
        self.log(f"Fenix (Texto): {resposta}")
        self.falar(resposta)

    def start(self):
        """Loop de conversação contínua"""
        self.log("Calibrando microfone...")
        try:
            with sr.Microphone() as source:
                self.reconhecedor.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            self.log(f"Erro de Hardware: {e}")
            return

        self.log(f"Núcleo {self.nome_projeto} Online.")
        self.falar(f"Sistema ativo. Estou ouvindo, Senhor {self.nome_usuario}.")

        while True:
            # Só ouvimos se a IA não estiver falando e o mic estiver ligado
            if not self.esta_falando and self.mic_ativo:
                if self.interface: self.interface.mudar_status("STANDBY", "#005555")
                
                # Captação de voz
                fala_usuario = capturar_voz(self.reconhecedor)
                
                if fala_usuario:
                    msg = fala_usuario.lower()
                    self.log(f"Você: {fala_usuario}")

                    # 1. Verificação de Palavra de Ativação (Wake Word)
                    if any(word in msg for word in self.cfg.WAKE_WORDS):
                        if self.interface: self.interface.mudar_status("OUVINDO", "#00fbff")
                        
                        # Extrai o que foi dito após o nome "Fenix"
                        # (O Grok processa melhor se mandarmos a frase completa)
                        resposta = chamar_fenix_na_nuvem(fala_usuario)
                        
                        if self.interface: self.interface.mudar_status("PENSANDO", "#FFA500")
                        self.log(f"Fenix: {resposta}")
                        self.falar(resposta)
            
            # Pequeno respiro para o processador
            asyncio.run(asyncio.sleep(0.3))