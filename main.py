import sys
import discord
import sqlite3
from tendo import singleton

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
        return await message.channel.send(res)

    else:
        response = get_response(message)
        return await message.channel.send(response)




if __name__ == "__main__":
    #  chekc if there is another instance running
    # this is so it can be added to cron everyminute, incase it goes down it can recover
    try:
        # will sys.exit(-1) if other instance is running
        me = singleton.SingleInstance()
    except:
        sys.exit(-1)

    # run
    client.run(token)
