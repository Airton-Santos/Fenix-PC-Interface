# core/config_audio.py
import speech_recognition as sr

class ConfigAudio:
    def __init__(self):
        # Ajuste de sensibilidade (80 é bom para microfones sensíveis)
        self.ENERGY_THRESHOLD = 650
        self.PAUSE_THRESHOLD = 0.9
        self.DYNAMIC_ENERGY = False
        
        # Palavras que despertam a Feni
        self.WAKE_WORDS = ["fênix", "fenix"]
        
        # Comandos críticos de sistema
        self.CMD_DESLIGAR = ["desligar projeto fênix", "desligar fenix", "encerrar sistema"]
        self.CMD_DESATIVAR_VOZ = ["descansar", "esperar", "ficar em espera", "parar de ouvir"]
        self.CMD_VERIFICAR_PC = ["verificar computador", "diagnóstico", "status do sistema"]

    def configurar_reconhecedor(self, reconhecedor):
        reconhecedor.energy_threshold = self.ENERGY_THRESHOLD
        reconhecedor.pause_threshold = self.PAUSE_THRESHOLD
        reconhecedor.dynamic_energy_threshold = self.DYNAMIC_ENERGY
        return reconhecedor