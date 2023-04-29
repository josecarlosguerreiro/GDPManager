import mysql.connector



def connect():
    try:
        mydb = mysql.connector.connect(user='jguerreiro', password='2111986kramermania',
                                       host='localhost',
                                       database='takuki')
        return mydb
    except:
        print("Erro ao aceder base dados.")
        return None

'''
#UPDATE games SET goals_home =

def connect():
    try:
        mydb = mysql.connector.connect(user='jguerreiro', password='2111986kramermania',
                                       host='192.168.1.72',
                                       port='3306',
                                       database='takuki')
        return mydb
    except:
        print("Erro ao aceder base dados.")
        return None
'''
def disconnect(connection):
    try:
        connection.close()
        return 0
    except:
        print("Cannot close db")
        return -1

def getActiveUsers():
    try:
        conn = connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT * FROM users WHERE ATIVO = 'S'")
        result = mycursor.fetchall()
        disconnect(conn)
        return result
    except:
        return None

def getPlayers():
    try:
        conn = connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT * FROM JOGADORES")
        result = mycursor.fetchall()
        disconnect(conn)
        return result
    except:
        return None

