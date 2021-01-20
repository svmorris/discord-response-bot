import discord
import sqlite3

from api import get_response
from api import set_rule

client = discord.Client()
token = 'ODAxMzc3MDk2NzcyNzQ3MzI3.YAfylA.7fE4zp0h2wsQU5fjUCKf36Db0Ts'




@client.event
async def on_message(message):
    if message.author == client.user:
        return

    prefix = '!rule'
    if message.content[:len(prefix)] == prefix:
        res = set_rule(message)
        await message.channel.send(res)
        return


    else:
        get_response(message)




client.run(token)
