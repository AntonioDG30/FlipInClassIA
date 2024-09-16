from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import mysql.connector
import uuid
import bcrypt
import os
import secrets
import random
import string
import uuid

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
            query = ("SELECT C.corso_id, C.nome AS corso_nome, C.descrizione AS corso_descrizione, C.image_path AS corso_immagine "
                     "FROM Corso AS C WHERE C.docente_id = %s")
            cursor.execute(query, (user_id,))
        else:  # Per gli studenti
            query = ("SELECT C.corso_id, C.nome AS corso_nome, C.descrizione AS corso_descrizione, C.image_path AS corso_immagine"
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


IMAGES_PATH = "static/dashboardStaticFile/img/corsi"
os.makedirs(IMAGES_PATH, exist_ok=True)

def generate_course_image(course_name, corso_id):
    # Crea un'immagine con un colore di sfondo generico
    img = Image.new('RGB', (200, 200), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    # Usa le prime due lettere del nome del corso, in maiuscolo
    initials = (course_name[:2] if len(course_name) >= 2 else course_name).upper()

    # Carica un font di default; puoi specificare un file TTF se vuoi un font particolare
    draw = ImageDraw.Draw(img)
    try:
        # Se hai un font TTF specifico, specifica il percorso qui
        font = ImageFont.truetype("arial.ttf", 100)
    except IOError:
        # Usa il font di default se quello specificato non è disponibile
        font = ImageFont.load_default()

    # Calcola la posizione per centrare il testo usando textbbox
    bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((img.width - text_width) // 2, (img.height - text_height) // 2)

    # Aggiungi il testo all'immagine
    draw.text(position, initials, fill=(255, 255, 255), font=font)

    # Salva l'immagine con il corso_id come nome del file
    image_filename = f"{corso_id}.png"
    image_path = os.path.join(IMAGES_PATH, image_filename)
    img.save(image_path)

    return image_filename  # Restituisce solo il nome del file per salvare nel database

@app.route('/crea_corso', methods=['POST'])
def crea_corso():
    if 'user_id' in session and session['user_type'] == 'docente':
        course_name = request.form['courseName']
        course_description = request.form['courseDescription']
        docente_id = session['user_id']

        # Genera un corso_id esadecimale univoco di 6 caratteri
        corso_id = ''.join(random.choices('0123456789abcdef', k=6))

        # Genera l'immagine per il corso
        image_filename = generate_course_image(course_name, corso_id)

        conn = get_db_connection()
        cursor = conn.cursor()
        # Aggiungi il campo per il percorso dell'immagine nel database
        query = "INSERT INTO Corso (corso_id, nome, descrizione, docente_id, image_path) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (corso_id, course_name, course_description, docente_id, image_filename))
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


@app.route('/indexCorso')
def indexCorso():
    # Recupera il corso_id passato come parametro dalla query
    corso_id = request.args.get('corso_id')

    return render_template('indexCorso.html', corso_id=corso_id)


@app.route('/api/lezioni', methods=['GET'])
def get_lezioni():
    corso_id = request.args.get('corso_id')  # Prende il corso_id dai parametri della query
    if not corso_id:
        return jsonify({"error": "Parametro 'corso_id' mancante"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Errore di connessione al database"}), 500

    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM lezione WHERE corso_id = %s"
    cursor.execute(query, (corso_id,))

    # Data corrente per il confronto
    oggi = datetime.now().date()

    lezioni = cursor.fetchall()
    result = []
    for lezione in lezioni:
        # Controlla e converte 'data' in oggetto datetime.date se necessario
        try:
            data_lezione = lezione['data']
            if isinstance(data_lezione, str):
                data_lezione = datetime.strptime(data_lezione, '%Y-%m-%d').date()  # Assicurati di ottenere solo la data
            elif isinstance(data_lezione, datetime):
                data_lezione = data_lezione.date()
            else:
                # Se data_lezione è già un oggetto di tipo date, non fare nulla
                pass

            # Determina il colore in base alla data dell'evento
            if data_lezione < oggi:
                colore = 'green'
                calendar = 'Lezione passata'
            elif data_lezione == oggi:
                colore = 'orange'
                calendar = 'Lezione odierna'
            else:
                colore = 'blue'
                calendar = 'Lezione programmata'

            result.append({
                'descrizione': f"{lezione['descrizione']}",
                'calendar': calendar,
                'color': colore,
                'date': data_lezione.strftime('%Y-%m-%d')
            })

        except Exception as e:
            print(f"Errore nella gestione della data: {e}")
            # Aggiungi una gestione degli errori se necessario

    cursor.close()
    conn.close()

    return jsonify(result)


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
