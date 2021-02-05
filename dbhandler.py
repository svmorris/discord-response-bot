import sqlite3
import base64
import os

# encode/decode shit to stop any sort of injection
def b(a):
    return base64.b64encode(str(a).encode('utf-8')).decode('utf-8')

def d(a):
    return base64.b64decode(str(a).encode('utf-8')).decode('utf-8')

################################ internal ########################
def get_all_rules():
    db_connection = sqlite3.connect(f'./rules.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT * FROM rules ")
    data = db_cursor.fetchall()
    db_connection.close()


################################ !internal ########################
def init_bd():
    if os.path.isfile("./rules.db"):
        print("db already exists")
        return 0
    else:
        db_connection = sqlite3.connect(f'./rules.db')
        db_cursor = db_connection.cursor()
        db_cursor.execute(f"CREATE TABLE rules ('serverId', 'keyword', 'response')")
        db_connection.commit()
        db_connection.close()
        return 1



def save_rule(serverId, keyword, response):
    if not os.path.isfile("./rules.db"):
        init_bd()

    # no injections pls
    serverId = b(serverId)
    keyword = b(keyword)
    response = b(response)

    db_connection = sqlite3.connect(f'./rules.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"INSERT INTO rules VALUES (?, ?, ?)", (serverId, keyword, response))
    db_connection.commit()
    db_connection.close()

    return 0



def get_rules_for_server(serverId):
    serverId = b(serverId)

    db_connection = sqlite3.connect(f'./rules.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT * FROM rules WHERE serverId = ?", (serverId,))
    data = db_cursor.fetchall()
    db_connection.close()

    json_data = []
    for element in data:
        a = {
            'serverId': d(element[0]),
            'keyword': d(element[1]),
            'response': d(element[2])
                }
        json_data.append(a)

    return json_data


def delete_rule(serverId, keyword):
    serverId = b(serverId)
    keyword = b(keyword)

    try:
        db_connection = sqlite3.connect(f'./rules.db')
        db_cursor = db_connection.cursor()
        db_cursor.execute("DELETE FROM rules WHERE serverId = ? AND keyword = ?", (serverId, keyword,))
        db_connection.commit()
        db_connection.close()
        return "deleted keyword: "+d(keyword)
    except:
        return "failed to remove keyword: "+d(keyword)


if __name__ == "__main__":
    init_bd()
