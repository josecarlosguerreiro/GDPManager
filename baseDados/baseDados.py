import mysql.connector
from mysql.connector import errorcode


def connect():
    try:
        mydb = mysql.connector.connect(user='jguerreiro', password='2111986kramermania',
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
'''


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
        sql = "select * from users where username = '%s' and pass = '%s' and ativo = 'S'" % (username, password)
        # print(sql)
        mycursor.execute(sql)
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


def getPlantel(epoca):
    try:
        conn = connect()
        mycursor = conn.cursor()
        sql = "select jog.id, jog.nome, jog.alcunha, jog.posicao from jogador jog, plantel p where jog.id = p.id_jogador and " \
              "p.epoca = '%s' and ativo ='S' order by pos_num asc, nome asc;" % epoca
        mycursor.execute(sql)
        result = mycursor.fetchall()
        disconnect(conn)
        return result
    except:
        return None


def criarPlantel(id_jog, epoca):
    try:
        conn = connect()
        mycursor = conn.cursor()
        sql = "insert into plantel (id_jogador, epoca) values (%s,%s)" % (id_jog, epoca)
        print(sql)
        mycursor.execute(sql, id_jog)
        conn.commit()
        print(mycursor.rowcount, "record inserted.")
        disconnect(conn)
    except:
        return None


def adicionaJogador(nome_completo, nome, dta_nasc, posicao, num_pos, telemovel, num_camisola, last_updated_date,
                    username):
    argsList = [nome_completo, nome, dta_nasc, posicao, num_pos, telemovel, num_camisola, last_updated_date, username]
    try:
        conn = connect()
        mycursor = conn.cursor()

        result_args = mycursor.callproc('adiciona_jogador', argsList)
        conn.commit()

        if len(result_args) > 0:
            res = 1
        else:
            res = 0
        disconnect(conn)

        return res

    except:
        print("Database error setTreino: %s" % result_args)


def procuraJogador(alcunha, posicao):
    try:
        conn = connect()
        mycursor = conn.cursor()
        sql = "select id from jogador where alcunha = '%s' and posicao = '%s'" % (alcunha, posicao)
        print(sql)
        mycursor.execute(sql)
        data = mycursor.fetchone()
        disconnect(conn)
        if data is None:
            data = 0
        return data[0]
    except:
        print("FODA-se")
        return None


def procuraJogadorPlantel(id_jog, epoca):
    try:
        conn = connect()
        mycursor = conn.cursor()
        sql = "select id from plantel where id_jogador = '%s' and epoca = '%s' and ativo = 'S' " % (id_jog, epoca)
        print("SQL --> " + sql)
        mycursor.execute(sql)
        data = mycursor.fetchone()
        disconnect(conn)
        return data[0]
    except:
        return None


def adiciona_jogador_plantel(id_jog, epoca, username, data):
    argsList = [id_jog, epoca, data, username]
    try:
        conn = connect()
        mycursor = conn.cursor()

        result_args = mycursor.callproc('adiciona_jogador_plantel', argsList)
        conn.commit()

        if len(result_args) > 0:
            res = 1
        else:
            res = 0
        disconnect(conn)

        return res

    except:
        print("Database error setTreino: %s" % result_args)


def removeJogadorPlantel(id_jog, epoca, username, hoje):
    try:
        conn = connect()
        mycursor = conn.cursor()
        sql = "UPDATE PLANTEL SET ATIVO = 'N', last_updated_date = '%s', last_updated_by = '%s' WHERE ID_JOGADOR = %s " \
              "AND EPOCA = '%s'" % (hoje, username, id_jog, epoca)
        mycursor.execute(sql)
        conn.commit()
        disconnect(conn)
        return 0
    except:
        return -1


def proxJogo():
    try:
        cnx = connect()
        cur = cnx.cursor()
        query_string = "select j.* from jogo j " \
                       "where j.dta_jogo = (select min(j.dta_jogo) from jogo j \
						                    where j.dta_jogo >= (select date_format(sysdate(), '%d-%m-%Y')) \
                                            ) \
				        and (j.id_eq_casa = 1 or j.id_eq_fora = 1 );"
        cur.execute(query_string)
        jogo = cur.fetchone()
        print("--> jogo" + str(jogo))
        return jogo
    except:
        print("ERROR")
        return None

def aposFolga(proxJornada):
    print("APOSFOLGA")
    try:
        cnx = connect()
        cur = cnx.cursor()
        query_string = "select j.* from jogo j where j.jornada = '%s' and (j.id_eq_casa = 1 or " \
                        "j.id_eq_fora = 1 );" % proxJornada
        cur.execute(query_string)
        jogo = cur.fetchone()
        return jogo
    except:
        print("ERROR!!!")
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


def setTreino(campo, data_treino, meteo, tipo_treino, epoca, update_date, update_by):
    argsList = [campo, data_treino, meteo, tipo_treino, epoca, update_date, update_by]
    try:
        conn = connect()
        mycursor = conn.cursor()

        result_args = mycursor.callproc('adiciona_treino', argsList)
        conn.commit()

        if len(result_args) > 0:
            res = 1
            sql = "select id from treino_base where campo = '%s' and data_treino = '%s'" % (campo, data_treino)
            mycursor.execute(sql)
            res = mycursor.fetchone()
        else:
            res = 0

        disconnect(conn)

        return res[0]

    except:
        print("Database error setTreino: %s" % result_args)


def listaTreinos(epoca):
    try:
        conn = connect()
        mycursor = conn.cursor()
        sql = "select * from treino_base where epoca = '%s' and activo = 'S'" % epoca

        mycursor.execute(sql)
        result = mycursor.fetchall()
        disconnect(conn)
        return result
    except:
        return None


def remTreino(id_treino, username, hoje):
    try:
        conn = connect()
        mycursor = conn.cursor()
        sql = "update treino_base set activo = 'N', last_updated_date = '%s', last_updated_by = '%s' where id = %s" % (
        hoje, username, id_treino)
        mycursor.execute(sql)
        conn.commit()
        disconnect(conn)
        return 0
    except:
        return None


def atualizaTreino(id_treino, change_date, username, campo, data, metereologia, tipo_treino):
    try:
        conn = connect()
        mycursor = conn.cursor()
        sql = "UPDATE treino_base SET campo = '%s', data_treino = '%s', tempo = '%s', tipo_treino = '%s', " \
              "last_updated_date = '%s', last_updated_by = '%s' WHERE id = '%s' " \
              % (campo, data, metereologia, tipo_treino, change_date, username, id_treino)
        mycursor.execute(sql)
        conn.commit()
        disconnect(conn)
        return 0
    except:
        return -1


def adicionaJogadorTreino(id_treino, id_jogador, presente, avaliacao, comentario, update_date, update_by):
    argsList = [id_treino, id_jogador, presente, avaliacao, comentario, update_date, update_by]
    try:
        conn = connect()
        mycursor = conn.cursor()

        result_args = mycursor.callproc('adiciona_jogador_treino', argsList)
        conn.commit()

        if len(result_args) > 0:
            res = 1
        else:
            res = 0

        disconnect(conn)

        return res

    except:
        print("Database error adicionaJogadorTreino: %s" % result_args)


def listarJogadoresPresentesTreino(id_treino):
    try:
        conn = connect()
        mycursor = conn.cursor()
        sql = "select jog.nome, jog.alcunha, jog.posicao, t.presente, t.avaliacao, t.comentario, t.last_updated_by, " \
              "t.last_updated_date from jogador jog, treino t where t.id_treino_base = '%s' and t.presente = 'S' and " \
              "jog.id = t.id_jogador  order by jog.pos_num, jog.nome asc;" % id_treino
        mycursor.execute(sql)
        result = mycursor.fetchall()
        disconnect(conn)
        return result
    except:
        return None


def getJogosTodos(epoca):
    try:
        conn = connect()
        mycursor = conn.cursor()
        sql = "select j.jornada, eq_casa.nome, j.golos_eq_casa , eq_fora.nome, j.golos_eq_fora  from jogo j , " \
              "equipas eq_casa, equipas eq_fora, epoca e where j.id_eq_casa = eq_casa.id and j.id_eq_fora = " \
              "eq_fora.id and j.id = e.id_jogo and e.ano = '%s' order by j.jornada asc" % epoca
        mycursor.execute(sql)
        result = mycursor.fetchall()
        disconnect(conn)
        return result
    except:
        return None
