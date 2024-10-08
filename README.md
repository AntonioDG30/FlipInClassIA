
# FlipInClassIA

FlipInClassIA è un progetto sviluppato nell'ambito del tirocinio per il corso di laurea in Informatica presso l'Università di Salerno, sotto la supervisione del Prof. Fabio Palomba. Questo progetto si basa sulla volontà di realizzare un tool di supporto alla metodologia della flipped classroom, concentrandosi specificamente sulla fase in-class. L'obiettivo è migliorare l'interazione tra studenti e docenti attraverso una piattaforma digitale che integra funzionalità avanzate per la gestione delle lezioni, dei quiz, del dibattito e delle statistiche, creando così un ambiente didattico innovativo.

Il progetto si è sviluppato tenendo in considerazione l'analisi dello stato dell'arte nell'integrazione della flipped classroom con l'Intelligenza Artificiale. I seguenti requisiti sono stati implementati per fornire un supporto completo all'esperienza in classe:

- **Supporto programmatico per il docente**: Il tool offre al docente strumenti per programmare e strutturare le lezioni, permettendo di avere un programma ben organizzato ed eseguibile.

- **Monitoraggio del progresso dell’apprendimento**: Il docente ha la possibilità di visualizzare lo stato del progresso dell'apprendimento dell'intera classe tramite un'interfaccia dettagliata, valutando l'acquisizione dei contenuti da parte degli studenti.

- **Feedback personalizzato**: Durante le attività in classe, il tool fornisce agli studenti un feedback immediato e mirato, identificando le lacune di comprensione e suggerendo miglioramenti.

- **Facilità di utilizzo**: L’interfaccia è progettata per essere intuitiva, permettendo agli utenti di accedere rapidamente alle funzionalità principali durante le lezioni.

- **Tracciamento della partecipazione**: Il tool monitora la partecipazione degli studenti durante le lezioni, valutando il livello di coinvolgimento e permettendo al docente di intervenire se necessario.

- **Tutela della privacy**: Per garantire la massima riservatezza, il docente può visualizzare esclusivamente l’andamento della classe nel suo complesso, senza accedere ai dati specifici dei singoli studenti.

## Indice

- [Introduzione](#introduzione)
- [Struttura del Progetto](#struttura-del-progetto)
- [Requisiti](#requisiti)
- [Installazione](#installazione)
- [Configurazione](#configurazione)
- [Utilizzo](#utilizzo)
- [Funzionalità Principali](#funzionalità-principali)
- [Contributi](#contributi)
- [Licenza](#licenza)

## Introduzione

FlipInClassIA è una piattaforma web pensata per agevolare l'interazione tra studenti e docenti nel contesto della flipped classroom. Il progetto si concentra sulla fase in-class, fornendo strumenti avanzati per l'analisi del progresso della classe e il coinvolgimento attivo degli studenti. Grazie a questa piattaforma, il docente può monitorare l'apprendimento, gestire attività interattive come quiz e dibattiti, e offrire feedback immediato, migliorando l'efficacia dell'insegnamento e il coinvolgimento degli studenti.

## Struttura del Progetto

La struttura del progetto è organizzata come segue:

- **static/**: Contiene file statici come immagini, CSS, JavaScript, plugin e altre risorse.
  - **dashboardStaticFile/**: Include i file CSS, immagini e script necessari per la dashboard.
  - **indexStaticFile/**: Contiene le risorse per la pagina di atterraggio (landing page) del progetto.
  - **fileCaricati/**: Cartella destinata ai file caricati nell'applicazione.
- **templates/**: Contiene i template HTML che definiscono la struttura delle varie pagine del sito, inclusi:
  - **dashboard.html**: La pagina della dashboard per la visualizzazione delle statistiche.
  - **lezioneDocente.html** e **lezioneStudente.html**: Template per la gestione delle lezioni da parte del docente e dello studente.
  - **index.html**: La landing page del progetto.
- **Database.sql**: File SQL contenente lo schema del database necessario per il funzionamento dell'applicazione.
- **app.py**: Il file principale dell'applicazione, che gestisce il backend e le interazioni con il database.
- **README.md**: La documentazione del progetto.

## Requisiti

- **Python** (versione >= 3.8)
- **Flask**: Framework web per Python.
- **SQLAlchemy**: ORM per la gestione del database.
- **Bootstrap**: Framework CSS per il design responsivo.
- **Database**: MySQL o un altro database compatibile.
- **JavaScript**: Per le funzionalità interattive.
- **OpenAI API** (opzionale): Per integrare funzionalità avanzate di intelligenza artificiale.

## Installazione

1. **Clona il repository**:

   ```bash
   git clone https://github.com/AntonioDG30/FlipInClassIA
   cd FlipInClassIA
   ```

2. **Installa le dipendenze Python**:

   Crea un ambiente virtuale e attivalo:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   Installa le dipendenze:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configura il database**:

   Crea un database in MySQL e importa il file `Database.sql` per creare le tabelle necessarie.

   ```bash
   mysql -u username -p database_name < Database.sql
   ```

4. **Configura le variabili d'ambiente**:

   Crea un file `.env` nella radice del progetto per specificare le variabili di configurazione come la connessione al database e le chiavi API (se utilizzate).

5. **Esegui l'applicazione**:

   ```bash
   python app.py
   ```

6. **Accedi all'applicazione**:

   L'applicazione sarà disponibile all'indirizzo: `http://localhost:5000`.

## Configurazione

Assicurarsi che il file di configurazione `.env` includa tutte le informazioni necessarie, come ad esempio:

```
FLASK_ENV=development
DATABASE_URL=mysql://username:password@localhost/database_name
SECRET_KEY=<la_tua_secret_key>
OPENAI_API_KEY=<la_tua_chiave_api>
```

## Utilizzo

- Gli utenti possono accedere alla piattaforma attraverso la pagina di login e visualizzare le lezioni disponibili.
- I docenti possono creare e gestire quiz, mentre gli studenti possono partecipare alle lezioni e completare i quiz.
- La dashboard fornisce statistiche aggregate e permette di filtrare i dati in base alle date selezionate.

## Funzionalità Principali

1. **Gestione Lezioni**: I docenti possono creare, modificare e gestire le lezioni direttamente dall'applicazione.

2. **Modalità Quiz**: Gli studenti possono partecipare a quiz in tempo reale, con il timer e il feedback dinamico implementati.

3. **Dashboard Statistiche**: Visualizzazione grafica delle statistiche delle lezioni, con la possibilità di esportare i dati.

4. **Feedback Studente**: Sistema di feedback per gli studenti per valutare le lezioni.

5. **Interfaccia Responsiva**: Design adattabile a diversi dispositivi grazie a Bootstrap.

6. **Integrazione con OpenAI**: Funzionalità avanzate di intelligenza artificiale per migliorare l'interazione didattica (opzionale).

## Contributi

I contributi sono benvenuti. Si prega di seguire le linee guida descritte nel file `CONTRIBUTING.md`.

## Licenza

Questo progetto è distribuito sotto la licenza MIT. Per ulteriori dettagli, consultare il file `LICENSE`.
