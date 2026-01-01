import customtkinter as ctk

class MonitoramentoTab(ctk.CTkFrame):
    def __init__(self, master, brain_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")
        self.brain_callback = brain_callback

        self.grid_columnconfigure((0, 1), weight=1)
        
        funcoes = [
            ("LISTA DE PROCESSOS", "Gerenciar RAM", "processos"),
            ("SAÚDE HARDWARE", "CPU e Disco", "hardware"),
            ("LIMPEZA TEMP", "Otimizar Sistema", "limpeza"),
            ("ANALISAR REDE", "Tráfego Web", "rede"),
            ("ENCERRAR APPS", "Matar Processo", "encerrar")
        ]

        for i, (nome, desc, cmd) in enumerate(funcoes):
            # O ajuste está aqui: cmd=cmd dentro do lambda garante o comando correto
            btn = ctk.CTkButton(self, 
                                text=f"{nome}\n{desc}", 
                                font=("Consolas", 12, "bold"),
                                fg_color="#111111",
                                border_width=1,
                                border_color="#1f1f1f",
                                hover_color="#0a2a2a",
                                text_color="#00fbff",
                                height=100,
                                command=lambda c=cmd: self.btn_callback(c)) 
            
            btn.grid(row=i//2, column=i%2, padx=15, pady=15, sticky="nsew")

    def btn_callback(self, comando):
        if self.brain_callback:
            # Feedback visual no console do VSCode para o senhor monitorar
            print(f">>> Interface: Solicitando {comando} ao núcleo...")
            self.brain_callback(comando)