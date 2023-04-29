import baseDados.baseDados as db


def readFile():
    try:
        print("Opening " + 'B8EBF940.csv')
        f1 = open('B8EBF940.csv', 'r')
        lines = f1.readlines()
        f1.close()
        return lines
    except:
        print("Cannot read file")
        exit(-1)

def insert(lines):
    for i in lines:
        # ignore the first row
        elem = i.split(";")
        jornada = elem[0]
        eq_casa = elem[1]
        eq_fora = elem[2]
        data = elem[3].replace("\n",'')
        id_eq_casa = getId(eq_casa)[0]
        id_eq_fora = getId(eq_fora)[0]
        print(data + " - " + str(id_eq_casa) + " - " + str(id_eq_fora))
        #print(id_eq_casa)
        #print(id_eq_fora)
        insertJ(jornada, data, id_eq_casa, id_eq_fora)

def insertJ(jornada, dta, eq1, eq2):
    conn = db.connect()
    mycursor = conn.cursor()
    sql = "insert into jogo (jornada, id_eq_casa, id_eq_fora, dta_jogo) values( '" + str(jornada) + "', '" + str(eq1) + "', '" + str(eq2) + "', '" + dta + "')"
    print(sql)
    mycursor.execute(sql)
    conn.commit()
    db.disconnect(conn)


def epoca(lines):
    for i in lines:
        # ignore the first row
        elem = i.split(";")
        jornada = elem[0]
        eq_casa = elem[1]
        eq_fora = elem[2]
        data = elem[3].replace("\n",'')
        id_eq_casa = getId(eq_casa)[0]
        id_eq_fora = getId(eq_fora)[0]
        print(data + " - " + str(id_eq_casa) + " - " + str(id_eq_fora))
        #print(id_eq_casa)
        #print(id_eq_fora)
        id_jogo = getIdJogo(id_eq_casa, id_eq_fora)[0]
        insertEpoca(id_jogo)

def insertEpoca(id_jogo):
    conn = db.connect()
    mycursor = conn.cursor()
    sql = "insert into epoca(id_jogo, ano) values( '" + str(id_jogo) + "', '2022-2023')"
    print(sql)
    mycursor.execute(sql)
    conn.commit()
    db.disconnect(conn)



def getId(equipa):
    conn = db.connect()
    mycursor = conn.cursor()
    mycursor.execute("SELECT id FROM equipas where nome = '" + equipa + "'")
    result = mycursor.fetchone()
    db.disconnect(conn)
    return result

def getIdJogo(eq1, eq2):
    conn = db.connect()
    mycursor = conn.cursor()
    mycursor.execute("SELECT id FROM jogo where id_eq_casa = '" + str(eq1) + "' and id_eq_fora = " + str(eq2))
    result = mycursor.fetchone()
    db.disconnect(conn)
    return result
def main():
    lines = readFile()
    insert(lines)
    epoca(lines)

if __name__ == '__main__':
    main()