import flet as ft

class ProtocolView(ft.Container):
    def __init__(self):
        super().__init__(expand=True, bgcolor="#0a0a0a")
        self.padding = 30
        
        self.content = ft.Column(
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=[
                ft.Text("MANUAL DE PROTOCOLOS", size=24, weight="bold", color="#00fbff", font_family="Orbitron"),
                ft.Divider(color="#1f1f1f", height=20),
                
                # --- SEÇÃO: SISTEMA ---
                self.criar_cabecalho(ft.Icons.SETTINGS_REMOTE, "SISTEMA E HARDWARE"),
                self.comando_item("Fenix, status do sistema", "Exibe logs de CPU e RAM."),
                self.comando_item("Fenix, limpar console", "Limpa o histórico de mensagens."),
                self.comando_item("Fenix, modo silêncio", "Desativa a voz da IA."),

                ft.Container(height=20),

                # --- SEÇÃO: MEMÓRIA (ANOTAÇÕES) ---
                self.criar_cabecalho(ft.Icons.MEMORY, "MEMÓRIA E APRENDIZADO"),
                self.comando_item("Fenix, novo amigo", "Adiciona alguém à lista 'amigos'."),
                self.comando_item("Fenix, comida favorita", "Registra preferências na categoria 'comida'."),
                self.comando_item("Fenix, novo conhecimento", "Compartilha aprendizados para a categoria 'trabalho'."),
                self.comando_item("Fenix, redes sociais", "Atualiza informações em 'rede_social'."),
                self.comando_item("Fenix, nova preferencia", "Adiciona hobbies à categoria 'hobby'."),

                ft.Container(height=20),

                # --- SEÇÃO: REMOÇÃO ---
                self.criar_cabecalho(ft.Icons.DELETE_SWEEP, "REMOVER INFORMAÇÕES"),
                self.comando_item("Fenix, remover amigo", "Retira um contato da lista de amigos."),
                self.comando_item("Fenix, remover informação", "Remove dados da categoria 'pessoal'."),
                self.comando_item("Fenix, limpar rede social", "Deleta registros de redes sociais."),

                ft.Container(height=40),
            ]
        )

    def criar_cabecalho(self, icone, titulo):
        """Usa a lógica que você validou: Container + Icon constante"""
        return ft.Container(
            content=ft.Row([
                ft.Icon(icone, color="#00fbff", size=20), 
                ft.Text(titulo, weight="bold", color="#555555")
            ], spacing=10),
            padding=ft.padding.only(bottom=10),
            bgcolor="transparent"
        )

    def comando_item(self, comando, desc):
        """Item de comando com fundo escuro e borda ciano fina"""
        return ft.Container(
            width=float("inf"), 
            content=ft.Column([
                ft.Text(comando, color="#00fbff", weight="bold", size=16),
                ft.Text(desc, color="#888888", size=14),
            ], spacing=5, tight=True),
            padding=15,
            bgcolor="#111111",
            border_radius=10,
            border=ft.border.all(1, "#1f1f1f"),
            margin=ft.margin.only(bottom=10)
        )