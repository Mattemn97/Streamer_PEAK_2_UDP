import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import threading
import can

class CANStreamerGUI:
    def __init__(self, root, start_streaming_callback):
        self.root = root
        self.root.title("CAN Streamer UDP")
        self.root.geometry("600x400")  # Modifica delle dimensioni della finestra

        # Callback per avviare lo streaming
        self.start_streaming_callback = start_streaming_callback

        # Frame principale
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Selezione dell'interfaccia Peak
        self.interface_label = tk.Label(main_frame, text="Seleziona interfaccia Peak:")
        self.interface_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        # Dropdown per le interfacce disponibili
        self.interface_var = tk.StringVar()
        self.interface_menu = ttk.Combobox(main_frame, textvariable=self.interface_var, state="readonly")
        self.interface_menu.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        # Bottone per aggiornare la lista delle interfacce
        self.refresh_button = tk.Button(main_frame, text="Aggiorna Interfacce", command=self.update_interfaces)
        self.refresh_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

        # Selezione del file .dbc
        self.dbc_label = tk.Label(main_frame, text="Seleziona file DBC:")
        self.dbc_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.dbc_var = tk.StringVar()
        self.dbc_entry = tk.Entry(main_frame, textvariable=self.dbc_var, state='readonly')
        self.dbc_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        self.dbc_button = tk.Button(main_frame, text="Sfoglia", command=self.select_dbc_file)
        self.dbc_button.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

        # Selezione del bitrate
        self.bitrate_label = tk.Label(main_frame, text="Seleziona Bitrate CAN:")
        self.bitrate_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

        self.bitrate_var = tk.StringVar()
        self.bitrate_menu = ttk.Combobox(main_frame, textvariable=self.bitrate_var, state="readonly")
        self.bitrate_menu['values'] = ["500000", "250000", "125000", "100000", "50000"]  # Aggiungi i bitrate che desideri
        self.bitrate_menu.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

        # Configurazione per il resto dei campi (indirizzo UDP, porta ecc.)
        self.address_label = tk.Label(main_frame, text="Indirizzo UDP:")
        self.address_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)

        self.address_entry = tk.Entry(main_frame)
        self.address_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)

        self.port_label = tk.Label(main_frame, text="Porta UDP:")
        self.port_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)

        self.port_entry = tk.Entry(main_frame)
        self.port_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.EW)

        # ScrolledText per mostrare messaggi di log e aggiornamenti
        self.log_box = scrolledtext.ScrolledText(main_frame, height=10, wrap=tk.WORD)
        self.log_box.grid(row=5, column=0, columnspan=3, padx=5, pady=10, sticky=tk.EW)

        # Bottone per avviare lo streaming
        self.start_button = tk.Button(main_frame, text="Avvia Streaming", command=self.start_streaming_thread)
        self.start_button.grid(row=6, column=1, padx=5, pady=10, sticky=tk.E)

        # Aggiustamento layout del grid
        for i in range(3):
            main_frame.grid_columnconfigure(i, weight=1)

        # Aggiorna l'elenco delle interfacce all'avvio
        self.update_interfaces()

    def update_interfaces(self):
        """Aggiorna la lista delle interfacce CAN disponibili"""
        try:
            available_interfaces = can.interfaces.PCAN.PcanBus().get_available_channels()
            if available_interfaces:
                self.interface_menu['values'] = available_interfaces
                self.interface_menu.current(0)  # Seleziona la prima interfaccia disponibile
                self.log_message("Interfacce aggiornate correttamente.")
            else:
                self.interface_menu['values'] = ["Nessuna interfaccia trovata"]
                self.log_message("Nessuna interfaccia trovata.")
        except Exception as e:
            self.interface_menu['values'] = [f"Errore: {e}"]
            self.log_message(f"Errore nell'aggiornare le interfacce: {e}")

    def select_dbc_file(self):
        """Permette all'utente di selezionare un file DBC"""
        dbc_file = filedialog.askopenfilename(title="Seleziona il file DBC", filetypes=[("DBC files", "*.dbc")])
        self.dbc_var.set(dbc_file)

    def start_streaming(self):
        """Avvia lo streaming passando i parametri alla callback"""
        selected_interface = self.interface_var.get()
        address = self.address_entry.get()
        port = self.port_entry.get()
        dbc_file = self.dbc_var.get()
        bitrate = self.bitrate_var.get()

        if not selected_interface or not address or not port or not dbc_file or not bitrate:
            self.log_message("Errore: Tutti i campi devono essere compilati.")
            return

        self.log_message(f"Avvio dello streaming su interfaccia {selected_interface}, indirizzo {address}, porta {port}, bitrate {bitrate}, file DBC {dbc_file}")
        try:
            # Chiamata alla callback passata come argomento
            self.start_streaming_callback(selected_interface, address, port, bitrate, dbc_file)
            self.log_message("Streaming avviato correttamente.")
        except Exception as e:
            self.log_message(f"Errore durante lo streaming: {e}")

    def log_message(self, message):
        """Logga i messaggi nel box di log"""
        self.log_box.insert(tk.END, f"{message}\n")
        self.log_box.see(tk.END)  # Scorre automaticamente in basso

    def start_streaming_thread(self):
        """Avvia lo streaming in un thread separato per non bloccare la GUI"""
        threading.Thread(target=self.start_streaming).start()
