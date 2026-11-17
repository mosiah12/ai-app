from ai import generate_response_stream
import flet as ft
import asyncio

async def load_response(message: str, text_instance: ft.Text):
    generator = generate_response_stream(message)
    first_token = True
    try:
        while True:
            token = await asyncio.to_thread(next, generator, None)
            if token is None:
                break
            if first_token:
                text_instance.value = ""
                first_token = False

            text_instance.value += token
            text_instance.update()
    except Exception:
        pass
    finally:
        generator.close()
