import python_functions.globalFunctions as f
import re
import os
from flask import Flask, flash, redirect, render_template, request, session

app = Flask(__name__)


@app.route('/')
def home():
    #f.proxJogo()
    data = f.proxJogo()
    if data is None:
        print("Data is None!!!")
        return render_template('index.html', data=data)
    else:
        print("@@@@@@@@@@@@")
        for i in data:
            print(i)
        return render_template('index.html', data=data)

@app.route('/plantel', methods=['GET'])
def plantel():
    return render_template('plantel.html', data=None)

@app.route('/sede', methods=['GET'])
def sede():
    return render_template('sede.html', data=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output em caso de erro
    msg = ''
    # valida se username e password POST existem
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        print('USERNAME --->', username)
        password = request.form['password']
        print('password --->', password)
        account = f.login(username, password)
        # Se a conta existe
        if account:
            # Cria sessao
            session['loggedin'] = True
            flash('Estas connectado')
            session['id'] = account[0]
            session['username'] = account[1]
            return redirect('/base')  # render_template('base.html')
        else:
            msg = 'Username / Password errada'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect('/')


@app.route('/registo', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account = f.checkUsername(username)

        if account:
            msg = 'Conta ja existente!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Endereco de email invalido!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username apenas pode conter letras e numeros!'
        elif not username or not password or not email:
            msg = 'Por favor preencha tudo!'
        else:
            # Account doesn't exist and the form data is valid, now insert new account into accounts table
            f.registerUser(username, password, email)
            msg = 'Utilizador registado com sucesso!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Por favor preencha tudo!'
    # Show registration form with message (if any)
    return render_template('registo.html', msg=msg)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0')