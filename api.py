import re

from dbhandler import save_rule
from dbhandler import delete_rule
from dbhandler import get_rules_for_server


## internal, escape chars
def escape(a):
    a = re.sub("`", "", a)
    a = re.sub("\*", "", a)
    a = re.sub("_", "", a)
    return a

# make sure 2k chars limit is not passed
def limit(a):
    if len(a) > 2000:
        return "could not send message because it longer than 2000 characters :("

    return a



def set_rule(text, guild_id):
    text = text.strip(" ")
    # split by separating commas
    text = text.split(",")

    if len(text) < 2:
        return "failed to set rule, wrong number of arguments supplied (2 needed)"

    keyword = text[0]
    response = ','.join(text[1:])


    if save_rule(guild_id, keyword, response) != 0:
        return "failed to set rule: '{keyword}', '{response}'"


    return limit(f"rule: '{keyword}', '{response}' has been set!")




def get_response(message):
    serverId = message.guild.id

    rules = get_rules_for_server(serverId)

    for rule in rules:
        if rule['keyword'].upper().strip() in message.content.upper():
            return limit(rule['response'])

    return False



def remove_rule(text, serverId):
    text = text.strip(" ")

    # get all rules on this server
    rules = get_rules_for_server(serverId)

    for rule in rules:
        if rule['keyword'] in text:
            response = delete_rule(serverId, rule['keyword'])
            return limit(response)

    return "nothing to remove! :)"


def get_rules(text, serverId):
    text = text.strip(" ")

    rules = get_rules_for_server(serverId)

    response = ''
    for rule in rules:
        key = rule['keyword']
        res = rule['response']

        if len(key) > 50:
            key = key[:50] + "..."
        if len(res) > 20:
            res= res[:20] + "..."

        response += escape(key) + f": ```\n" + escape(res) + "\n``` \n"

    if len(response) > 1:
        return limit(response)
    else:
        return "no rules have been set yet"




def get_help():
    Help = "       **help menu for bot:**\n\n"
    Help += "set new rule:\n"
    Help += "```\n"
    Help += "  //rule <keyword> , <response>\n"
    Help += "```\n"
    Help += "check set rules:\n"
    Help += "```\n"
    Help += "  //rules\n"
    Help += "```\n"
    Help += "remove rule:\n"
    Help += "```\n"
    Help += "  //remove <keyword>\n"
    Help += "```\n"
    Help += "help menu:\n"
    Help += "```\n"
    Help += "  //help\n"
    Help += "```\n"

    return Help

