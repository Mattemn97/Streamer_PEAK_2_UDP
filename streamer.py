import socket
import can
import cantools


def load_dbc_file(dbc_file):
    """Load the DBC file."""
    try:
        return cantools.database.load_file(dbc_file)
    except Exception as e:
        raise RuntimeError(f"Error loading DBC file '{dbc_file}': {e}")


def setup_can_interface(channel, bitrate):
    """Setup the CAN interface."""
    try:
        return can.interface.Bus(channel=channel, bustype='pcan', bitrate=bitrate)
    except Exception as e:
        raise RuntimeError(f"Error setting up CAN interface on channel '{channel}': {e}")


def start_streaming(udp_address, udp_port, can_channel, can_bitrate, dbc_file):
    """Start listening to the CAN network and send messages via UDP."""
    try:
        db = load_dbc_file(dbc_file)
        can_bus = setup_can_interface(can_channel, can_bitrate)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print("Streaming CAN data to UDP...")

        while True:
            # Receive CAN message
            msg = can_bus.recv()

            if msg is None:
                continue

            # Decode the CAN message using the DBC file
            try:
                decoded_message = db.decode_message(msg.arbitration_id, msg.data)
            except (cantools.database.errors.DecodeError, KeyError):
                continue

            # Prepare the JSON data
            data = {
                "timestamp": msg.timestamp,
                "arbitration_id": msg.arbitration_id,
                "signals": decoded_message
            }

            json_data = json.dumps(data)

            # Send the UDP packet
            sock.sendto(json_data.encode(), (udp_address, udp_port))

    except Exception as e:
        print(f"Error during streaming: {e}")
    finally:
        can_bus.shutdown()
