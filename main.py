import tkinter as tk
from gui import CANStreamerGUI
from streamer import start_streaming


def start_streaming_callback(udp_address, udp_port, dbc_file, blf_file=None, start_recording=False):
    app_callbacks = {
        "update_green": app.update_green_indicator,
        "update_red": app.update_red_indicator,
    }
    start_streaming(udp_address, udp_port, dbc_file, blf_file, start_recording, gui_callbacks=app_callbacks)


def main():
    global app
    root = tk.Tk()
    app = CANStreamerGUI(root, start_streaming_callback)
    root.mainloop()


if __name__ == "__main__":
    main()
