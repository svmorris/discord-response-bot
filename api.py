from dbhandler import save_rule
from dbhandler import delete_rule
from dbhandler import get_rules_for_server


def set_rule(message):
    text = message.content

    # remove prefix from message
    text = text[len("//rule "):]

    # split by separating commas
    text = text.split(",")

    if len(text) != 2:
        return "failed to set rule, wrong number of arguments supplied (2 needed)"

    keyword = text[0].strip(" ")
    response = text[1].strip(" ")

    if save_rule(message.guild.name, keyword, response) != 0:
        return "failed to set rule: '{keyword}', '{response}'"


    print(f"rule: '{keyword}', '{response}' has been set!")
    return f"rule: '{keyword}', '{response}' has been set!"




def get_response(message):
    serverName = message.guild.name

    rules = get_rules_for_server(serverName)

    print(rules)
    for rule in rules:
        print(rule)
        if rule['keyword'] in message.content:
            return rule['response']

    return False



def remove_rule(message):
    text = message.content
    serverName = message.guild.name

    # remove prefix from message
    text = text[len("//remove "):]
    text = text.strip(" ")

    # get all rules on this server
    rules = get_rules_for_server(serverName)

    print(rules)
    for rule in rules:
        print(rule)
        if rule['keyword'] in text:
            response = delete_rule(serverName, rule['keyword'])
            return response

    return "nothing to remove! :)"


def get_rules(message):
    serverName = message.guild.name

    rules = get_rules_for_server(serverName)

    response = ''
    for rule in rules:
        response += "**"+ rule['keyword'] + "**: " + rule['response'] + "\n"

    if len(response) > 1:
        return response
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

