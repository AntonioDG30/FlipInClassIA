-- Eliminazione del vecchio Database
DROP DATABASE IF EXISTS FlipInClassIA_DB;

-- Creazione del Database
CREATE DATABASE FlipInClassIA_DB;

-- Selezione del Database
USE FlipInClassIA_DB;

-- Creazione della tabella Docenti
CREATE TABLE Docente
(
    docente_id VARCHAR(100) PRIMARY KEY,
    nome       VARCHAR(100) NOT NULL,
    cognome    VARCHAR(100) NOT NULL,
    email      VARCHAR(100) NOT NULL,
    password   VARCHAR(100) NOT NULL,
    image_path varchar(100)
);

-- Creazione della tabella Corsi
CREATE TABLE Corso
(
    corso_id    VARCHAR(100) PRIMARY KEY,
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
    FOREIGN KEY (lezione_id) REFERENCES Lezione (lezione_id)
);

-- Creazione della tabella Domanda
CREATE TABLE Domanda
(
    domanda_id           INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    questionario_id      INT                            NOT NULL,
    testo_domanda        TEXT                           NOT NULL,
    corretta_opzione_id  INT                            NOT NULL,
    argomento_id         INT                            NOT NULL, -- Riferimento all'argomento trattato dalla domanda
    difficolta_percepita FLOAT,                                   -- Difficoltà percepita della domanda
    FOREIGN KEY (questionario_id) REFERENCES Questionario (questionario_id),
    FOREIGN KEY (argomento_id) REFERENCES Argomento (argomento_id)
);

