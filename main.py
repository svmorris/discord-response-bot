import sys
import discord
import sqlite3
from tendo import singleton

from api import get_help
from api import set_rule
from api import get_rules
from api import remove_rule
from api import get_response

client = discord.Client()
token = 'ODAxMzc3MDk2NzcyNzQ3MzI3.YAfylA.7fE4zp0h2wsQU5fjUCKf36Db0Ts'



@client.event
async def on_message(message):
    if message.author == client.user:
        return


    prefix = '//rules'
    if message.content[:len(prefix)] == prefix:
        res = get_rules(message.content[len(prefix):], message.guild.id)
        return await message.channel.send(res)


    prefix = '//rule'
    if message.content[:len(prefix)] == prefix:
        res = set_rule(message.content[len(prefix):], message.guild.id)
        return await message.channel.send(res)


    prefix = '//remove'
    if message.content[:len(prefix)] == prefix:
        res = remove_rule(message.content[len(prefix):], message.guild.id)
        return await message.channel.send(res)


    prefix = '//help'
    if message.content[:len(prefix)] == prefix:
        res = get_help()
        return await message.channel.send(res)


    response = get_response(message)
    if response:
        return await message.channel.send(response)


if __name__ == "__main__":
    #  chekc if there is another instance running
    # this is so it can be added to cron everyminute, incase it goes down it can recover
    try:
        # will sys.exit(-1) if other instance is running
        me = singleton.SingleInstance()
    except:
        sys.exit(-1)

    from dbhandler import init_bd
    init_bd()

    # run
    client.run(token)
