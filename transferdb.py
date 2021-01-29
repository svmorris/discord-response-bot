import os
import base64
import sqlite3

# encode/decode shit to stop any sort of injection
def b(a):
    return base64.b64encode(str(a).encode('utf-8')).decode('utf-8')

def d(a):
    return base64.b64decode(str(a).encode('utf-8')).decode('utf-8')


if os.path.isfile("./rules_withID.db"):
    pass
else:
    db_connection = sqlite3.connect(f'./rules_withID.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"CREATE TABLE rules ('serverId', 'keyword', 'response')")
    db_connection.commit()
    db_connection.close()



db_connection = sqlite3.connect(f'./rules.db')
db_cursor = db_connection.cursor()
db_cursor.execute("SELECT * FROM rules WHERE serverName = ?", (b("TEAM0001"),))
data = db_cursor.fetchall()
db_connection.close()



for rule in data:
    serverName = d(rule[0])
    print('serverName: ',serverName , type(serverName))
    keyword = d(rule[1])
    print('keyword: ',keyword , type(keyword))
    response = d(rule[2])
    print('response: ',response , type(response))

    serverId = "770680298123558942"




    db_connection = sqlite3.connect(f'./rules_withID.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"INSERT INTO rules VALUES (?, ?, ?)", (b(serverId), b(keyword), b(response)))
    db_connection.commit()
    db_connection.close()

