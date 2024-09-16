import tkinter as tk
from gui import CANStreamerGUI
from streamer import start_streaming
import threading


def start_streaming_callback(selected_interface, address, port, dbc_file):
    """Callback function to start CAN streaming."""
    # Start the streaming in a separate thread
    threading.Thread(
        target=start_streaming,
        args=(address, port, selected_interface, 250000, dbc_file),  # Usa il bitrate corretto per il CAN
        daemon=True
    ).start()


if __name__ == "__main__":
    root = tk.Tk()
    gui = CANStreamerGUI(root, start_streaming_callback)
    root.mainloop()
