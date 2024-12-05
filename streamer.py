import json
import socket
import can
import can.interfaces.pcan
import cantools


def load_dbc_file(dbc_file):
    """Load the DBC file."""
    try:
        return cantools.database.load_file(dbc_file)
    except Exception as e:
        raise RuntimeError(f"Error loading DBC file '{dbc_file}': {e}")


def get_numeric_value(db, msg_name, signal_name, signal_value):
    """
    Convert NamedSignalValue or string value to its numeric equivalent using the DBC value table, if available.
    If no mapping is found, return the original value.
    """
    try:
        if isinstance(signal_value, cantools.database.can.signal.NamedSignalValue):
            signal_value = str(signal_value)

        message = db.get_message_by_name(msg_name)
        signal = next(sig for sig in message.signals if sig.name == signal_name)
        if signal.choices and isinstance(signal_value, str):
            for num_value, str_value in signal.choices.items():
                if str_value == signal_value:
                    return num_value
        return signal_value
    except Exception:
        return signal_value


def start_streaming(udp_address, udp_port, dbc_file, blf_file=None, start_recording=False, gui_callbacks=None):
    """Start listening to the CAN network, send messages via UDP, and optionally record to a .blf file."""
    try:
        db = load_dbc_file(dbc_file)
        can_bus = can.ThreadSafeBus(interface='pcan', channel='PCAN_USBBUS1', bitrate=250000)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        blf_writer = None
        if start_recording and blf_file:
            blf_writer = can.BLFWriter(open(blf_file, 'wb'))

        print("Streaming CAN data to UDP...")

        while True:
            msg = can_bus.recv()

            if msg is None:
                continue

            if blf_writer:
                blf_writer.write(msg)

            try:
                decoded_message = db.decode_message(msg.arbitration_id, msg.data)
                if gui_callbacks:
                    gui_callbacks["update_green"]()
            except (cantools.database.errors.DecodeError, KeyError):
                continue

            msg_name = db.get_message_by_frame_id(msg.arbitration_id).name
            data = {"timestamp": msg.timestamp}
            for signal_name, signal_value in decoded_message.items():
                numeric_value = get_numeric_value(db, msg_name, signal_name, signal_value)
                data[signal_name] = numeric_value

            json_data = json.dumps(data)
            sock.sendto(json_data.encode(), (udp_address, udp_port))

    except Exception as e:
        print(f"Error during streaming: {e}")
        if gui_callbacks:
            gui_callbacks["update_red"]()
    finally:
        if blf_writer:
            blf_writer.close()
        can_bus.shutdown()
