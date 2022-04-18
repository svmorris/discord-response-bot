import os
import sys
import discord
import time
import sqlite3
import threading
from tendo import singleton

from api import get_help
from api import set_rule
from api import get_rules
from api import remove_rule
from api import get_response

client = discord.Client()
token = os.getenv('TOKEN')
if token is None:
    print("No token supplied")
    sys.exit(-1)


def backup_rules():
    """ Every 100 minutes, create a backup of the database """
    while True:
        with open('storage/rules.db', 'r', encoding='UTF-8') as infile:
            rulesdb = infile.read()

        with open(f"storage/backup_{time.time()}.db", 'w', encoding='UTF-8') as outfile:
            outfile.write(rulesdb)

        time.sleep(6000) # every 100 minutes


@client.event
async def on_message(message):
    if message.author == client.user:
        return


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


        prefix = '//rules'
        if message.content[:len(prefix)] == prefix:
            res = get_rules(message.content[len(prefix):], message.guild.id)
            if type(res) == list:
                for a in res:
                    await message.channel.send("```json\n" + a + "//The characters: \\, \` and \" have been replaced with '*'\n```")
                    time.sleep(0.5)

                return await message.channel.send("done")
            else:
                return await message.channel.send(
                        "```json\n" + res + "\n//The characters: \\, \` and \" have been replaced with '*'\n//The characters: \\, \` and \" have been replaced with '*'\n```")



    if "dont_respond" not in [y.name.lower() for y in message.author.roles]:
        response = get_response(message)
        if response:
            return await message.channel.send(response)



if __name__ == "__main__":
    #  check if there is another instance running
    # this is so it can be added to cron everyminute, incase it goes down it can recover
    try:
        # will sys.exit(-1) if other instance is running
        me = singleton.SingleInstance()
    except:
        sys.exit(-1)

    from dbhandler import init_bd
    init_bd()

    # Run the periodic backups
    x = threading.Thread(target=backup_rules, args=())
    x.start()

    # Run the actual bot
    client.run(token)
