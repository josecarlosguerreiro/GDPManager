import mysql.connector
from mysql.connector import errorcode

'''
def connect():
    try:
        mydb = mysql.connector.connect(user='root', password='2111986kramermania',
                                       host='127.0.0.1',
                                       database='gdpenela_tst')
        return mydb
    except:
        print("Erro ao aceder base dados.")
        return None

'''

def connect():
    try:
        mydb = mysql.connector.connect(user='jguerreiro', password='2111986kramermania',
                                       host='192.168.1.72',
                                       port='3306',
                                       database='gdpenela_tst')
        return mydb
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        return mydb

def disconnect(connection):
    try:
        connection.close()
        return 0
    except:
        print("Cannot close db")
        return -1

def login(username, password):
    try:
        conn = connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT * FROM users where username = %s and password = %s and ativo = 'S'" % {username, password})
        result = mycursor.fetchone()
        disconnect(conn)
        return result
    except:
        return None

def checkUsername(username):
    try:
        conn = connect()
        mycursor = conn.cursor()
        mycursor.execute("SELECT * FROM users where username = %s and ativo = 'S'" % {username})
        result = mycursor.fetchone()
        disconnect(conn)
        return result
    except:
        return None

def registerUser(username, password, email):
    argsList = [username, password, email]
    try:
        conn = connect()
        mycursor = conn.cursor()
        result_args = mycursor.callproc('registarUser', argsList)
        conn.commit()

        if len(result_args) > 0:
            res = 1
        else:
            res = 0
        disconnect(conn)

        return res
    except:
        print("Database error: registerUser")
        print("End of error")
        print("#############################")
    return None




def insertGame(country, league, season, game_date, round, home_team, away_team, realized):
    argsList = [country, league, season, game_date, round, home_team, away_team, realized]

    try:
        conn = connect()
        mycursor = conn.cursor()
        result_args = mycursor.callproc('insertGame', argsList)
        conn.commit()

        if len(result_args) > 0:
            res = 1
        else:
            res = 0
        disconnect(conn)

        return res
    except:
        print("Database error: insertGame")
        for i in argsList:
            print(i)
        print("End of error")
        print("#############################")



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
        mycursor.execute("SELECT * FROM jogador")
        result = mycursor.fetchall()
        disconnect(conn)
        return result
    except:
        return None

def proxJogo():
    try:
        cnx = connect()
        cur = cnx.cursor()
        query_string = "select min(j.dta_jogo), j.* from jogo j\
                        where j.dta_jogo >=sysdate()\
                          and (j.id_eq_casa = 1 or j.id_eq_fora = 1 )"
        cur.execute(query_string)
        data = cur.fetchall()
        dta = data[0]
        return dta
    except:
        print("ERROR")
        return None

def getEquipaInfo(id_eq):
    try:
        conn = connect()
        mycursor = conn.cursor()
        sql = "select * from equipas where id = " + str(id_eq)
        print(sql)

        mycursor.execute(sql)
        result = mycursor.fetchone()
        disconnect(conn)
        return result
    except:
        return None