-- Creazione della tabella Opzioni
CREATE TABLE Opzione
(
    opzione_id                INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    domanda_id                INT                            NOT NULL,
    testo_opzione             TEXT                           NOT NULL,
    risposte_errate_frequenza INT DEFAULT 0                  NOT NULL, -- Frequenza con cui questa opzione è stata scelta come risposta errata
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


-- INSERT INTO GENERICI PER TEST E SPERIMENTAZIONI

INSERT INTO `corso` (`corso_id`, `nome`, `descrizione`, `image_path`)
VALUES ('4d9b2b', 'corso1', 'desc_corso1', '4d9b2b.png'),
       ('5eb1ea', 'corso2', 'desc_corso2', '5eb1ea.png'),
       ('8cd2b9', 'corso3', 'desc_corso3', '8cd2b9.png'),
       ('2f8d41', 'corso4', 'desc_corso4', '2f8d41.png'),
       ('346d54', 'corso5', 'desc_corso5', '346d54.png'),
       ('241129', 'corso6', 'desc_corso6', '241129.png');

INSERT INTO `docente` (`docente_id`, `nome`, `cognome`, `email`, `password`, `image_path`)
VALUES ('dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', 'docente1', 'docente1', 'docente@docente.it',
        '$2b$12$P9nLKLYwGg.NIoYHWXk1YeRiu8qHm1oopFzCZu7HnOO46FKxY9r0K', 'fd72d445-f82a-403d-b27b-88baa5b4759d.png'),
       ('86d820d2-65cc-42d7-9e7f-3568d1c3c4ef', 'docente2', 'docente2', 'docente2@docente.it',
        '$2b$12$dHTp2NgI3.KB3Kto7dyhU.ef.ubL65wlXSAx571VL6Wq6KYo6rKwu', '1004e0e3-a013-4495-9057-cd0dd3605c4a.png');

INSERT INTO `lavora` (`docente_id`, `corso_id`, `proprietario`)
VALUES ('dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '4d9b2b', 1),
       ('dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '5eb1ea', 1),
       ('dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '8cd2b9', 1),
       ('86d820d2-65cc-42d7-9e7f-3568d1c3c4ef', '8cd2b9', 0),
       ('dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '2f8d41', 1),
       ('86d820d2-65cc-42d7-9e7f-3568d1c3c4ef', '346d54', 1),
       ('dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '241129', 0),
       ('86d820d2-65cc-42d7-9e7f-3568d1c3c4ef', '346d54', 0),
       ('86d820d2-65cc-42d7-9e7f-3568d1c3c4ef', '241129', 1);


INSERT INTO `studente` (`studente_id`, `nome`, `cognome`, `email`, `password`, `image_path`)
VALUES ('fd72d445-f82a-403d-b27b-88baa5b4759d', 'Studente', 'Studente', 'studente@studente.it',
        '$2b$12$Y5dnTH..1oWZYAmeTcMp3OY5mRfnBKZrgg1QHN6FeEK397V0acM2O', 'fd72d445-f82a-403d-b27b-88baa5b4759d.png');

INSERT INTO `partecipa` (`studente_id`, `corso_id`)
VALUES ('fd72d445-f82a-403d-b27b-88baa5b4759d', '8cd2b9');

INSERT INTO `attivitàlezione` (`attività_lezione_id`, `stato_lezione`, `modalità_lezione`, `fase_lezione`, `descrizione`)
VALUES (1, 'Programmata', '', '', 'La lezione è stata programmata ma non ancora avviata'),
       (2, 'Avviata', 'Questionari', 'Attesa',
        'La lezione è stata avviata in modalità questionari ed è in fase di attesa dell\'autorizzazione da parte del docente per la somministrazione del primo questionario'),
       (3, 'Avviata', 'Questionari', 'Primo_questionario',
        'La lezione è stata avviata nella modalità questionari e agli studenti è stato somministrato per la prima volta il questionario di cui non vedranno il risultato'),
       (4, 'Avviata', 'Questionari', 'Libera',
        'La lezione è stata avviata nella modalità questionari ed è nella fase libera per il docente, il quale può gestire il cosa fare e il come senza supporto o obblighi del tool'),
       (5, 'Avviata', 'Questionari', 'Ultimo_questionario',
        'La lezione è stata avviata nella modalità questionari e agli studenti è stato somministrato per l\'ultima volta il questionario di cui vedranno il risultato'),
       (6, 'Avviata', 'Dibattito', 'Dibattito_gestito',
        'La lezione è stata avviata nella modalità dibattito dov\'è il tool a gestire l\'andamento della lezione a seguito delle risposte che riceve dalle domande che stesso lui pone nel corso della stessa'),
       (7, 'Terminata', '', '', 'La lezione è terminata');


INSERT INTO `lezione` (`lezione_id`, `corso_id`, `docente_id`, `data`, `descrizione`, `statoLezione`)
VALUES (1, '8cd2b9', 'dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '2024-09-12', 'desc_lez1', '7'),
       (2, '8cd2b9', 'dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '2024-09-15', 'desc_lez2', '7'),
       (3, '8cd2b9', '86d820d2-65cc-42d7-9e7f-3568d1c3c4ef', '2024-09-19', 'desc_lez3', '7'),
       (4, '5eb1ea', 'dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '2024-09-23', 'desc_lez4', '7'),
       (5, '5eb1ea', 'dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '2024-09-26', 'desc_lez5', '7'),
       (6, '241129', 'dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '2024-09-26', 'desc_lez6', '7'),
       (7, '8cd2b9', 'dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '2024-09-27', 'desc_lez7', '7'),
       (8, '8cd2b9', '86d820d2-65cc-42d7-9e7f-3568d1c3c4ef', '2024-09-27', 'desc_lez8', '7'),
       (9, '2f8d41', 'dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '2024-09-28', 'desc_lez9', '7'),
       (10, '4d9b2b', 'dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '2024-09-28', 'desc_lez10', '7'),
       (11, '8cd2b9', 'dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '2024-09-29', 'desc_lez11', '7'),
       (12, '241129', 'dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '2024-09-29', 'desc_lez12', '7'),
       (13, '8cd2b9', 'dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '2024-09-29', 'desc_lez13', '7'),
       (14, '8cd2b9', 'dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '2024-09-30', 'desc_lez14', '7'),
       (15, '8cd2b9', 'dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '2024-09-30', 'desc_lez15', '7'),
       (16, '8cd2b9', 'dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '2024-10-01', 'desc_lez16', '2'),
       (17, '8cd2b9', 'dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '2024-10-02', 'desc_lez17', '1'),
       (18, '8cd2b9', 'dba0cc77-496b-4e5d-a7d0-57dd2a981bb7', '2024-10-03', 'desc_lez18', '1');

INSERT INTO `lezione_argomento` (`lezione_argomento_id`, `lezione_id`, `nome_argomento`, `descrizione_argomento`)
VALUES (1, 1, 'nome_arg1_lez1', 'desc_arg1_lez1'),
       (2, 1, 'nome_arg2_lez1', 'desc_arg2_lez1'),
       (3, 1, 'nome_arg2_lez1', 'desc_arg2_lez1'),
       (4, 2, 'nome_arg1_lez2', 'desc_arg1_lez2'),
       (5, 6, 'nome_arg1_lez6', 'desc_arg1_lez6'),
       (6, 9, 'nome_arg1_lez9', 'desc_arg1_lez9'),
       (7, 11, 'nome_arg1_lez11', 'desc_arg1_lez11'),
       (8, 12, 'nome_arg1_lez12', 'desc_arg1_lez12');