import aiohttp

import config

async def create_user(user_id: int, first_name: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{config.API_BASE_URL}/users/",
            json={
                "id": user_id,
                "first_name": first_name
            }
        ) as resp:
            if resp.status == 201:
                return (await resp.json())["id"]
            else:
                raise Exception(f"!API error {resp.status}: {await resp.text()}")

async def create_reminder(user_id: int, text: str, target_time: str) -> int:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{config.API_BASE_URL}/reminders/",
            json={
                "user_id": user_id, 
                "text": text,
                "target_time": target_time
            }
        ) as resp:
            if resp.status == 201:
                return (await resp.json())["id"]
            else:
                raise Exception(f"!API error {resp.status}: {await resp.text()}")

async def update_reminder(reminder_id: int, is_sent: bool) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.patch(
            f"{config.API_BASE_URL}/reminders/{reminder_id}",
            json={"is_sent": is_sent}
        ) as resp:
            return resp.status == 200
