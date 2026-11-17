from chat import load_response
import flet as ft
import os

async def main(page: ft.Page):
    page.title = "Assistente IA"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F1117"
    page.padding = 20

    page.window.width = 800
    page.window.height = 800

    current_dir = os.path.dirname(os.path.abspath(__file__))
    page.window.icon = os.path.join(current_dir, "assets", "icon.ico")

    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.AUTO_AWESOME, color=ft.Colors.BLUE_400, size=24),
                ft.Text("Assistente Local", size=18, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.Padding.only(bottom=15),
        border=ft.Border.only(bottom=ft.BorderSide(1, ft.Colors.WHITE_10)),
    )

    chat_list = ft.ListView(
        expand=True,
        spacing=12,
        auto_scroll=True,
        padding=ft.Padding.symmetric(vertical=10),
    )

    def create_bubble(text_control: ft.Control, is_user: bool):
        return ft.Row(
            controls=[
                ft.Container(
                    content=text_control,
                    bgcolor=ft.Colors.BLUE_800 if is_user else "#1E222D",
                    padding=ft.Padding.symmetric(horizontal=16, vertical=12),
                    border_radius=ft.BorderRadius.only(
                        top_left=16,
                        top_right=16,
                        bottom_left=16 if is_user else 4,
                        bottom_right=4 if is_user else 16,
                    ),
                    border=None if is_user else ft.Border.all(1, ft.Colors.WHITE_10),
                    width=550,
                )
            ],
            alignment=ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START,
        )

    async def process_chat(message: str):
        text_field.disabled = True
        send_button.disabled = True

        user_msg = ft.Text(message, size=15, color=ft.Colors.WHITE)
        chat_list.controls.append(create_bubble(user_msg, is_user=True))

        ai_msg = ft.Text("Pensando...", size=15, color=ft.Colors.GREY_200, selectable=True)
        chat_list.controls.append(create_bubble(ai_msg, is_user=False))
        page.update()

        await load_response(message, ai_msg)

        text_field.disabled = False
        send_button.disabled = False
        page.update()
        await text_field.focus()

    def on_send(e):
        msg = text_field.value.strip()
        if not msg:
            return
        text_field.value = ""
        page.run_task(process_chat, msg)

    text_field = ft.TextField(
        hint_text="Pergunte qualquer coisa...",
        expand=True,
        border_radius=24,
        filled=True,
        bgcolor="#1E222D",
        border_color=ft.Colors.WHITE_12,
        focused_border_color=ft.Colors.BLUE_400,
        content_padding=ft.Padding.symmetric(horizontal=20, vertical=14),
        on_submit=on_send,
    )

    send_button = ft.IconButton(
        icon=ft.Icons.SEND_ROUNDED,
        icon_color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_600,
        on_click=on_send,
    )

    user_area = ft.Container(
        content=ft.Row(controls=[text_field, send_button], spacing=10),
        padding=ft.Padding.only(top=10),
    )

    page.add(header, chat_list, user_area)
    page.update()

    await page.window.center()
    page.window.visible = True
    page.update()

    page.run_task(process_chat, "Olá! Quem é você e o que você sabe fazer?")

ft.run(main, assets_dir="assets", view=ft.AppView.FLET_APP_HIDDEN)