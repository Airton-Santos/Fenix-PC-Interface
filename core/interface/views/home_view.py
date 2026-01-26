import flet as ft
import time

class HomeView(ft.Container):
    def __init__(self):
        super().__init__(expand=True)
        self.padding = 10
        
        # Lista de mensagens (Console)
        self.console_output = ft.ListView(
            expand=True,
            spacing=5,
            auto_scroll=True,
        )

        # Layout da Home
        self.content = ft.Column(
            controls=[
                ft.Text("TERMINAL DE COMANDO", size=18, weight="bold", color="#00fbff", font_family="Orbitron"),
                ft.Container(
                    content=self.console_output,
                    expand=True,
                    bgcolor="#050505",
                    border=ft.border.all(1, "#1f1f1f"),
                    border_radius=10,
                    padding=15,
                ),
            ]
        )

    def log_msg(self, msg):
        """Adiciona mensagens ao console com timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        nova_linha = ft.Text(
            f"[{timestamp}] > {msg}",
            color="#00fbff",
            font_family="Consolas",
            size=13
        )
        self.console_output.controls.append(nova_linha)
        try:
            self.page.update()
        except:
            pass