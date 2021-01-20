from dbhandler import save_rule
from dbhandler import get_rules_for_server


def set_rule(message):
    text = message.content

    # remove prefix from message
    text = text[len("!rule "):]

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
