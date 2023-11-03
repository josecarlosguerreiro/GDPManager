import hashlib
import sys
import os

import baseDados.baseDados as db
from datetime import datetime
import time


hoje = datetime.today().strftime('%Y-%m-%d')

def listaTreinos(epoca):
    lista = db.listaTreinos(epoca)

    print("%s \t\t%s - \t%s - \t%s" % ("CAMPO".ljust(10), "DATA".ljust(15), "METEREOLOGIA".ljust(15), "TIPO TREINO"))
    print("====================================================================================")
    for treino in lista:
        campo = treino[1]
        data = treino[1]
        metereologia = treino[2]
        tipo_treino = treino[3]
        print("%s - \t%s - \t%s - \t%s" % (campo.ljust(15), data.ljust(15), metereologia.ljust(15), tipo_treino))
    cont = input("Enter para continuar...")
def adicionaTreino(username, epoca):
    os.system('cls')
    print("###########################################")
    print("##                                       ##")
    print("##           GDPenela Manager            ##")
    print("##                                       ##")
    print("##           Adicionar Treino            ##")
    print("##                                       ##")
    print("###########################################\n\n")
    campo = input('Campo do treino:')
    tipo_treino = input('Tipo de treino:')
    data_treino =  input('Data do treino (YYYY-MM-DD):')
    metereologia = input('Metereologia prevista:')


    treino_id = db.setTreino(campo, data_treino, metereologia, tipo_treino, epoca, hoje, username)

    if treino_id == 0:
        print("Erro ao inserir treino.")
        sys.exit(-1)
    else:
        print("Treino inserido com sucesso")
        time.sleep(2)
        opcao = input("Adicionar jogadores (S/N)?").upper()
        while opcao != 'N' or opcao != 'S':
            opcao = input("Valor invalido!\nAdicionar jogadores ao treino? (S/N)").upper()
        if opcao == 'N':
            treinos(username, epoca)
        elif opcao == 'S':
            plantel = getPlantel(epoca)

            for i, jog in enumerate(plantel):
                i += 1
                nome = jog[2]
                print(str(i) + " - " + nome)
                presente = input("Presente (S/N):").upper()
                if presente == 'S':
                    avaliacao = input("Avaliacao (0-9):")
                    while not avaliacao.isnumeric():
                        print("Erro no valor inserido para avaliar jogador %s" % nome)
                        avaliacao = input("Avaliacao (0-9):")
                    while not 0 <= int(avaliacao) <= 9:
                        print("Erro! Avaliacao tem de ser entre 0 e 9")
                        avaliacao = input("Avaliacao (0-9):")
                        while not avaliacao.isnumeric():
                            print("Erro no valor inserido para avaliar jogador %s" % nome)
                            avaliacao = input("Avaliacao (0-9):")
                else:
                    avaliacao = None
                comentario = input("Comentario:")
                db.adicionaJogadorTreino(treino_id, jog[0], presente, avaliacao, comentario, hoje, username)
                print("#######################################")
        else:
            treinos(username, epoca)


def removerTreino(username, epoca):
    lista_treinos = db.listaTreinos(epoca)
    print("#".ljust(7) + "CAMPO".ljust(17), "DATA".ljust(16), "TIPO DE TREINO")
    for i, treino in enumerate(lista_treinos):
        i+=1
        cont = i
        print(str(i).ljust(3) + " - " + treino[1].ljust(16) + " - " + treino[2].ljust(16) + " - " + treino[4])

    print("0 - Voltar atras")

    opcao = int(input('Opção: '))
    if opcao <= cont:
        if opcao == 0:
            treinos(username, epoca)
        else:
            treino = lista_treinos[opcao-1]
            result = db.remTreino(opcao, username, hoje)
            if result == 0:
                print("Treino removido com sucesso")
            else:
                print("Erro na remocao do treino!!!")

    else:
        print("Opção inválida. Pf escolhe uma opção correta")
        return -1

