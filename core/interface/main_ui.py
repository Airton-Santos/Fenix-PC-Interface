import flet as ft
import psutil
import threading
import time
from core.interface.views.home_view import HomeView
from core.interface.views.about_view import AboutView
from core.interface.views.ProtocolView import ProtocolView

class FenixUI:
    def __init__(self, brain_callback=None):
        self.brain_callback = brain_callback
        
        # Instanciando as Views
        self.view_home = HomeView()
        self.view_about = AboutView()
        self.view_protocol = ProtocolView()
        
        # Container dinâmico
        self.content_area = ft.Container(content=self.view_home, expand=True)
        
        # Componentes de Hardware
        self.status_led = ft.Text("● STANDBY", color="#005555", size=14, weight="bold")
        self.ram_bar = ft.ProgressBar(width=200, height=8, color="#00fbff", bgcolor="#051a1a")
        self.cpu_bar = ft.ProgressBar(width=200, height=8, color="#ff0055", bgcolor="#1a0505")
        self.ram_text = ft.Text("RAM: 0%", size=12, font_family="Consolas")
        self.cpu_text = ft.Text("CPU: 0%", size=12, font_family="Consolas")

    def main(self, page: ft.Page):
        self.page = page
        self.page.title = "FENIX - NÚCLEO CENTRAL"
        self.page.bgcolor = "#0a0a0a"
        self.page.window_width = 1200
        self.page.window_height = 800
        self.page.padding = 0 
        
        nav_style = ft.ButtonStyle(
            color="#ffffff",
            overlay_color="#1a1a1a",
            shape=ft.RoundedRectangleBorder(radius=8),
        )

        sidebar = ft.Container(
            width=250,
            bgcolor="#111111",
            padding=20,
            border=ft.border.only(right=ft.BorderSide(1, "#1f1f1f")),
            content=ft.Column(
                controls=[
                    ft.Text("FENIX", size=30, weight="bold", color="#00fbff", font_family="Orbitron"),
                    ft.Divider(color="#1f1f1f", height=20),
                    
                    ft.Text("MENU", size=12, color="#555555"),
                    
                    # CORREÇÃO: Usando strings diretas para os ícones
                    ft.TextButton(
                        "INICIO", 
                        icon=ft.Icons.TERMINAL,
                        style=nav_style, 
                        on_click=lambda _: self.navegar("home")
                    ),
                    ft.TextButton(
                        "INFORMAÇÕES", 
                        icon=ft.Icons.SETTINGS, 
                        style=nav_style, 
                        on_click=lambda _: self.navegar("about")
                    ),
                    ft.TextButton(
                        "COMANDOS", 
                        icon=ft.Icons.DESCRIPTION, 
                        style=nav_style, 
                        on_click=lambda _: self.navegar("protocol")
                    ),
                    
                    ft.Divider(color="#1f1f1f", height=40),
                    
                    ft.Text("SISTEMA", size=12, color="#555555"),
                    self.status_led,
                    
                    ft.Divider(color="#1f1f1f", height=40),
                    
                    ft.Text("HARDWARE", size=12, color="#555555"),
                    self.cpu_text, self.cpu_bar,
                    ft.Container(height=10),
                    self.ram_text, self.ram_bar,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START,
            )
        )

        self.page.add(
            ft.Row(
                controls=[
                    sidebar,
                    self.content_area 
                ],
                expand=True,
                spacing=0
            )
        )

        threading.Thread(target=self.update_hardware, daemon=True).start()

    def navegar(self, destino):
        if destino == "home":
            self.content_area.content = self.view_home
        elif destino == "about":
            self.content_area.content = self.view_about
        elif destino == "protocol":
            self.content_area.content = self.view_protocol
        
        self.page.update()

    def mudar_status(self, status, cor):
        self.status_led.value = f"● {status}"
        self.status_led.color = cor
        try: self.page.update()
        except: pass

    def update_hardware(self):
        while True:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            self.cpu_bar.value = cpu / 100
            self.cpu_text.value = f"CPU: {cpu}%"
            self.ram_bar.value = ram / 100
            self.ram_text.value = f"RAM: {ram}%"
            try:
                self.page.update()
            except: break
            time.sleep(1)

    def log_msg(self, msg):
        self.view_home.log_msg(msg)