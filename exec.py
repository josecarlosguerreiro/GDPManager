import hashlib
import baseDados.baseDados as db
def menu():

    print("###########################################")
    print("##                                       ##")
    print("##           GDPenela Manager            ##")
    print("##                                       ##")
    print("###########################################\n\n")
    print("1 - Ver estatisticas por pais")
    print("2 - Atualizar takuki")
    print("9 - Atualizar takuki de forma global")
    print("0 - Sair")

    op = int(input('Opção:'))
    if op == 1:
        return
    elif op == 2:
        return
    elif op == 9:
        return
    elif op == 0:
        return 0
    else:
        print("Opção inválida!")
        return -1


def login():
    print("###########################################")
    print("##                                       ##")
    print("##           GDPenela Manager            ##")
    print("##                                       ##")
    print("###########################################\n\n")
    username = input('Username:')
    password = input('Password:')

    salt = "5gz"

    print("Username/Password = %s/%s" % (username,password))

    passwordEncr = password+salt
    hashed = hashlib.md5(passwordEncr.encode())

    print("HASHED " + hashed)


def main():
    login()
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()