def atualizarTreino(username, epoca):
    lista_treinos = db.listaTreinos(epoca)
    print("#".ljust(7) + "CAMPO".ljust(17), "DATA".ljust(16), "TIPO DE TREINO")
    for i, treino in enumerate(lista_treinos):
        i += 1
        cont = i
        print(str(i).ljust(3) + " - " + treino[1].ljust(16) + " - " + treino[2].ljust(16) + " - " + treino[4])

    print("0 - Voltar atras")

    opcao = int(input('Opção: '))

    if opcao <= cont:
        if opcao == 0:
            treinos(username, epoca)
        else:
            treino = lista_treinos[opcao-1]
            campo = input("Campo:")
            data = input("Data do treino:")
            meteo = input("Metereologia:")
            tipo_treino = input("Tipo de treino:")
            if campo == '':
                campo = treino[1]

            if data == '':
                data = treino[2]

            if meteo == '':
                meteo = treino[3]

            if tipo_treino == '':
                tipo_treino = treino[4]

            result = db.atualizaTreino(opcao, hoje, username, campo, data, meteo, tipo_treino)

            if result == 0:
                print("Treino alterado com sucesso!")
            else:
                print("Erro na correcao do treino!!!")

    else:
        print("Opção inválida. Pf escolhe uma opção correta")
        return -1

def treinoPormenor(username, epoca):
    lista_treinos = db.listaTreinos(epoca)
    print("#".ljust(7) + "CAMPO".ljust(17), "DATA".ljust(16), "TIPO DE TREINO")
    for i, treino in enumerate(lista_treinos):
        i += 1
        cont = i
        print(str(i).ljust(3) + " - " + treino[1].ljust(16) + " - " + treino[2].ljust(16) + " - " + treino[4])

    print("0 - Voltar atras")

    opcao = int(input('Opção: '))
    os.system('cls')
    if opcao <= cont:
        if opcao == 0:
            treinos(username, epoca)
        else:
            treino = lista_treinos[opcao - 1]
            id_treino = treino[0]
            print("###########################################")
            print("Campo: %s" % treino[1])
            print("Data do treino: %s" % treino[2])
            print("Metereologia: %s" % treino[3])
            print("Tipo de treino: %s" % treino[4])
            print("###########################################")
            print("Ultima modificacao: %s" % treino[7])
            print("Modificado por: %s" % treino[8])
            print("###########################################\n")
            print("1 - Ver jogadores presentes")
            print("2 - Atualizar lista de jogadores")
            print("3 - Ver jogador")
            print("0 - Voltar atras")
            op = input('Opcao:')
            num = op.isnumeric()
            if op.isnumeric():
                while not 0 <= int(op) <= 3:
                    print("Erro! Opcao tem de ser entre 0 e 3")
                    op = input("Opcao (0-3):")
                while not op.isnumeric():
                    print("Opcao invalida")
                    op = input("Opcao (0-9):")
            else:
                while not op.isnumeric():
                    print("Opcao invalida")
                    op = input("Opcao")
                    while not 0 <= int(op) <= 3:
                        print("Erro! Opcao tem de ser entre 0 e 3")
                        op = input("Opcao (0-3):")
                        while not op.isnumeric():
                            print("Opcao invalida")
                            op = input("Opcao (0-9):")
            op = int(op)
            if op == 1:
                listarJogadoresPresentesTreino(id_treino)
                treinoPormenor(username, epoca)
            elif op == 2:
                return
            elif op == 3:
                return
            print("teste")

def listarJogadoresPresentesTreino(id_treino):
    listaJog = db.listarJogadoresPresentesTreino(id_treino)

    for i, jog in enumerate(listaJog):
        print(str(i) + " - " + str(jog))

def menuTreino(username, epoca):
    print("###########################################")
    print("##                                       ##")
    print("##           GDPenela Manager            ##")
    print("##                                       ##")
    print("###########################################\n\n")
    print("1 - Listar treino")
    print("2 - Adicionar treino")
    print("3 - Remover treino")
    print("4 - Corrigir treino")
    print("5 - Ver treino")
    print("0 - Voltar atras")

