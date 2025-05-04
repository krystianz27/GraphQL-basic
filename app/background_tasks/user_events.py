import asyncio
import json

from app.background_tasks.user_queue import user_created_queue


async def process_user_created_queue():
    while True:
        message_json = await user_created_queue.get()
        user_data = json.loads(message_json)
        print(f"Przetwarzam zdarzenie utworzenia użytkownika: {user_data}")
        # Tutaj umieść logikę przetwarzania (np. wysyłanie e-maili)
        await asyncio.sleep(1)  # Dodano dla przykładu, aby nie zalewać konsoli
        user_created_queue.task_done()
