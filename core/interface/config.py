import customtkinter as ctk

class ConfigTab(ctk.CTkFrame):
    def __init__(self, master, brain_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.brain_callback = brain_callback # Recebe o comando para o cérebro
        self.configure(fg_color="transparent")

        self.label = ctk.CTkLabel(self, text="PROTOCOLOS DE CONFIGURAÇÃO", 
                                  font=("Orbitron", 18, "bold"), text_color="#00fbff")
        self.label.pack(pady=30)

        # --- CONTROLE DE VOLUME ---
        self.vol_label = ctk.CTkLabel(self, text="VOLUME DO SISTEMA", font=("Consolas", 13), text_color="#00fbff")
        self.vol_label.pack(pady=(10, 5))
        
        self.vol_slider = ctk.CTkSlider(
            self, from_=0, to=1, 
            command=self.ajustar_volume, # Chama a função abaixo
            button_color="#00fbff", progress_color="#00fbff"
        )
        self.vol_slider.set(0.8)
        self.vol_slider.pack(pady=10, padx=80, fill="x")

        # --- SENSIBILIDADE DO MICROFONE ---
        self.mic_label = ctk.CTkLabel(self, text="SENSIBILIDADE DO MICROFONE", font=("Consolas", 13), text_color="#00fbff")
        self.mic_label.pack(pady=(30, 5))
        
        self.mic_slider = ctk.CTkSlider(
            self, from_=20, to=500, # Escala de sensibilidade do SpeechRecognition
            command=self.ajustar_mic, # Chama a função abaixo
            button_color="#00fbff", progress_color="#00fbff"
        )
        self.mic_slider.set(80) 
        self.mic_slider.pack(pady=10, padx=80, fill="x")

    def ajustar_volume(self, valor):
        if self.brain_callback:
            # Envia o comando "volume:0.8" por exemplo
            self.brain_callback(f"set_volume:{valor}")

    def ajustar_mic(self, valor):
        if self.brain_callback:
            # Envia o comando "mic:100" para ajustar o threshold
            self.brain_callback(f"set_mic:{valor}")