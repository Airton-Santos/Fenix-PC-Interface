import os
import sys
import warnings
import threading
from core.interface.main_ui import FenixUI
from core.brain import FenixBrain

# Silenciar avisos e prompts desnecessários
warnings.filterwarnings("ignore", category=UserWarning)
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

def rodar_sistema(fenix_instancia):
    """Executa o loop principal do cérebro"""
    try:
        fenix_instancia.start()
    except Exception as e:
        print(f"Erro crítico no núcleo: {e}")

if __name__ == "__main__":
    # 1. Instanciar o Cérebro primeiro (sem iniciar o loop ainda)
    brain = FenixBrain(nome_usuario="Airton") 

    # 2. Criar a Interface passando o callback do cérebro
    # Isso permite que, ao clicar num botão, a UI avise o Brain
    app = FenixUI(brain_callback=brain.processar_comando_manual)
    
    # 3. Vincular a interface ao cérebro para que o Brain consiga usar o app.log_msg
    brain.interface = app

    # 4. Configurar e disparar a Thread do Cérebro
    # daemon=True garante que o cérebro morra se você fechar a janela
    brain_thread = threading.Thread(target=rodar_sistema, args=(brain,), daemon=True)
    
    # Opcional: Você pode iniciar aqui ou vincular ao botão "SISTEMA ON"
    # Para teste imediato, vamos iniciar:
    brain_thread.start()

    # 5. Inicia o loop da Interface (Bloqueante)
    app.log_msg("Sistemas integrados. Núcleo Fenix Online.")
    app.mainloop()