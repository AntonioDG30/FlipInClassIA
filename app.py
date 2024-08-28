from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import uuid
import bcrypt
import os
import secrets

app = Flask(__name__)

# Genera una chiave segreta casuale per l'app
app.secret_key = secrets.token_bytes(32)  # Genera una chiave segreta casuale di 32 byte

# Funzione di connessione al database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",  # sostituisci con il tuo host se necessario
        user="root",
        password="",
        database="FlipInClassIA_DB"
    )

# Rotta per la homepage
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

# Rotta per la pagina di registrazione
@app.route('/registrati')
def registrati():
    return render_template('registrati.html')

# Rotta per la dashboard
# Rotta per la dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user_type = session['user_type']
        conn = get_db_connection()
        cursor = conn.cursor()

        # Determina il numero di corsi in cui l'utente è coinvolto
        if user_type == 'docente':
            query = "SELECT COUNT(*) FROM Corso WHERE docente_id = %s"
            cursor.execute(query, (user_id,))
        else:  # Per gli studenti
            #query = "SELECT COUNT(*) FROM Corso WHERE studente_id = %s"
            #cursor.execute(query, (user_id,))
            cursor.execute("SELECT 100")

        numero_corsi = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        return render_template('dashboard.html', user_id=user_id, user_type=user_type, numero_corsi=numero_corsi)
    else:
        flash('Devi essere loggato per accedere alla dashboard.')
        return redirect(url_for('login'))

# Rotta per la pagina di login
@app.route('/loginForm', methods=['GET', 'POST'])
def loginForm():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Connessione al database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Controlla se l'utente esiste come Docente
        query = "SELECT * FROM Docente WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        # Se non è un docente, controlla se è uno studente
        if user is None:
            query = "SELECT * FROM Studente WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            user_type = 'studente'
        else:
            user_type = 'docente'

        conn.close()

        # Se l'utente è trovato, verifica la password
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # Imposta i dettagli dell'utente nella sessione
            session['user_id'] = user['docente_id'] if user_type == 'docente' else user['studente_id']
            session['user_type'] = user_type
            session['user_name'] = user['nome'] + " " + user['cognome']
            session['session_secret'] = secrets.token_hex(16)  # Genera una chiave segreta specifica per la sessione

            flash('Login avvenuto con successo!')
            return redirect(url_for('dashboard'))
        else:
            flash('Email o password non corretti. Riprova.')

    return render_template('login.html')

# Rotta per la gestione del form di registrazione
@app.route('/registratiForm', methods=['GET', 'POST'])
def registratiForm():
    if request.method == 'POST':
        name = request.form['name']
        cognome = request.form['cognome']
        email = request.form['email']
        password = request.form['password']
        user_type = 'docente' if 'userType' in request.form else 'studente'

        # Genera un ID univoco
        user_id = str(uuid.uuid4())

        # Cifra la password prima di memorizzarla
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Inserisci i dati nella tabella appropriata
        conn = get_db_connection()
        cursor = conn.cursor()

        if user_type == 'docente':
            query = "INSERT INTO Docente (docente_id, nome, cognome, email, password) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (user_id, name, cognome, email, hashed_password))
        else:
            query = "INSERT INTO Studente (studente_id, nome, cognome, email, password) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (user_id, name, cognome, email, hashed_password))

        conn.commit()
        cursor.close()
        conn.close()

        # Imposta i dettagli dell'utente nella sessione
        session['user_id'] = user_id
        session['user_type'] = user_type
        session['session_secret'] = secrets.token_hex(16)  # Genera una chiave segreta specifica per la sessione

        flash('Registrazione avvenuta con successo!')
        return redirect(url_for('dashboard'))

    return redirect(url_for('registrati'))


if __name__ == '__main__':
    # Avvia l'app in modalità debug
    app.run(debug=True)
