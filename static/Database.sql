-- Creazione del Database
CREATE DATABASE FlipInClassIA_DB;

-- Selezione del Database
USE FlipInClassIA_DB;

-- Creazione della tabella Docenti
CREATE TABLE Docente
(
    docente_id VARCHAR(100) PRIMARY KEY,
    nome       VARCHAR(100),
    cognome    VARCHAR(100),
    email      VARCHAR(100),
    password   VARCHAR(100)
);

-- Creazione della tabella Corsi
CREATE TABLE Corso
(
    corso_id    VARCHAR(100) PRIMARY KEY,
    nome        VARCHAR(100),
    descrizione TEXT,
    docente_id  VARCHAR(100),
    image_path  VARCHAR(100),
    FOREIGN KEY (docente_id) REFERENCES Docente (docente_id)
);

-- Creazione della tabella Studenti
CREATE TABLE Studente
(
    studente_id VARCHAR(100) PRIMARY KEY,
    nome        VARCHAR(100),
    cognome     VARCHAR(100),
    email       VARCHAR(100),
    password    VARCHAR(100)
);

-- Creazione della tabella Partecipa
CREATE TABLE Partecipa
(
    studente_id VARCHAR(100),
    corso_id    VARCHAR(100),
    FOREIGN KEY (studente_id) REFERENCES Studente (studente_id),
    FOREIGN KEY (corso_id) REFERENCES Corso (corso_id)
);

-- Creazione della tabella Argomenti
CREATE TABLE Argomento
(
    argomento_id INT AUTO_INCREMENT PRIMARY KEY,
    nome         VARCHAR(100),
    descrizione  TEXT
);

-- Creazione della tabella Lezioni
CREATE TABLE Lezione
(
    lezione_id INT AUTO_INCREMENT PRIMARY KEY,
    corso_id   INT,
    data       DATE,
    FOREIGN KEY (corso_id) REFERENCES Corso (corso_id)
);

-- Creazione della tabella Lezione_Argomenti
CREATE TABLE Lezione_Argomento
(
    lezione_argomento_id INT AUTO_INCREMENT PRIMARY KEY,
    lezione_id           INT,
    argomento_id         INT,
    tempo_trascorso      INT, -- Tempo dedicato a questo argomento nella lezione in minuti
    FOREIGN KEY (lezione_id) REFERENCES Lezione (lezione_id),
    FOREIGN KEY (argomento_id) REFERENCES Argomento (argomento_id)
);

-- Creazione della tabella Questionari
CREATE TABLE Questionario
(
    questionario_id INT AUTO_INCREMENT PRIMARY KEY,
    lezione_id      INT,
    FOREIGN KEY (lezione_id) REFERENCES Lezione (lezione_id)
);

-- Creazione della tabella Domande
CREATE TABLE Domanda
(
    domanda_id           INT AUTO_INCREMENT PRIMARY KEY,
    questionario_id      INT,
    testo_domanda        TEXT,
    corretta_opzione_id  INT,
    argomento_id         INT,   -- Riferimento all'argomento trattato dalla domanda
    difficolta_percepita FLOAT, -- Difficoltà percepita della domanda
    FOREIGN KEY (questionario_id) REFERENCES Questionario (questionario_id),
    FOREIGN KEY (argomento_id) REFERENCES Argomento (argomento_id)
);

-- Creazione della tabella Opzioni
CREATE TABLE Opzione
(
    opzione_id                INT AUTO_INCREMENT PRIMARY KEY,
    domanda_id                INT,
    testo_opzione             TEXT,
    risposte_errate_frequenza INT DEFAULT 0, -- Frequenza con cui questa opzione è stata scelta come risposta errata
    FOREIGN KEY (domanda_id) REFERENCES Domanda (domanda_id)
);

-- Creazione della tabella Risposte degli Studenti
CREATE TABLE Risposta_Studente
(
    risposta_studente_id INT AUTO_INCREMENT PRIMARY KEY,
    studente_id          VARCHAR(100),
    domanda_id           INT,
    opzione_scelta_id    INT,
    tempo_risposta       INT, -- Tempo impiegato dallo studente per rispondere, in secondi
    FOREIGN KEY (studente_id) REFERENCES Studente (studente_id),
    FOREIGN KEY (domanda_id) REFERENCES Domanda (domanda_id),
    FOREIGN KEY (opzione_scelta_id) REFERENCES Opzione (opzione_id)
);

-- Creazione della tabella Statistiche Questionario
CREATE TABLE Statistiche_Questionario
(
    statistiche_questionario_id INT AUTO_INCREMENT PRIMARY KEY,
    questionario_id             INT,
    numero_domande              INT,   -- Numero totale di domande nel questionario
    risposte_corrette           INT,   -- Numero totale di risposte corrette
    risposte_errate             INT,   -- Numero totale di risposte errate
    punteggio_medio             FLOAT, -- Punteggio medio degli studenti per questo questionario
    percentuale_successo        FLOAT, -- Percentuale media di successo
    correttezza_per_argomento   FLOAT, -- Percentuale di risposte corrette per argomento
    indice_difficolta           FLOAT, -- Indice complessivo di difficoltà del questionario
    varianza_punteggio          FLOAT, -- Varianza dei punteggi degli studenti per questo questionario
    FOREIGN KEY (questionario_id) REFERENCES Questionario (questionario_id)
);

-- Creazione della tabella Statistiche Studente
CREATE TABLE Statistiche_Studente
(
    statistiche_studente_id     INT AUTO_INCREMENT PRIMARY KEY,
    studente_id                 VARCHAR(100),
    questionario_id             INT,
    risposte_corrette           INT,   -- Numero di risposte corrette dello studente
    risposte_errate             INT,   -- Numero di risposte errate dello studente
    punteggio                   FLOAT, -- Punteggio ottenuto dallo studente
    feedback                    TEXT,  -- Feedback manuale per lo studente
    percentuale_primo_tentativo FLOAT, -- Percentuale di risposte corrette al primo tentativo
    feedback_suggerito          TEXT,  -- Feedback automatico suggerito per lo studente
    FOREIGN KEY (studente_id) REFERENCES Studente (studente_id),
    FOREIGN KEY (questionario_id) REFERENCES Questionario (questionario_id)
);

-- Creazione della tabella Progressione dello Studente
CREATE TABLE Progressione_Studente
(
    progressione_studente_id INT AUTO_INCREMENT PRIMARY KEY,
    studente_id              VARCHAR(100),
    questionario_id          INT,
    punteggio                FLOAT,                               -- Punteggio ottenuto dallo studente in quel questionario
    data                     TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data e ora della registrazione del punteggio
    FOREIGN KEY (studente_id) REFERENCES Studente (studente_id),
    FOREIGN KEY (questionario_id) REFERENCES Questionario (questionario_id)
);

/*-- Creazione della tabella Engagement degli Studenti
CREATE TABLE Engagement_Studente (
    engagement_studente_id INT AUTO_INCREMENT PRIMARY KEY,
    studente_id VARCHAR(100),
    questionari_completati INT,  -- Numero di questionari completati dallo studente
    percentuale_completamento FLOAT,  -- Percentuale di completamento dei questionari assegnati
    questionari_tentati INT,  -- Numero di questionari che lo studente ha iniziato
    FOREIGN KEY (studente_id) REFERENCES Studente(studente_id)
);*/
