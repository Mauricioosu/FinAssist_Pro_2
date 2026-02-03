import flet as ft
import asyncio
# Importa do pacote src que está na mesma pasta
from src.ai.controller import AIController
from src.core.database import get_db, init_db

# Configuração de cores
BG_COLOR = "#101216" # Fundo escuro
CHAT_BG = "#1A1D21"  # Fundo do chat
USER_COLOR = "#0D6EFD" # Azul
AI_COLOR = "#212529"   # Cinza escuro

async def main(page: ft.Page):
    page.title = "FinAssist Pro 2 (Desktop)"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG_COLOR
    page.padding = 20
    
    # Inicializa Banco de Dados
    await init_db()

    # Prepara o Controlador de IA
    try:
        ai_session_gen = get_db()
        session = await anext(ai_session_gen)
        controller = AIController(session)
    except Exception as e:
        page.add(ft.Text(f"Erro ao conectar banco: {e}", color="red"))
        return
    
    # --- AQUECIMENTO DA IA ---
    loading_text = ft.Text("🔥 Aquecendo motores da IA... aguarde.", color="orange")
    page.add(loading_text)
    page.update()
    
    # Faz o aquecimento (Protegido contra falhas)
    try:
        await controller.warm_up()
    except:
        pass 
    
    page.remove(loading_text)
    
    # --- ELEMENTOS DA UI ---
    
    # Área onde as mensagens aparecem
    chat_view = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # Campo de texto
    user_input = ft.TextField(
        hint_text="Digite aqui (ex: Gastei 50 no Uber)...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        border_radius=20,
        on_submit=lambda e: asyncio.create_task(send_message(e))
    )

    # Função para adicionar mensagem na tela
    def add_message(text, sender="user"):
        is_user = sender == "user"
        
        # Cores e Ícones (Strings simples)
        avatar_bg = USER_COLOR if is_user else "teal" 
        icon_name = "person" if is_user else "smart_toy"
        
        avatar = ft.CircleAvatar(
            content=ft.Icon(icon_name),
            bgcolor=avatar_bg,
            radius=16,
        )
        
        # Balão de texto
        # REMOVIDO 'constraints' para evitar erro
        # ATUALIZADO 'border_radius' para a nova sintaxe
        bubble = ft.Container(
            content=ft.Markdown(
                text, 
                selectable=True, 
                extension_set=ft.MarkdownExtensionSet.GITHUB_WEB
            ),
            bgcolor=USER_COLOR if is_user else AI_COLOR,
            padding=15,
            border_radius=ft.BorderRadius(
                top_left=15, top_right=15,
                bottom_left=15 if is_user else 0,
                bottom_right=0 if is_user else 15
            )
        )

        # Linha de alinhamento
        row = ft.Row(
            controls=[bubble, avatar] if is_user else [avatar, bubble],
            alignment=ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
        
        chat_view.controls.append(row)
        page.update()

    # Lógica de Envio
    async def send_message(e):
        text = user_input.value
        if not text:
            return

        user_input.value = ""
        user_input.disabled = True
        page.update()

        # 1. Mostra msg do usuário
        add_message(text, "user")

        # 2. Indicador de "Pensando..."
        typing_indicator = ft.Row([
            ft.ProgressRing(width=16, height=16, stroke_width=2),
            ft.Text(" Analisando...", size=12, color="grey")
        ])
        chat_view.controls.append(typing_indicator)
        page.update()

        # 3. Chama a IA
        try:
            response = await controller.process_user_message(text)
        except Exception as err:
            response = f"❌ Erro na IA: {err}"

        # 4. Remove loading e mostra resposta
        chat_view.controls.remove(typing_indicator)
        add_message(response, "ai")
        
        user_input.disabled = False
        user_input.focus()
        page.update()

    # Botão de enviar
    send_btn = ft.IconButton(
        icon="send", 
        icon_color="blue",
        on_click=lambda e: asyncio.create_task(send_message(e))
    )

    # Layout
    input_area = ft.Container(
        content=ft.Row([user_input, send_btn]),
        padding=10,
        bgcolor=CHAT_BG,
        border_radius=20
    )

    page.add(
        ft.Container(content=chat_view, expand=True, padding=10),
        input_area
    )

    # Mensagem de Boas-vindas
    add_message("👋 **Olá! Sou o FinAssist Pro (Desktop).**\n\nPosso registrar transações e tirar dúvidas.\n\nExperimente: *'Gastei 30 no almoço'*", "ai")

if __name__ == "__main__":
    # Sintaxe compatível com versão nova
    ft.app(target=main)