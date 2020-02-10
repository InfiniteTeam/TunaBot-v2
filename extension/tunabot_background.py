import json
import asyncio
import discord

async def file_load(app):
    await app.wait_until_ready()
    while not app.is_closed():
        global config
        global userData
        with open('config.json') as config_file:    
            config = json.load(config_file)
        with open('userData.json') as userData_file:    
            userData = json.load(userData_file)
        await asyncio.sleep(0.05)