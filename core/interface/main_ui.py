# No topo do core/interface/main_ui.py
import customtkinter as ctk
import psutil
from core.interface.home import HomeTab
from core.interface.monitoramento import MonitoramentoTab
from core.interface.config import ConfigTab

class FenixUI(ctk.CTk):
    def __init__(self, brain_callback=None):
        super().__init__()
        self.title("PROJECT FENIX - CORE SYSTEM")
        self.geometry("1100x750")
        self.configure(fg_color="#0a0a0a")

        # Grid Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()

        # Sistema de Abas
        self.tabview = ctk.CTkTabview(self, fg_color="#0a0a0a", segmented_button_selected_color="#00fbff")
        self.tabview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        tab_home = self.tabview.add("CONSOLE")
        tab_monitor = self.tabview.add("MONITORAMENTO")
        tab_config = self.tabview.add("CONFIGURAÇÕES")

        # Instanciar abas e expandir
        self.home = HomeTab(tab_home)
        self.home.pack(fill="both", expand=True)

        self.monitor = MonitoramentoTab(tab_monitor, brain_callback=brain_callback)
        self.monitor.pack(fill="both", expand=True)

        self.config = ConfigTab(tab_config)
        self.config.pack(fill="both", expand=True)

        self.update_metrics()

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#111111", border_width=1, border_color="#1f1f1f")
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self.sidebar, text="FÊNIX", font=("Orbitron", 35, "bold"), text_color="#00fbff").pack(pady=(30, 10))
        
        # --- TELEMETRIA RAM ---
        self.ram_label = ctk.CTkLabel(self.sidebar, text="MEMORY USAGE: 0%", font=("Consolas", 12), text_color="#00fbff")
        self.ram_label.pack(pady=(20, 5))
        self.ram_bar = ctk.CTkProgressBar(self.sidebar, width=200, height=8, progress_color="#00fbff", fg_color="#051a1a")
        self.ram_bar.set(0)
        self.ram_bar.pack()

        # --- TELEMETRIA CPU ---
        self.cpu_label = ctk.CTkLabel(self.sidebar, text="CPU LOAD: 0%", font=("Consolas", 12), text_color="#00fbff")
        self.cpu_label.pack(pady=(20, 5))
        self.cpu_bar = ctk.CTkProgressBar(self.sidebar, width=200, height=8, progress_color="#00fbff", fg_color="#051a1a")
        self.cpu_bar.set(0)
        self.cpu_bar.pack()

        self.status_led = ctk.CTkLabel(self.sidebar, text="● SYSTEM READY", text_color="#00fbff", font=("Consolas", 11))
        self.status_led.pack(side="bottom", pady=20)

    def update_metrics(self):
        ram = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent()
        self.ram_bar.set(ram / 100)
        self.ram_label.configure(text=f"MEMORY USAGE: {ram}%")
        self.cpu_bar.set(cpu / 100)
        self.cpu_label.configure(text=f"CPU LOAD: {cpu}%")
        self.after(2000, self.update_metrics)

    def log_msg(self, msg):
        self.home.log_msg(msg)

    def mudar_status(self, status, cor):
        self.status_led.configure(text=f"● {status}", text_color=cor)