# Streamer_PEAK_2_UDP
Questo programma permette di ascoltare i segnali dalla rete CAN utilizzando una interfaccia Peak, decodificarli utilizzando un file .dbc e inviarli su un server UDP. Il progetto offre un'interfaccia grafica per una gestione semplice dei parametri di configurazione.

## Caratteristiche
- Ascolto della rete CAN: Riceve i messaggi CAN dalla rete utilizzando un'interfaccia Peak
- Decodifica dei messaggi CAN: Utilizza file .dbc per decodificare i messaggi CAN in segnali comprensibili.
- Invio dei dati via UDP: Invia i segnali CAN decodificati in formato JSON a un server UDP specificato.
- Interfaccia grafica: Fornisce un'interfaccia grafica (GUI) per configurare l'indirizzo e la porta UDP, il canale CAN, il bitrate e il file .dbc.
- Esecuzione parallela: Lo streaming dei dati avviene in un thread separato per non bloccare l'interfaccia utente.

## Requisiti
- Python 3.x
- Librerie Python: tkinter, python-can, cantools
- Hardware: Interfaccia CAN Peak (PCAN)

## Installazione
1) Clona la repository:

bash
git clone https://github.com/tuo-username/CAN_Streamer_UDP.git

bash
cd CAN_Streamer_UDP

2) Installa le dipendenze:

bash
pip install -r requirements.txt

## Utilizzo
### Avvio versione Python
1) Esegui il programma:

bash
python main.py

2) Configura i parametri:

    - Inserisci l'indirizzo UDP e la porta di destinazione.
    - Seleziona il canale CAN e il bitrate.
    - Seleziona il file .dbc per la decodifica dei messaggi.

3) Clicca su "Start Streaming" per avviare l'ascolto dei messaggi CAN e l'invio su UDP. Lo streaming avverrà in background.

### Avvio versione eseguibile
Se non vuoi configurare Python, puoi scaricare l'eseguibile dalla sezione Release della repository:

1) Scarica il file main.exe.
2) Esegui il file .exe e utilizza l'interfaccia grafica per avviare lo streaming.

## Contributi
I contributi sono benvenuti! Sentiti libero di aprire issue e pull request.

## Licenza
Questo progetto è distribuito sotto la licenza GPL-3.0. Vedi il file LICENSE per maggiori dettagli.