import re
import json

from dbhandler import save_rule
from dbhandler import delete_rule
from dbhandler import get_rules_for_server


## internal, escape chars
def escape(a):
    disallowed = ['\\', '`', '"']
    b = ''
    for i in a:
        if i in disallowed:
            b += '*'
        else:
            b += i
    return b

# make sure 2k chars limit is not passed
def limit(a):
    a = str(a)
    if len(a) > 2000:
        return "could not send message because it longer than 2000 characters :("
    return a



def set_rule(text, guild_id):
    text = text.strip(" ")
    # split by separating commas
    text = text.split(",")

    if len(text) < 2:
        return "failed to set rule, wrong number of arguments supplied (2 needed)"

    keyword = text[0].strip(' ')
    response = ','.join(text[1:])


    if save_rule(guild_id, keyword, response) != 0:
        return "failed to set rule: '{keyword}', '{response}'"


    return limit(f"rule: '{keyword}', '{response}' has been set!")




def get_response(message):
    serverId = message.guild.id

    rules = get_rules_for_server(serverId)

    found = []
    for i, rule in enumerate(rules):
        if rule['keyword'].upper().strip() in message.content.upper():
            found.append({'key': rule.get('keyword'), 'res': rule.get('response')})


    if len(found) > 0:
        longest = {}
        for i in found:
            if i:
                if not longest.get('key'):
                    longest = i
                elif len(str(longest.get('key'))) < len(str(i.get('key'))):
                    print(str(longest.get('key')))
                    longest = i
        return limit(str(longest.get('res')))


    else:
        return None




def remove_rule(text, serverId):
    text = text.strip(" ")

    # get all rules on this server
    rules = get_rules_for_server(serverId)

    for rule in rules:
        if rule['keyword'].strip(' ') in text:
            response = delete_rule(serverId, rule['keyword'])
            return limit(response)

    return "nothing to remove! :)"




def get_rules(text, serverId):
    text = text.strip(" ")

    rules = get_rules_for_server(serverId)

    response_list = []
    for rule in rules:
        # get response, None if something is broken
        key = str(rule.get('keyword'))
        res = str(rule.get('response'))

        # shorten responses
        if len(key) > 50: key = key[:50] + "..."
        if len(res) > 50: res = res[:50] + "..."


        # add response to response_list
        response_list.append({"key": escape(key).strip(' '), "res": escape(res).strip(' ')})


    # format the response
    response = json.dumps(response_list, sort_keys=True, indent=4, separators=(',', ': '), allow_nan = True)


    # if the response is greater than 2000 chars then break it up (leaving 75 for formatting)
    if len(response) > 2000-75:

        # list holds the rules broken up into less than 2000 len blocks
        responses = []
        # response temporarily holds string with responses, until it is larger than 2000 and has to be cut
        response = ''

        # loop through list to format them
        for i in response_list:
            # if larger than 2000 - max len of one object then cut it and append to list
            if len(response) > 2000-215:
                responses.append(response)
                response = ''
            response += json.dumps(i, sort_keys=True, indent=4, separators=(',', ': '), allow_nan = True) + ',\n'

        # append the remainder to the list
        responses.append(response)
        return responses


    # it its less than 2000 then just return it
    else:
        return response




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

