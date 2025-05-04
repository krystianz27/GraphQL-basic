import json

from app.background_tasks.user_queue import user_created_queue


async def send_user_created_signal(user_id: int, username: str, email: str):
    """
    Symuluje wysłanie sygnału o utworzeniu użytkownika.
    Teraz używamy tylko asyncio.Queue.
    """
    print(
        f"Wysyłam sygnał o utworzeniu użytkownika (z kolejki): {user_id}, {username}, {email}"
    )
    message = json.dumps({"user_id": user_id, "username": username, "email": email})
    # Dodajemy wiadomość do kolejki
    await user_created_queue.put(message)


async def send_user_login_signal():
    """
    Symuluje wysłanie sygnału o utworzeniu użytkownika.
    Teraz używamy tylko asyncio.Queue.
    """
    print("Wysyłam sygnał o utworzeniu użytkownika (z kolejki):")

    message = json.dumps({"message": "User logged!"})
    # Dodajemy wiadomość do kolejki
    await user_created_queue.put(message)
