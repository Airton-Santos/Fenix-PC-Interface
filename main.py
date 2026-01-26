import os
import threading
import warnings
import pygame # <--- Adicione aqui
import flet as ft
from core.interface.main_ui import FenixUI
from core.brain import FenixBrain

warnings.filterwarnings("ignore", category=UserWarning)
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

if __name__ == "__main__":
    brain = FenixBrain(nome_usuario="Airton") 
    ui_fenix = FenixUI(brain_callback=brain.processar_comando_manual)
    brain.interface = ui_fenix
    pygame.mixer.init()

    # Inicia cérebro em Thread separada
    threading.Thread(target=brain.start, daemon=True).start()

    # Log inicial antes do loop
    ui_fenix.log_msg("Sistemas integrados. Núcleo Fenix Online.")
    
    print("Iniciando interface Fenix...")
    # Chamada mais estável para v0.80.4
    ft.app(ui_fenix.main)