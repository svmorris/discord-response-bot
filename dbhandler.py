import sqlite3
import base64
import os

# encode/decode shit to stop any sort of injection
def b(a):
    return base64.b64encode(a.encode('utf-8')).decode('utf-8')

def d(a):
    return base64.b64decode(a.encode('utf-8')).decode('utf-8')

################################ internal ########################
def get_all_rules():
    db_connection = sqlite3.connect(f'./rules.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT * FROM rules ")
    data = db_cursor.fetchall()
    db_connection.close()
    print(data)


################################ !internal ########################
def init_bd():
    if os.path.isfile("./rules.db"):
        return 0
    else:
        db_connection = sqlite3.connect(f'./rules.db')
        db_cursor = db_connection.cursor()
        db_cursor.execute(f"CREATE TABLE rules ('serverName', 'keyword', 'response')")
        db_connection.commit()
        db_connection.close()
        return 1



def save_rule(serverName, keyword, response):
    if not os.path.isfile("./rules.db"):
        init_bd()

    # no injections pls
    serverName = b(serverName)
    keyword = b(keyword)
    response = b(response)

    db_connection = sqlite3.connect(f'./rules.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"INSERT INTO rules VALUES (?, ?, ?)", (serverName, keyword, response))
    db_connection.commit()
    db_connection.close()

    return 0



def get_rules_for_server(serverName):
    serverName = b(serverName)

    db_connection = sqlite3.connect(f'./rules.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT * FROM rules WHERE serverName = ?", (serverName,))
    data = db_cursor.fetchall()
    db_connection.close()

    json_data = []
    for element in data:
        a = {
            'serverName': d(element[0]),
            'keyword': d(element[1]),
            'response': d(element[2])
                }
        json_data.append(a)

    return json_data


def delete_rule(serverName, keyword):
    serverName = b(serverName)
    keyword = b(keyword)

    try:
        db_connection = sqlite3.connect(f'./rules.db')
        db_cursor = db_connection.cursor()
        db_cursor.execute("DELETE FROM rules WHERE serverName = ? AND keyword = ?", (serverName, keyword,))
        db_connection.commit()
        db_connection.close()
        return "deleted keyword: "+d(keyword)
    except:
        return "failed to remove keyword: "+d(keyword)

