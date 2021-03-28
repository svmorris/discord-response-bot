import sys
import discord
import time
import sqlite3
from tendo import singleton

from api import get_help
from api import set_rule
from api import get_rules
from api import remove_rule
from api import get_response

client = discord.Client()
token = str(sys.argv[1])



@client.event
async def on_message(message):
    if message.author == client.user:
        return


    prefix = '//rules'
    if message.content[:len(prefix)] == prefix:
        res = get_rules(message.content[len(prefix):], message.guild.id)
        if type(res) == list:
            for a in res:
                await message.channel.send("```json\n" + a + "//The characters: \\, \` and \" have been replaced with '*'\n```")
                time.sleep(0.5)

            return await message.channel.send("done")
        else:
            return await message.channel.send("```json\n" + res + "\n//The characters: \\, \` and \" have been replaced with '*'\n//The characters: \\, \` and \" have been replaced with '*'\n```")



    prefix = '//help'
    if message.content[:len(prefix)] == prefix:
        res = get_help()
        return await message.channel.send(res)



    # need role from here on
    if "response_controller" in [y.name.lower() for y in message.author.roles] or "admin" in [y.name.lower() for y in message.author.roles]:
        prefix = '//rule'
        if message.content[:len(prefix)] == prefix:
            res = set_rule(message.content[len(prefix):], message.guild.id)
            return await message.channel.send(res)


        prefix = '//remove'
        if message.content[:len(prefix)] == prefix:
            res = remove_rule(message.content[len(prefix):], message.guild.id)
            return await message.channel.send(res)


    if "dont_respond" not in [y.name.lower() for y in message.author.roles]:
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
