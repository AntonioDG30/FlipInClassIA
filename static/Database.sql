-- Eliminazione del vecchio Database
DROP DATABASE IF EXISTS FlipInClassIA_DB;

-- Creazione del Database
CREATE DATABASE FlipInClassIA_DB;

-- Selezione del Database
USE FlipInClassIA_DB;

-- Creazione della tabella Docenti
CREATE TABLE Docente
(
    docente_id VARCHAR(100) PRIMARY KEY NOT NULL,
    nome       VARCHAR(100) NOT NULL,
    cognome    VARCHAR(100) NOT NULL,
    email      VARCHAR(100) NOT NULL,
    password   VARCHAR(100) NOT NULL,
    image_path varchar(100)
);

-- Creazione della tabella Corsi
CREATE TABLE Corso
(
    corso_id    VARCHAR(100) PRIMARY KEY NOT NULL,
    nome        VARCHAR(100),
    descrizione TEXT,
    image_path  VARCHAR(100)
);

-- Creazione della tabella Studenti
CREATE TABLE Studente
(
    studente_id VARCHAR(100) PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL,
    cognome     VARCHAR(100) NOT NULL,
    email       VARCHAR(100) NOT NULL,
    password    VARCHAR(100) NOT NULL,
    image_path  varchar(100)
);

-- Creazione della tabella Lavora
CREATE TABLE Lavora
(
    docente_id   VARCHAR(100) NOT NULL,
    corso_id     VARCHAR(100) NOT NULL,
    proprietario tinyint      NOT NULL,
    FOREIGN KEY (docente_id) REFERENCES Docente (docente_id),
    FOREIGN KEY (corso_id) REFERENCES Corso (corso_id)
);

-- Creazione della tabella Partecipa
CREATE TABLE Partecipa
(
    studente_id VARCHAR(100) NOT NULL,
    corso_id    VARCHAR(100) NOT NULL,
    FOREIGN KEY (studente_id) REFERENCES Studente (studente_id),
    FOREIGN KEY (corso_id) REFERENCES Corso (corso_id)
);

-- Creazione della tabella AttivitàLezione
CREATE TABLE AttivitàLezione
(
    attività_lezione_id int                                                           NOT NULL AUTO_INCREMENT PRIMARY KEY,
    stato_lezione       varchar(100)                                                  NOT NULL,
    modalità_lezione    varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
    fase_lezione        varchar(100)                                                  NOT NULL,
    descrizione         text                                                          NOT NULL
);

-- Creazione della tabella Lezioni
CREATE TABLE Lezione
(
    lezione_id   INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    corso_id     VARCHAR(100)                   NOT NULL,
    docente_id   VARCHAR(100)                   NOT NULL,
    data         DATE                           NOT NULL,
    descrizione  TEXT                           NOT NULL,
    statoLezione INT                            NOT NULL,
    FOREIGN KEY (corso_id) REFERENCES Corso (corso_id),
    FOREIGN KEY (docente_id) REFERENCES Docente (docente_id),
    FOREIGN KEY (statoLezione) REFERENCES AttivitàLezione (attività_lezione_id)
);

-- Creazione della tabella Presente
CREATE TABLE Presente
(
    studente_id VARCHAR(100) NOT NULL,
    lezione_id    INT NOT NULL,
    FOREIGN KEY (studente_id) REFERENCES Studente (studente_id),
    FOREIGN KEY (lezione_id) REFERENCES Lezione (lezione_id)
);

-- Creazione della tabella Lezione_Argomenti
CREATE TABLE Lezione_Argomento
(
    lezione_argomento_id  INT AUTO_INCREMENT PRIMARY KEY,
    lezione_id            INT          NOT NULL,
    nome_argomento        VARCHAR(100) NOT NULL,
    descrizione_argomento TEXT         NOT NULL,
    FOREIGN KEY (lezione_id) REFERENCES Lezione (lezione_id)
);

-- Creazione della tabella Questionari
CREATE TABLE Questionario
(
    questionario_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    lezione_id      INT                            NOT NULL,
    avvio_primaFase TIMESTAMP                      NOT NULL,
    avvio_secondaFase TIMESTAMP                    NOT NULL,
    FOREIGN KEY (lezione_id) REFERENCES Lezione (lezione_id)
);

-- Creazione della tabella Domanda
CREATE TABLE Domanda
(
    domanda_id           INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    questionario_id      INT                            NOT NULL,
    testo_domanda        TEXT                           NOT NULL,
    corretta_opzione_id  INT                                    ,
    FOREIGN KEY (questionario_id) REFERENCES Questionario (questionario_id)
);

-- Creazione della tabella Opzioni
CREATE TABLE Opzione
(
    opzione_id                INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    domanda_id                INT                            NOT NULL,
    testo_opzione             TEXT                           NOT NULL,
    FOREIGN KEY (domanda_id) REFERENCES Domanda (domanda_id)
);

-- Creazione della tabella Risposte degli Studenti
CREATE TABLE Risposta_Studente
(
    risposta_studente_id INT AUTO_INCREMENT PRIMARY KEY,
    studente_id          VARCHAR(100),
    domanda_id           INT,
    opzione_scelta_id    INT,
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
    feedback_suggerito          TEXT,  -- Feedback manuale per lo studente
    FOREIGN KEY (studente_id) REFERENCES Studente (studente_id),
    FOREIGN KEY (questionario_id) REFERENCES Questionario (questionario_id)
);