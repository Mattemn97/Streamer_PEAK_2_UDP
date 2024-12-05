import threading
import tkinter as tk
from tkinter import filedialog


class CANStreamerGUI:
    def __init__(self, root, start_streaming_callback):
        self.root = root
        self.root.title("CAN Streamer UDP")
        self.root.geometry("400x300")

        self.start_streaming_callback = start_streaming_callback

        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.dbc_label = tk.Label(main_frame, text="Seleziona file .dbc:")
        self.dbc_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.dbc_button = tk.Button(main_frame, text="Sfoglia", command=self.select_dbc_file)
        self.dbc_button.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.dbc_file_label = tk.Label(main_frame, text="Nessun file selezionato")
        self.dbc_file_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

        self.start_button = tk.Button(main_frame, text="Avvia Streaming", command=self.start_streaming_thread)
        self.start_button.grid(row=2, column=1, padx=5, pady=10, sticky=tk.E)

        self.bl_label = tk.Label(main_frame, text="Percorso file .blf:")
        self.bl_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)

        self.bl_entry = tk.Entry(main_frame)
        self.bl_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)

        self.record_button = tk.Button(main_frame, text="Avvia Registrazione", command=self.toggle_recording)
        self.record_button.grid(row=4, column=1, padx=5, pady=10, sticky=tk.E)

        # Status Indicators
        self.indicator_frame = tk.Frame(main_frame)
        self.indicator_frame.grid(row=5, column=0, columnspan=2, pady=10)

        self.green_indicator = tk.Canvas(self.indicator_frame, width=20, height=20, bg="gray")
        self.green_indicator.grid(row=0, column=0, padx=10)
        tk.Label(self.indicator_frame, text="Messaggio ricevuto").grid(row=0, column=1, sticky=tk.W)

        self.red_indicator = tk.Canvas(self.indicator_frame, width=20, height=20, bg="gray")
        self.red_indicator.grid(row=1, column=0, padx=10)
        tk.Label(self.indicator_frame, text="Errore periferica").grid(row=1, column=1, sticky=tk.W)

        self.yellow_indicator = tk.Canvas(self.indicator_frame, width=20, height=20, bg="gray")
        self.yellow_indicator.grid(row=2, column=0, padx=10)
        tk.Label(self.indicator_frame, text="Registrazione attiva").grid(row=2, column=1, sticky=tk.W)

        for i in range(2):
            main_frame.grid_columnconfigure(i, weight=1)

        self.dbc_file_path = None
        self.bl_file_path = None
        self.recording = False

    def select_dbc_file(self):
        self.dbc_file_path = filedialog.askopenfilename(filetypes=[("DBC Files", "*.dbc")])
        if self.dbc_file_path:
            self.dbc_file_label.config(text=self.dbc_file_path.split("/")[-1])
        else:
            self.dbc_file_label.config(text="Nessun file selezionato")

    def toggle_recording(self):
        self.bl_file_path = self.bl_entry.get()
        if not self.bl_file_path:
            self.update_red_indicator()
            return

        if not self.recording:
            self.start_streaming_callback('127.0.0.1', 9870, self.dbc_file_path, self.bl_file_path, start_recording=True)
            self.record_button.config(text="Ferma Registrazione")
            self.update_yellow_indicator(True)
        else:
            self.start_streaming_callback('127.0.0.1', 9870, self.dbc_file_path, self.bl_file_path, start_recording=False)
            self.record_button.config(text="Avvia Registrazione")
            self.update_yellow_indicator(False)

        self.recording = not self.recording

    def start_streaming(self):
        if not self.dbc_file_path:
            self.update_red_indicator()
            return
        self.start_streaming_callback('127.0.0.1', 9870, self.dbc_file_path)

    def start_streaming_thread(self):
        threading.Thread(target=self.start_streaming).start()

    def update_green_indicator(self):
        self.green_indicator.config(bg="green")
        self.root.after(500, lambda: self.green_indicator.config(bg="gray"))

    def update_red_indicator(self):
        self.red_indicator.config(bg="red")
        self.root.after(500, lambda: self.red_indicator.config(bg="gray"))

    def update_yellow_indicator(self, active):
        if active:
            self.yellow_indicator.config(bg="yellow")
        else:
            self.yellow_indicator.config(bg="gray")
