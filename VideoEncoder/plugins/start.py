#  Copyright (C) 2021 The Authors

from . import *


@BotzHub.on(
    events.NewMessage(incoming=True, pattern="^/start$", func=lambda e: e.is_private)
)
async def starter(event):
    user = await BotzHub.get_entity(event.sender_id)
    if not await check_user(event.sender_id):
        await add_user(event.sender_id)
    await event.reply(
        f"Hi {user.first_name}\n🤷‍♂️This is A Telegram Bot To Encode x265 (HEVC)Via Ffmpeg.",
        buttons=[
            Button.url("Developer🤷‍♂️", url="https://t.me/isharaka"),
            Button.url("Bots Channel🤷‍♂️", url="https://t.me/joinchat/FJc0YlRIAv9lODM1"),
        ],
    )
