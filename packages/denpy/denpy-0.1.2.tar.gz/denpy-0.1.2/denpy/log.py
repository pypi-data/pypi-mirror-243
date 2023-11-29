import discord

async def send_embed(self, description, title=None, color=None, image_url=None, thumbnail_url=None, footer=None):
    if color is None:
        embed2 = discord.Embed(
            title=title,
            description=description
        )
        if image_url:
            embed2.set_image(url=image_url)
        if thumbnail_url:
            embed2.set_thumbnail(url=thumbnail_url)
        if footer:
            embed2.set_footer(text=footer)
    else:
        embed2 = discord.Embed(
            title=title,
            description=description,
            colour=int('0x' + color.replace('#', ''), 16)
        )
        if image_url:
            embed2.set_image(url=image_url)
        if thumbnail_url:
            embed2.set_thumbnail(url=thumbnail_url)
        if footer:
            embed2.set_footer(text=footer)
    await self.log.send(embed=embed2)

async def send_message(self, content):
    await self.log.send(content=content)
