"""
reader.py
CLI tool: connects to the ELM327, reads stored fault codes once,
then polls key PIDs on a loop and prints live values.
"""

import time
import sys
from obd_serial import ELM327
from pid_decoder import DECODERS, decode_dtcs, decode_status

PORT = "/dev/tty.usbserial-ABBC2GWD"  # <-- put respective port back here

PIDS_TO_POLL = ["0C", "0D", "05", "11"]  # RPM, speed, coolant, throttle
PID_LABELS = {
    "0C": "RPM",
    "0D": "Speed (km/h)",
    "05": "Coolant Temp (C)",
    "11": "Throttle (%)",
}


def main():
    print(f"Connecting to {PORT}...")
    try:
        elm = ELM327(PORT)
    except Exception as e:
        print(f"Connection failed: {e}")
        print("Check: ignition ON, correct port, cable seated properly.")
        sys.exit(1)

    print("Connected.\n")

    status = decode_status(elm.query_pid("01", "01"))
    if status:
        light_on, count = status
        print(f"Check engine light: {'ON' if light_on else 'off'}, stored codes: {count}")
    else:
        print("Couldn't read status (ECU didn't answer PID 01)")
    print("Fault codes:", decode_dtcs(elm.read_dtcs()) or "none")

    print("\nPolling live data (Ctrl+C to stop)...\n")
    try:
        while True:
            for pid in PIDS_TO_POLL:
                value = DECODERS[pid](elm.query_pid("01", pid))
                print(f"{PID_LABELS[pid]}: {value}")
            print("-" * 30)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping.")
    finally:
        elm.close()


if __name__ == "__main__":
    main()