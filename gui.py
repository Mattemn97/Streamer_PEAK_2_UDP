import tkinter as tk
from tkinter import filedialog, messagebox


class CANStreamerGUI:
    def __init__(self, root, start_streaming_callback):
        self.root = root
        self.root.title("CAN Streamer")
        
        # Label and Entry for UDP address
        tk.Label(root, text="UDP Address:").grid(row=0, column=0, sticky=tk.W)
        self.udp_address_entry = tk.Entry(root)
        self.udp_address_entry.insert(0, "127.0.0.1")
        self.udp_address_entry.grid(row=0, column=1)

        # Label and Entry for UDP port
        tk.Label(root, text="UDP Port:").grid(row=1, column=0, sticky=tk.W)
        self.udp_port_entry = tk.Entry(root)
        self.udp_port_entry.insert(0, "9870")
        self.udp_port_entry.grid(row=1, column=1)

        # Label and Entry for CAN channel
        tk.Label(root, text="CAN Channel:").grid(row=2, column=0, sticky=tk.W)
        self.can_channel_entry = tk.Entry(root)
        self.can_channel_entry.insert(0, "PCAN_USBBUS1")
        self.can_channel_entry.grid(row=2, column=1)

        # Label and Entry for CAN bitrate
        tk.Label(root, text="CAN Bitrate:").grid(row=3, column=0, sticky=tk.W)
        self.can_bitrate_entry = tk.Entry(root)
        self.can_bitrate_entry.insert(0, "500000")
        self.can_bitrate_entry.grid(row=3, column=1)

        # Button to select DBC file
        self.dbc_file = tk.StringVar()
        tk.Label(root, text="DBC File:").grid(row=4, column=0, sticky=tk.W)
        self.dbc_file_label = tk.Label(root, text="No file selected")
        self.dbc_file_label.grid(row=4, column=1)
        tk.Button(root, text="Browse", command=self.select_dbc_file).grid(row=4, column=2)

        # Button to start streaming
        tk.Button(root, text="Start Streaming", command=start_streaming_callback).grid(row=5, columnspan=3)

    def select_dbc_file(self):
        """Open a file dialog to select a DBC file."""
        file_path = filedialog.askopenfilename(
            title="Select DBC File",
            filetypes=(("DBC Files", "*.dbc"), ("All Files", "*.*"))
        )
        if file_path:
            self.dbc_file.set(file_path)
            self.dbc_file_label.config(text=file_path)

    def get_parameters(self):
        """Retrieve the parameters from the GUI fields."""
        udp_address = self.udp_address_entry.get()
        udp_port = int(self.udp_port_entry.get())
        can_channel = self.can_channel_entry.get()
        can_bitrate = int(self.can_bitrate_entry.get())
        dbc_file = self.dbc_file.get()

        if not dbc_file:
            messagebox.showerror("Error", "Please select a DBC file.")
            return None

        return udp_address, udp_port, can_channel, can_bitrate, dbc_file
