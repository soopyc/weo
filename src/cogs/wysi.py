import asyncio
from io import BytesIO
from typing import List, Optional
from discord.ext import commands
import discord
from discord import app_commands

import numpy as np
import cv2
import pytesseract


def highlight_727(
    attachment_bytes: bytes,
) -> Optional[discord.File]:
    # read image as an numpy array
    image = np.asarray(bytearray(attachment_bytes), dtype="uint8")

    # use imdecode function
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    d = pytesseract.image_to_data(
        image,
        config="--psm 3 --oem 3 -c tessedit_char_whitelist=0123456789",
        output_type=pytesseract.Output.DICT,
    )
    n_boxes = len(d["level"])

    has_727 = False
    for i in range(n_boxes):
        if "727" in d["text"][i]:
            has_727 = True
            (x, y, w, h) = (
                d["left"][i],
                d["top"][i],
                d["width"][i],
                d["height"][i],
            )
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    if has_727:
        return discord.File(
            BytesIO(cv2.imencode(".png", image)[1].tobytes()),
            filename="{i}.png",
        )


class Wysi(commands.Cog):
    """The description for Wysi goes here."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name="where 727",
            callback=self.where_727,
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    @app_commands.guilds(559402502102056961, 680401335862296611)
    async def where_727(
        self, interaction: discord.Interaction, message: discord.Message
    ) -> None:
        if not message.attachments:
            await interaction.response.send_message(
                "The message must have an image attached.\n"
                "This incident will be reported to the hat man 🕷🕷🕷🕷👁🪳👁🪳👁🪳👁👹🪳👁👺👁👺👺👁👺👺👹👹👹🪳👹🪳👁🕷👁🕷👹🪳👹🪳👹👁🕷👁👺👁👺👁🪳👹🪳👹🪳👹👁🕷👺👁🕷🕷🕷🪳🪳🪳🕳🕷👁🕷👁🪳👁🕷👁🕷🕳👺🕳🕷🕳🪳👁🪳👹🕷👹🕷👁🪳👁🪳🕳🪳🕳🕷👁👺👁🕷👹🪳👹🕷🕳👺👁🕷👹🪳👹🪳👹🕷👹🕷👁🕷🕷🕷🕷🕷👁👁👁👁👁👁🪳👹🕷👁🕷👁👺👺👁👺👹👺👹🪳👁🪳🕳🪳👁",
                ephemeral=True,
            )
            return

        await interaction.response.defer(thinking=True)
        highlighted_files = []
        for attachment in message.attachments:
            attachment_bytes = await attachment.read()

            highlighted_file = await asyncio.to_thread(highlight_727, attachment_bytes)

            if highlighted_file:
                highlighted_files.append(highlighted_file)

        if highlighted_files:
            await interaction.followup.send(files=highlighted_files)
        else:
            await interaction.followup.send("no 727 here :moyai:")

    @app_commands.command(name="owo")
    async def owo(self, interaction: discord.Interaction) -> None:
        """owo"""
        await interaction.response.send_message("uwu", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Wysi(bot))
