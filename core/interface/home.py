# core/interface/home.py
import customtkinter as ctk
import time

class HomeTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")

        # Aba Console (Onde a mágica acontece)
        self.textbox = ctk.CTkTextbox(
            self, 
            fg_color="#050505", 
            border_color="#1f1f1f", 
            border_width=1, 
            text_color="#00fbff", 
            font=("Consolas", 13),
            activate_scrollbars=True
        )
        self.textbox.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Bloqueia edição manual para ser apenas um console de saída
        self.textbox.configure(state="disabled")

    def log_msg(self, msg):
        """Adiciona as falas e logs no console estilo Matrix"""
        self.textbox.configure(state="normal") # Libera para escrita
        timestamp = time.strftime("%H:%M:%S")
        self.textbox.insert("end", f"[{timestamp}] > {msg}\n")
        self.textbox.see("end")
        self.textbox.configure(state="disabled") # Bloqueia novamente