def treinos(username, epoca):
    menuTreino(username, epoca)
    op = int(input('Opcao:'))
    if op == 1:
        listaTreinos(epoca)
        treinos(username, epoca)
    elif op == 2:
        adicionaTreino(username, epoca)
        treinos(username, epoca)
    elif op == 3:
        removerTreino(username, epoca)
        treinos(username, epoca)
    elif op == 4:
        atualizarTreino(username, epoca)
        treinos(username, epoca)
    elif op == 5:
        treinoPormenor(username, epoca)
        #treinos(username, epoca)
    elif op == 0:
        menu(username, epoca)
    else:
        print('Opcao invalida')
        menu(username)


def plantel(username, epoca):
    menuPlantel(username, epoca)
    op = int(input('Opcao:'))
    print("OPCAO " + str(op))
    if op == 1:
        listarPlantel(username, epoca)
        menuPlantel(username, epoca)
    elif op == 2:
        return
    elif op == 3:
        removeJogadorPlantel(username, epoca)
        plantel(username, epoca)
    elif op == 0:
        menuPenela(epoca)
        menu(username, epoca)
    else:
        print('Opcao invalida')
        menu(username)

def adicionaJogador(username, epoca):
    os.system('cls')
    menuPenela(epoca)

    nome_completo = input('Nome Completo:').upper()
    alcunha = input('Nome:').upper()
    dta_nasc = input('Data de nascimento (YYYY-MM-DD):')
    print("1 - GUARDA REDES")
    print("2 - DEFESA")
    print("3 - MEDIO")
    print("4 - AVANCADO")

    op = int(input('Posicao:'))

    telemovel = input('Numero telemovel:')
    num_camisola = input('Numero camisola:')

    if op == 1:
        num_pos = 1
        posicao = "GUARDA REDES"
    elif op == 2:
        num_pos = 2
        posicao = "DEFESA"
    elif op == 3:
        num_pos = 3
        posicao = "MEDIO"
    else:
        num_pos = 4
        posicao = "AVANCADO"

    result = db.adicionaJogador(nome_completo, dta_nasc, alcunha, posicao, num_pos, telemovel, num_camisola, hoje, username)
    id_jog = db.procuraJogador(alcunha, posicao)
    db.adiciona_jogador_plantel(id_jog, epoca, username, hoje)

    if result == 1:
        print("Jogador inserido com sucesso")
        time.sleep(5)
        plantel(username, epoca)
    else:
        print("ALGO CORREU MAL.")
        sys.exit(-1)

def removeJogadorPlantel(username, epoca):
    print("###########################################")
    print("        REMOVER JOGADOR DO PLANTEL         ")
    print("###########################################")
    alcunha = input('Nome:').upper()
    print("1 - GUARDA REDES")
    print("2 - DEFESA")
    print("3 - MEDIO")
    print("4 - AVANCADO")

    op = int(input('Posicao:'))

    if op == 1:
        num_pos = 1
        posicao = "GUARDA REDES"
    elif op == 2:
        num_pos = 2
        posicao = "DEFESA"
    elif op == 3:
        num_pos = 3
        posicao = "MEDIO"
    else:
        num_pos = 4
        posicao = "AVANCADO"

    #valida se o jogador existe na base dados
    id_jog = db.procuraJogador(alcunha, posicao)
    if id_jog == 0:
        print("Erro na procura do jogador\nVoltando ao menu anterior")
        time.sleep(5)
        os.system('cls')
        menu(username, epoca)
    else:
        #valida se o jogador existe no plantel
        jog = db.procuraJogadorPlantel(id_jog, epoca)
        if jog is None:
            print("Jogador %s nao existe no plantel da epoca %s" %(alcunha, epoca))
            time.sleep(5)
            menu(username, epoca)
        else:
            res = db.removeJogadorPlantel(id_jog, epoca, username, hoje)
            if res == 0:
                print("%s removido do plantel com sucesso." % alcunha)
                time.sleep(3)
            else:
                print("Algo de errado aconteceu. Por favor reportar.")
                time.sleep(5)
        menu(username, epoca)


def getPlantel(epoca):
    lista_jog = db.getPlantel(epoca)

    return lista_jog
