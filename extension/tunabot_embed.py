import datetime
import discord

def embed_text(message, title, description, color, footer):
    now = datetime.datetime.utcnow()
    embed = discord.Embed(title=title, description=description, color=color, timestamp=now)
    embed.set_footer(text=footer, icon_url=message.author.avatar_url)
    return embed