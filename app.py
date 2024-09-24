from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import mysql.connector
import bcrypt
import os
import secrets
import random


# Inizializza l'app Flask
app = Flask(__name__)

# Genera una chiave segreta casuale per la sessione dell'app (necessaria per le sessioni in Flask)
app.secret_key = secrets.token_bytes(32)


# Funzione che gestisce la connessione al database MySQL
def get_db_connection():
    try:
        # Crea la connessione con il database
        conn = mysql.connector.connect(
            host="localhost",  # Indirizzo del server MySQL
            user="root",  # Nome utente del database MySQL
            password="",  # Password per l'utente del database
            database="FlipInClassIA_DB"  # Nome del database da utilizzare
        )
        return conn
    except mysql.connector.Error as err:
        # Se c'è un errore nella connessione, lo stampa e restituisce None
        print(f"Errore di connessione al database: {err}")
        return None


# Rotta per la homepage dell'app
@app.route('/')
def index():
    # Restituisce la pagina principale ('index.html') come risposta
    return render_template('index.html')


# Rotta per la pagina di login
@app.route('/login')
def login():
    # Restituisce la pagina di login ('login.html')
    return render_template('login.html')


# Rotta per la pagina di registrazione
@app.route('/registrati')
def registrati():
    # Restituisce la pagina di registrazione ('registrati.html')
    return render_template('registrati.html')


# Rotta per la dashboard, visibile solo agli utenti loggati
@app.route('/dashboard')
def dashboard():
    # Verifica se l'utente è loggato controllando se c'è un 'user_id' nella sessione
    if 'user_id' in session:
        user_id = session['user_id']  # Recupera l'ID utente dalla sessione
        user_type = session['user_type']  # Recupera il tipo di utente (docente o studente)

        # Connessione al database
        conn = get_db_connection()
        if conn is None:
            # Se la connessione fallisce, mostra un messaggio di errore e reindirizza al login
            flash('Errore di connessione al database.')
            return redirect(url_for('login'))

        # Cursore per eseguire le query SQL
        cursor = conn.cursor(dictionary=True)

        # Se l'utente è un docente, recupera i corsi associati a quel docente
        if user_type == 'docente':
            query = (
                "SELECT C.corso_id, C.nome AS corso_nome, C.descrizione AS corso_descrizione, C.image_path AS corso_immagine "
                "FROM Corso AS C WHERE C.corso_id IN (SELECT corso_id FROM Lavora WHERE docente_id = %s)")
            cursor.execute(query, (user_id,))  # Esegue la query passando l'ID del docente
        else:
            # Se l'utente è uno studente, recupera i corsi a cui lo studente partecipa
            query = (
                "SELECT C.corso_id, C.nome AS corso_nome, C.descrizione AS corso_descrizione, C.image_path AS corso_immagine "
                "FROM Corso AS C "
                "JOIN Partecipa AS P ON C.corso_id = P.corso_id "
                "WHERE P.studente_id = %s")
            cursor.execute(query, (user_id,))  # Esegue la query con l'ID dello studente

        # Ottiene i risultati della query (corsi)
        corsi = cursor.fetchall()
        cursor.close()  # Chiude il cursore
        conn.close()  # Chiude la connessione al database

        # Restituisce la pagina della dashboard con i corsi dell'utente
        return render_template('dashboard.html', user_id=user_id, user_type=user_type, corsi=corsi)

    else:
        # Se l'utente non è loggato, mostra un messaggio e reindirizza alla pagina di login
        flash('Devi essere loggato per accedere alla dashboard.')
        return redirect(url_for('login'))


# Definisce il percorso in cui verranno salvate le immagini dei corsi
IMAGES_PATH = "static/dashboardStaticFile/img/corsi"
os.makedirs(IMAGES_PATH, exist_ok=True)  # Crea la cartella se non esiste già