def listarPlantel(username, epoca):
    os.system('cls')

    lista_jog = db.getPlantel(epoca)

    menuPenela(epoca)
    print("%s \t\t%s - \t%s" % ("POSICAO".ljust(10), "NOME".ljust(15), "NOME COMPLETO"))
    print("========== \t\t========== \t\t====================")
    for jog in lista_jog:
        nome = jog[1]
        alcunha = jog[2]
        posicao = jog[3]
        print("%s - \t%s - \t%s" % (posicao.ljust(15), alcunha.ljust(15), nome))


def menuJogos(username, epoca):
    print("\n\n\n###########################################\n\n")
    print("1 - Listar Jogos - TODOS")
    print("2 - Listar Jogos - Penela")
    print("3 - Adicionar jogo")
    print("4 - Remover jogo")
    print("5 - Atualizar jogo")
    print("0 - Menu principal")
    op = int(input('Opcao:'))
    if op == 1:
        listarJogosTodos(username,epoca)
        menuJogos(username, epoca)
    else:
        print('Opcao invalida')
        menu(username, epoca)

def listarJogosTodos(username, epoca):
    lista_jog = db.getJogosTodos(epoca)
    for i, num in enumerate(lista_jog):
        print(str(num))
        print(i)
        if (i/7) == 0:
            enter = input('Prima ENTER para continuar:')


def menuPlantel(username, epoca):
    print("\n\n\n###########################################\n\n")
    print("1 - Listar Plantel")
    print("2 - Adicionar jogador")
    print("3 - Remover jogador")
    print("0 - Menu principal")
    op = int(input('Opcao:'))
    if op == 1:
        listarPlantel(username,epoca)
        menuPlantel(username, epoca)
    elif op == 2:
        adicionaJogador(username, epoca)
        menuPlantel(username, epoca)
    elif op == 3:
        removeJogadorPlantel(username, epoca)
        menuPlantel(username, epoca)
    elif op == 0:
        menu(username, epoca)
    else:
        print('Opcao invalida')
        menu(username)
def menuAno(username):
    print("###########################################")
    print("##                                       ##")
    print("##           GDPenela Manager            ##")
    print("##                                       ##")
    print("###########################################\n\n")
    print("1 - 2023-2024")
    print("0 - Voltar atras")
    op = int(input('Opcao:'))
    if op == 1:
        epoca = "2023-2024"
        menu(username, epoca)
    elif op == 0:
        main(username)
    else:
        print('Opcao invalida')
        menu(username)

def menu(username, epoca):
    os.system('cls')
    menuPenela(epoca)
    print("1 - Plantel")
    print("2 - Jogos")
    print("3 - Treinos")
    print("0 - Sair")
    op = int(input('Opcao:'))
    if op == 1:
        plantel(username, epoca)
    elif op == 2:
        menuJogos(username, epoca)
    elif op == 3:
        treinos(username, epoca)
    elif op == 0:
        sys.exit(0)
    else:
        print('Opcao invalida')
        menu(username)


def menuPenela(epoca):
    print("###########################################")
    print("##                                       ##")
    print("##           GDPenela Manager            ##")
    print("##              %s                ##" % epoca)
    print("##                                       ##")
    print("###########################################\n\n")

def login():
    print("###########################################")
    print("##                                       ##")
    print("##           GDPenela Manager            ##")
    print("##                                       ##")
    print("###########################################\n\n")

    username = input('Username:')
    password = input('Password:')

    salt = "5gz"

    #print("Username/Password = %s/%s" % (username,password))

    passwordEncr = password+salt
    hashed = hashlib.md5(passwordEncr.encode())
    hashedHex = hashed.hexdigest()


    try:
        result = db.login(username, hashedHex)

        if result is None:
            print("Username/Password invalidos")
            sys.exit(1)
        else:
            print("Username/Password corretos")
            #perfil = result[5]
            time.sleep(2)
            os.system('cls')
            return username
    except:
        print("Username/Password invalidos")
        sys.exit(1)


def main():
    username = "jguerreiro"
    if username is None:
        username = login()

    menuAno(username)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()