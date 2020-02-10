import discord
from discord.ext import commands
from extension import tunabot_embed, tunabot_utils

al = tunabot_utils.aliases
args = tunabot_utils.arguments
color = tunabot_utils.color

class Ping(commands.Cog):
    def __init__ (self, app):
        self.app = app
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith(al())
        ping = int(app.latency*1000)
        if  ping <= 100:
            status = "양호"
            pcolor = color['green']
        elif 100 < ping <= 200:
            status = "보통"
            pcolor = color['yellow']
        elif 200 < ping <= 300:
            status = "나쁨"
            pcolor = color['orange']
        elif 300 < ping:
            status = "매우 나쁨"
            pcolor = color['red']
        embed = tunabot_embed.embed_text(ctx.message, f":ping_pong: **{status}**", (f"**봇 지연시간** {str(ping)}ms"), pcolor, ctx.message.author)
        await ctx.send(embed=embed)

def setup(app):
    app.add_cog(Ping(app))