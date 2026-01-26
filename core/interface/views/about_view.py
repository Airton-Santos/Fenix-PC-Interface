import flet as ft
import webbrowser

class AboutView(ft.Container):
    def __init__(self):
        super().__init__(expand=True)
        self.padding = 30
        
        # Usando exatamente o mesmo estilo que funciona na sua Sidebar
        nav_style = ft.ButtonStyle(
            color="#ffffff",
            overlay_color="#1a1a1a",
            shape=ft.RoundedRectangleBorder(radius=8),
        )

        self.content = ft.Column(
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=[
                ft.Text("NÚCLEO FENIX - SOBRE", size=24, weight="bold", color="#00fbff", font_family="Orbitron"),
                ft.Divider(color="#1f1f1f", height=30),
                
                ft.Text("SISTEMA OPERACIONAL", size=16, weight="bold", color="#555555"),
                ft.Text(
                    "O Projeto Fenix é o seu terminal pessoal de automação e inteligência.",
                    color="#bbbbbb"
                ),
                
                ft.Container(height=20),
                
                # Botões idênticos aos da Sidebar
                ft.Row([
                    ft.TextButton(
                        "MEU GITHUB", 
                        icon="code", 
                        style=nav_style, 
                        on_click=lambda _: webbrowser.open("https://github.com/Airton-Santos")
                    ),
                    ft.TextButton(
                        "PORTFÓLIO", 
                        icon="language", 
                        style=nav_style, 
                        on_click=lambda _: webbrowser.open("https://seu-portfolio.com")
                    ),
                ], spacing=20),
                
                ft.Container(height=40),
                ft.Text("CRÉDITOS", size=16, weight="bold", color="#555555"),
                ft.Text("Operador: Fenix (Airton)", color="#00fbff"),
            ]
        )