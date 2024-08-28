from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import uuid
import bcrypt
import os
import secrets

app = Flask(__name__)

# Genera una chiave segreta casuale per l'app di 32 byte
app.secret_key = secrets.token_bytes(32)


# Funzione di connessione al database
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="FlipInClassIA_DB"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Errore di connessione al database: {err}")
        return None


# Rotta per la homepage
@app.route('/')
def index():
    return render_template('index.html')


# Rotta per la pagina di login
@app.route('/login')
def login():
    return render_template('login.html')


# Rotta per la pagina di registrazione
@app.route('/registrati')
def registrati():
    return render_template('registrati.html')


# Rotta per la dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user_type = session['user_type']
        conn = get_db_connection()
        if conn is None:
            flash('Errore di connessione al database.')
            return redirect(url_for('login'))

        cursor = conn.cursor(dictionary=True)

        # Determina i corsi in cui l'utente è coinvolto
        if user_type == 'docente':
            query = ("SELECT C.corso_id, C.nome AS corso_nome, C.descrizione AS corso_descrizione "
                     "FROM Corso AS C WHERE C.docente_id = %s")
            cursor.execute(query, (user_id,))
        else:  # Per gli studenti
            query = ("SELECT C.corso_id, C.nome AS corso_nome, C.descrizione AS corso_descrizione "
                     "FROM Corso AS C "
                     "JOIN Partecipa AS P ON C.corso_id = P.corso_id "
                     "WHERE P.studente_id = %s")
            cursor.execute(query, (user_id,))

        corsi = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('dashboard.html', user_id=user_id, user_type=user_type, corsi=corsi)

    else:
        flash('Devi essere loggato per accedere alla dashboard.')
        return redirect(url_for('login'))


@app.route('/crea_corso', methods=['POST'])
def crea_corso():
    if 'user_id' in session and session['user_type'] == 'docente':
        course_name = request.form['courseName']
        course_description = request.form['courseDescription']
        docente_id = session['user_id']

        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO Corso (corso_id, nome, descrizione, docente_id) VALUES (%s, %s, %s, %s)"
        corso_id = str(uuid.uuid4())
        cursor.execute(query, (corso_id, course_name, course_description, docente_id))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Corso creato con successo!')
    else:
        flash('Non sei autorizzato a creare un corso.')

    return redirect(url_for('dashboard'))


@app.route('/partecipa_corso', methods=['POST'])
def partecipa_corso():
    if 'user_id' in session and session['user_type'] == 'studente':
        course_code = request.form['courseCode']
        studente_id = session['user_id']

        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO Partecipa (studente_id, corso_id) VALUES (%s, %s)"
        cursor.execute(query, (studente_id, course_code))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Partecipazione al corso avvenuta con successo!')
    else:
        flash('Non sei autorizzato a partecipare a un corso.')

    return redirect(url_for('dashboard'))


# Rotta per la gestione del form di login
@app.route('/loginForm', methods=['GET', 'POST'])
def loginForm():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Connessione al database
        conn = get_db_connection()
        if conn is None:
            flash('Errore di connessione al database.')
            return redirect(url_for('login'))

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
        if conn is None:
            flash('Errore di connessione al database.')
            return redirect(url_for('registrati'))

        cursor = conn.cursor()

        if user_type == 'docente':
            query = "INSERT INTO Docente (docente_id, nome, cognome, email, password) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (user_id, name, cognome, email, hashed_password.decode('utf-8')))
        else:
            query = "INSERT INTO Studente (studente_id, nome, cognome, email, password) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (user_id, name, cognome, email, hashed_password.decode('utf-8')))

        conn.commit()
        cursor.close()
        conn.close()

        # Imposta i dettagli dell'utente nella sessione
        session['user_id'] = user_id
        session['user_type'] = user_type
        session['user_name'] = name + " " + cognome

        flash('Registrazione avvenuta con successo!')
        return redirect(url_for('dashboard'))

    return redirect(url_for('registrati'))


# Rotta per il logout
@app.route('/logout')
def logout():
    session.clear()  # Cancella la sessione
    flash('Logout avvenuto con successo.')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
