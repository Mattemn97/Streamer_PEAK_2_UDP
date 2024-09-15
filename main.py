import tkinter as tk
from gui import CANStreamerGUI
from streamer import start_streaming
import threading


def start_streaming_callback():
    """Callback function to start CAN streaming."""
    params = gui.get_parameters()
    if params is not None:
        udp_address, udp_port, can_channel, can_bitrate, dbc_file = params
        # Start the streaming in a separate thread
        threading.Thread(
            target=start_streaming, 
            args=(udp_address, udp_port, can_channel, can_bitrate, dbc_file),
            daemon=True
        ).start()


if __name__ == "__main__":
    root = tk.Tk()
    gui = CANStreamerGUI(root, start_streaming_callback)
    root.mainloop()