# Funzione per generare un'immagine personalizzata per un corso
def generate_course_image(course_name, corso_id):
    # Crea una nuova immagine di 200x200 pixel con un colore di sfondo casuale
    img = Image.new('RGB', (200, 200), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    # Usa le prime due lettere del nome del corso (in maiuscolo) come iniziali
    initials = (course_name[:2] if len(course_name) >= 2 else course_name).upper()

    # Crea un oggetto di disegno e tenta di caricare il font 'arial.ttf'
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except IOError:
        # Se il font non è disponibile, usa un font di default
        font = ImageFont.load_default()

    # Calcola la posizione per centrare il testo nell'immagine usando textbbox
    bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((img.width - text_width) // 2, (img.height - text_height) // 2)

    # Disegna le iniziali al centro dell'immagine
    draw.text(position, initials, fill=(255, 255, 255), font=font)

    # Salva l'immagine con un nome basato sul corso_id
    image_filename = f"{corso_id}.png"
    image_path = os.path.join(IMAGES_PATH, image_filename)
    img.save(image_path)  # Salva l'immagine

    return image_filename  # Restituisce il nome del file immagine da inserire nel database


# Rotta per creare un nuovo corso, accessibile solo ai docenti
@app.route('/crea_corso', methods=['POST'])
def crea_corso():
    # Controlla se l'utente è loggato e se è un docente
    if 'user_id' in session and session['user_type'] == 'docente':
        course_name = request.form['courseName']  # Ottiene il nome del corso dal form HTML
        course_description = request.form['courseDescription']  # Ottiene la descrizione del corso
        docente_id = session['user_id']  # Recupera l'ID del docente dalla sessione

        # Genera un ID univoco per il corso (un codice esadecimale di 6 caratteri)
        corso_id = ''.join(random.choices('0123456789abcdef', k=6))

        # Genera un'immagine personalizzata per il corso
        image_filename = generate_course_image(course_name, corso_id)

        # Connessione al database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Inserisce il nuovo corso nel database con il percorso dell'immagine
        query = "INSERT INTO Corso (corso_id, nome, descrizione, image_path) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (corso_id, course_name, course_description, image_filename))

        # Inserisce un record che associa il docente creatore come proprietario del corso
        query = "INSERT INTO Lavora (docente_id, corso_id, proprietario) VALUES (%s, %s, 1)"
        cursor.execute(query, (docente_id, corso_id))

        # Esegue le modifiche e chiude il cursore e la connessione
        conn.commit()
        cursor.close()
        conn.close()

    else:
        # Se non è un docente loggato, mostra un messaggio di errore
        flash('Non sei autorizzato a creare un corso.')

    # Reindirizza alla dashboard dopo la creazione del corso
    return redirect(url_for('dashboard'))


# Rotta per partecipare a un corso, accessibile solo agli studenti
@app.route('/partecipa_corso', methods=['POST'])
def partecipa_corso():
    # Verifica se l'utente è loggato e se è uno studente
    if 'user_id' in session and session['user_type'] == 'studente':
        course_code = request.form['courseCode']  # Ottiene il codice del corso dal form
        studente_id = session['user_id']  # Recupera l'ID dello studente dalla sessione

        # Connessione al database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Inserisce il record di partecipazione dello studente al corso
        query = "INSERT INTO Partecipa (studente_id, corso_id) VALUES (%s, %s)"
        cursor.execute(query, (studente_id, course_code))

        # Esegue le modifiche e chiude il cursore e la connessione
        conn.commit()
        cursor.close()
        conn.close()

    else:
        # Se non è uno studente loggato, mostra un messaggio di errore
        flash('Non sei autorizzato a partecipare a un corso.')

    # Reindirizza alla dashboard
    return redirect(url_for('dashboard'))


# Funzione per ottenere il docente proprietario di un corso
def ottieniProfessorePresidente(corso_id):
    # Connessione al database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Esegue una query per ottenere il nome, cognome e immagine del docente che è proprietario del corso
    query = ("SELECT D.nome, D.cognome, D.image_path FROM Lavora AS L, Docente AS D "
             "WHERE L.corso_id = %s AND L.proprietario = 1 AND D.docente_id = L.docente_id")
    cursor.execute(query, (corso_id,))
    docente_presidente = cursor.fetchone()  # Ottiene il risultato della query

    return docente_presidente  # Restituisce le informazioni del docente


# Funzione per ottenere il nome di un corso dato il suo ID
def ottieniNomeCorso(corso_id):
    # Connessione al database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Esegue una query per ottenere il nome del corso
    query = ("SELECT C.nome FROM Corso AS C WHERE C.corso_id = %s")
    cursor.execute(query, (corso_id,))
    nome_corso = cursor.fetchone()  # Ottiene il nome del corso

    if nome_corso:
        nome_corso = nome_corso['nome']  # Estrae il nome dal risultato
    else:
        nome_corso = "Corso non trovato"  # Messaggio di errore se il corso non è stato trovato

    return nome_corso  # Restituisce il nome del corso


# Rotta per la pagina dettagliata di un corso specifico
@app.route('/indexCorso')
def indexCorso():
    # Controlla se l'utente è loggato
    if 'user_id' in session:
        user_id = session['user_id']  # Recupera l'ID dell'utente dalla sessione
        user_type = session['user_type']  # Recupera il tipo di utente (studente o docente)

        # Recupera il corso_id dalla query string (parametro URL)
        corso_id = request.args.get('corso_id')

        oggi = datetime.now().date()  # Ottiene la data odierna

        # Connessione al database
        conn = get_db_connection()
        if conn is None:
            return jsonify({
                               "error": "Errore di connessione al database"}), 500  # Messaggio di errore in caso di fallimento della connessione

        cursor = conn.cursor(dictionary=True)

        # Query per ottenere il calendario delle lezioni del corso
        query = ("SELECT D.nome, D.cognome, LE.data, LE.descrizione, LE.lezione_id "
                 "FROM Lezione AS LE "
                 "JOIN Docente AS D ON LE.docente_id = D.docente_id "
                 "JOIN Corso AS C ON C.corso_id = LE.corso_id "
                 "WHERE C.corso_id = %s "
                 "ORDER BY LE.data DESC")
        cursor.execute(query, (corso_id,))
        calendario_lezioni = cursor.fetchall()  # Recupera tutte le lezioni del corso

        # Query per ottenere gli argomenti trattati in ogni lezione del corso
        query = ("SELECT ARG.nome_argomento, ARG.lezione_id "
                  "FROM Lezione_argomento AS ARG, Corso AS C, Lezione AS L "
                  "WHERE C.corso_id = %s "
                  "AND C.corso_id = L.corso_id AND L.lezione_id = ARG.lezione_id ")
        cursor.execute(query, (corso_id,))
        argomenti_lezioni = cursor.fetchall()  # Recupera gli argomenti delle lezioni

        docente_presidente = ottieniProfessorePresidente(corso_id)  # Ottiene il docente proprietario del corso
        nome_corso = ottieniNomeCorso(corso_id)  # Ottiene il nome del corso

        # Chiude i cursori e la connessione
        cursor.close()
        conn.close()

        # Restituisce la pagina del corso ('indexCorso.html') con tutte le informazioni necessarie
        return render_template('indexCorso.html', user_id=user_id, user_type=user_type,
                               nome_corso=nome_corso, corso_id=corso_id, calendario_lezioni=calendario_lezioni,
                               oggi=oggi, argomenti_lezioni=argomenti_lezioni, docente_presidente=docente_presidente)

    else:
        # Se l'utente non è loggato, mostra un messaggio e reindirizza al login
        flash('Devi essere loggato per accedere alla dashboard.')
    return redirect(url_for('login'))


# Rotta per visualizzare la lista degli studenti che partecipano a un corso
@app.route('/studentiPartecipanti')
def studentiPartecipanti():
    # Controlla se l'utente è loggato
    if 'user_id' in session:
        user_id = session['user_id']  # Recupera l'ID utente dalla sessione
        user_type = session['user_type']  # Recupera il tipo di utente (studente o docente)

        # Recupera il corso_id passato come parametro dalla query string
        corso_id = request.args.get('corso_id')

        # Connessione al database
        conn = get_db_connection()
        if conn is None:
            # In caso di errore nella connessione, restituisce un messaggio di errore come JSON
            return jsonify({"error": "Errore di connessione al database"}), 500

        cursor = conn.cursor(dictionary=True)

        # Esegue una query per ottenere le informazioni sugli studenti iscritti al corso
        query = ("SELECT S.nome, S.cognome, S.email, S.image_path "
                 "FROM Studente AS S, Partecipa AS P "
                 "WHERE P.corso_id = %s AND S.studente_id = P.studente_id")
        cursor.execute(query, (corso_id,))
        studenti_corso = cursor.fetchall()  # Recupera la lista di studenti

        docente_presidente = ottieniProfessorePresidente(corso_id)  # Ottiene il docente responsabile del corso
        nome_corso = ottieniNomeCorso(corso_id)  # Ottiene il nome del corso

        # Chiude il cursore e la connessione
        cursor.close()
        conn.close()

        # Restituisce la pagina con l'elenco degli studenti partecipanti ('studenti_partecipanti.html')
        return render_template('studenti_partecipanti.html', user_id=user_id, user_type=user_type,
                               corso_id=corso_id, studenti_corso=studenti_corso,
                               docente_presidente=docente_presidente, nome_corso=nome_corso)

    else:
        # Se l'utente non è loggato, mostra un messaggio di errore e reindirizza alla pagina di login
        flash('Devi essere loggato per accedere alla dashboard.')
    return redirect(url_for('login'))


# Rotta per visualizzare la lista dei professori che partecipano a un corso
@app.route('/professoriPartecipanti')
def professoriPartecipanti():
    # Controlla se l'utente è loggato
    if 'user_id' in session:
        user_id = session['user_id']  # Recupera l'ID utente dalla sessione
        user_type = session['user_type']  # Recupera il tipo di utente (studente o docente)

        # Recupera il corso_id passato come parametro dalla query string
        corso_id = request.args.get('corso_id')

        # Connessione al database
        conn = get_db_connection()
        if conn is None:
            # In caso di errore nella connessione, restituisce un messaggio di errore come JSON
            return jsonify({"error": "Errore di connessione al database"}), 500

        cursor = conn.cursor(dictionary=True)

        # Esegue una query per ottenere le informazioni sui professori associati al corso
        query = ("SELECT D.nome, D.cognome, D.email, D.image_path, L.proprietario "
                 "FROM Docente AS D, Lavora AS L "
                 "WHERE L.corso_id = %s AND D.docente_id = L.docente_id")
        cursor.execute(query, (corso_id,))
        docente_corso = cursor.fetchall()  # Recupera la lista di docenti

        docente_presidente = ottieniProfessorePresidente(corso_id)  # Ottiene il docente responsabile del corso
        nome_corso = ottieniNomeCorso(corso_id)  # Ottiene il nome del corso

        # Chiude il cursore e la connessione
        cursor.close()
        conn.close()

        # Restituisce la pagina con l'elenco dei professori partecipanti ('professori_partecipanti.html')
        return render_template('professori_partecipanti.html', user_id=user_id, user_type=user_type,
                               corso_id=corso_id, docente_corso=docente_corso,
                               docente_presidente=docente_presidente, nome_corso=nome_corso)

    else:
        # Se l'utente non è loggato, mostra un messaggio di errore e reindirizza alla pagina di login
        flash('Devi essere loggato per accedere alla dashboard.')
    return redirect(url_for('login'))

# Rotta per visualizzare e/o partecipare alle lezioni giornaliere del corso
@app.route('/lezioni')
def lezioni():
    # Controlla se l'utente è loggato
    if 'user_id' in session:
        user_id = session['user_id']  # Recupera l'ID utente dalla sessione
        user_type = session['user_type']  # Recupera il tipo di utente (studente o docente)

        # Recupera il corso_id passato come parametro dalla query string
        corso_id = request.args.get('corso_id')

        # Connessione al database
        conn = get_db_connection()
        if conn is None:
            # In caso di errore nella connessione, restituisce un messaggio di errore come JSON
            return jsonify({"error": "Errore di connessione al database"}), 500

        cursor = conn.cursor(dictionary=True)

        # Ottiene la data corrente per il confronto
        oggi = datetime.now().date()

        query = ("SELECT D.nome, D.cognome, LE.descrizione, LE.flagAttività "
                 "FROM Lezione AS LE "
                 "JOIN Docente AS D ON LE.docente_id = D.docente_id "
                 "JOIN Corso AS C ON C.corso_id = LE.corso_id "
                 "WHERE C.corso_id = %s AND LE.data = %s ")
        cursor.execute(query, (corso_id, oggi))
        lezioni = cursor.fetchall()  # Recupera tutte le lezioni del corso

        docente_presidente = ottieniProfessorePresidente(corso_id)  # Ottiene il docente responsabile del corso
        nome_corso = ottieniNomeCorso(corso_id)  # Ottiene il nome del corso

        # Chiude il cursore e la connessione
        cursor.close()
        conn.close()

        # Restituisce la pagina con l'elenco dei professori partecipanti ('professori_partecipanti.html')
        return render_template('lezioni.html', user_id=user_id, user_type=user_type,
                               corso_id=corso_id, lezioni=lezioni,
                               docente_presidente=docente_presidente, nome_corso=nome_corso)

    else:
        # Se l'utente non è loggato, mostra un messaggio di errore e reindirizza alla pagina di login
        flash('Devi essere loggato per accedere alla dashboard.')
    return redirect(url_for('login'))


# Rotta per ottenere le informazioni delle lezioni in formato JSON (API)
@app.route('/api/lezioni', methods=['GET'])
def get_lezioni():
    # Ottiene il corso_id dai parametri della query string
    corso_id = request.args.get('corso_id')
    if not corso_id:
        # Se manca il parametro 'corso_id', restituisce un errore
        return jsonify({"error": "Parametro 'corso_id' mancante"}), 400

    # Connessione al database
    conn = get_db_connection()
    if conn is None:
        # Se c'è un errore nella connessione, restituisce un errore
        return jsonify({"error": "Errore di connessione al database"}), 500

    cursor = conn.cursor(dictionary=True)

    # Query per recuperare tutte le lezioni di un determinato corso
    query = "SELECT * FROM lezione WHERE corso_id = %s"
    cursor.execute(query, (corso_id,))

    # Ottiene la data corrente per il confronto
    oggi = datetime.now().date()

    lezioni = cursor.fetchall()  # Recupera tutte le lezioni del corso
    result = []

    # Itera attraverso le lezioni e determina il colore in base alla data
    for lezione in lezioni:
        try:
            data_lezione = lezione['data']  # Ottiene la data della lezione
            if isinstance(data_lezione, str):
                # Se la data è una stringa, la converte in oggetto `datetime.date`
                data_lezione = datetime.strptime(data_lezione, '%Y-%m-%d').date()
            elif isinstance(data_lezione, datetime):
                data_lezione = data_lezione.date()

            # Determina il colore dell'evento in base alla data
            if data_lezione < oggi:
                colore = 'green'  # Lezioni passate
                calendar = 'Lezione passata'
            elif data_lezione == oggi:
                colore = 'orange'  # Lezioni odierne
                calendar = 'Lezione odierna'
            else:
                colore = 'blue'  # Lezioni future
                calendar = 'Lezione programmata'

            # Aggiunge il risultato in formato JSON-friendly
            result.append({
                'descrizione': f"{lezione['descrizione']}",
                'calendar': calendar,
                'color': colore,
                'date': data_lezione.strftime('%Y-%m-%d')
            })

        except Exception as e:
            # In caso di errore durante il processo di data, stampa l'errore
            print(f"Errore nella gestione della data: {e}")

    # Chiude il cursore e la connessione
    cursor.close()
    conn.close()

    # Restituisce il risultato in formato JSON
    return jsonify(result)


# Rotta per gestire il form di login
@app.route('/loginForm', methods=['GET', 'POST'])
def loginForm():
    if request.method == 'POST':
        email = request.form['email']  # Ottiene l'email dal form
        password = request.form['password']  # Ottiene la password dal form

        # Connessione al database
        conn = get_db_connection()
        if conn is None:
            flash('Errore di connessione al database.')
            return redirect(url_for('login'))

        cursor = conn.cursor(dictionary=True)

        # Controlla se l'utente è un docente
        query = "SELECT * FROM Docente WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        # Se l'utente non è un docente, controlla se è uno studente
        if user is None:
            query = "SELECT * FROM Studente WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            user_type = 'studente'
        else:
            user_type = 'docente'

        conn.close()

        # Se l'utente esiste e la password è corretta
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # Imposta i dettagli dell'utente nella sessione
            session['user_id'] = user['docente_id'] if user_type == 'docente' else user['studente_id']
            session['user_type'] = user_type
            session['user_name'] = user['nome'] + " " + user['cognome']
            session['image'] = user['image_path']

            # Reindirizza alla dashboard
            return redirect(url_for('dashboard'))
        else:
            flash('Email o password non corretti. Riprova.')

    return render_template('login.html')


# Rotta per il logout dell'utente
@app.route('/logout')
def logout():
    # Cancella tutte le informazioni della sessione
    session.clear()
    return redirect(url_for('login'))


# Rotta per la visualizzazione del profilo utente
@app.route('/profilo')
def profilo():
    # Verifica se l'utente è loggato
    if 'user_id' in session:
        user_id = session['user_id']  # Ottiene l'ID dell'utente
        user_type = session['user_type']  # Ottiene il tipo di utente (docente o studente)

        # Connessione al database
        conn = get_db_connection()
        if conn is None:
            flash('Errore di connessione al database.')
            return redirect(url_for('registrati'))

        cursor = conn.cursor(dictionary=True)

        # Query per ottenere i dettagli dell'utente
        if user_type == 'docente':
            query = "SELECT * FROM Docente WHERE docente_id = %s"
        else:
            query = "SELECT * FROM Studente WHERE studente_id = %s"
        cursor.execute(query, (user_id,))
        profilo_utente = cursor.fetchone()

        cursor.close()  # Chiude il cursore
        conn.close()  # Chiude la connessione al database

        # Restituisce la pagina del profilo ('profilo.html')
        return render_template('profilo.html', user_id=user_id, user_type=user_type, profilo_utente=profilo_utente)

    else:
        # Se l'utente non è loggato, mostra un messaggio e reindirizza al login
        flash('Devi essere loggato per accedere alla dashboard.')
        return redirect(url_for('login'))

# Percorso per le immagini profilo degli utenti
USER_IMAGES_PATH = "static/dashboardStaticFile/img/utenti"
os.makedirs(USER_IMAGES_PATH, exist_ok=True)


# Rotta per la modifica del profilo utente
@app.route('/modificaProfilo', methods=['GET', 'POST'])
def modificaProfilo():
    if request.method == 'POST':
        user_type = request.form.get('user_type')  # Ottiene il tipo di utente
        user_id = request.form.get('user_id')  # Ottiene l'ID dell'utente

        # Connessione al database
        conn = get_db_connection()
        if conn is None:
            flash('Errore di connessione al database.')
            return redirect(url_for('registrati'))

        cursor = conn.cursor(dictionary=True)

        # Ottiene le informazioni del profilo utente
        if user_type == 'docente':
            query = "SELECT * FROM Docente WHERE docente_id = %s"
        else:
            query = "SELECT * FROM Studente WHERE studente_id = %s"
        cursor.execute(query, (user_id,))
        profilo_utente = cursor.fetchone()

        # Recupera i nuovi dati o mantiene quelli attuali se non sono stati modificati
        name = request.form.get('name') or profilo_utente['nome']
        cognome = request.form.get('cognome') or profilo_utente['cognome']
        email = request.form.get('email') or profilo_utente['email']

        # Verifica se l'email è già presente nel database
        try:
            query = "SELECT * FROM Docente WHERE email = %s AND docente_id != %s"
            cursor.execute(query, (email, user_id))
            existing_user = cursor.fetchone()

            if not existing_user:
                query = "SELECT * FROM Studente WHERE email = %s AND studente_id != %s"
                cursor.execute(query, (email, user_id))
                existing_user = cursor.fetchone()

            if existing_user:
                flash('L\'email esiste già. Riprova!')
                return redirect(url_for('profilo'))

            # Verifica se è stata caricata una nuova immagine
            image = request.files.get('profilePicture')
            if image and image.filename != '':
                ext = os.path.splitext(image.filename)[1]  # Ottiene l'estensione del file immagine
                image_filename = f"{user_id}{ext}"
                image_path = os.path.join(USER_IMAGES_PATH, image_filename)
                image.save(image_path)  # Salva l'immagine nel percorso specificato
            else:
                # Mantiene l'immagine attuale se non viene caricata una nuova immagine
                image_filename = profilo_utente["image_path"]

            # Aggiorna il profilo utente nel database
            if user_type == 'docente':
                query = "UPDATE Docente SET nome = %s, cognome = %s, email = %s, image_path = %s WHERE docente_id = %s"
                cursor.execute(query, (name, cognome, email, image_filename, user_id))
            else:
                query = "UPDATE Studente SET nome = %s, cognome = %s, email = %s, image_path = %s WHERE studente_id = %s"
                cursor.execute(query, (name, cognome, email, image_filename, user_id))

            conn.commit()  # Salva le modifiche nel database

        except mysql.connector.Error as err:
            flash(f'Errore durante la modifica: {err}')
            return redirect(url_for('registrati'))

        finally:
            cursor.close()  # Chiude il cursore
            conn.close()  # Chiude la connessione al database

        # Aggiorna i dettagli dell'utente nella sessione
        session['user_id'] = user_id
        session['user_type'] = user_type
        session['user_name'] = name + " " + cognome
        session['image'] = image_filename

        # Reindirizza alla pagina del profilo
        return redirect(url_for('profilo'))

    return redirect(url_for('login'))


# Avvio dell'applicazione Flask in modalità di debug
if __name__ == '__main__':
    app.run(debug=True)
