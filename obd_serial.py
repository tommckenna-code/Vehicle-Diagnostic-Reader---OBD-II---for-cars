"""
obd_serial.py
Low-level serial interface to the ELM327 chip over USB.
Handles the AT command handshake directly rather than hiding it
behind a library — this is the layer that shows you understand
the actual ELM327 protocol.
"""
 
from curses import raw

import serial
import time
 
class ELM327:
    def __init__(self, port, baudrate=38400, timeout=10):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self._initialise()
 
    def _send(self, command):
        self.ser.reset_input_buffer()
        self.ser.write((command + "\r").encode())
        raw = self.ser.read_until(b">").decode(errors="ignore")
        return raw.replace(">", "").replace("SEARCHING...", "").strip()
 
    def _initialise(self):
        """Standard ELM327 startup sequence."""
        self._send("ATZ")    # reset device
        time.sleep(1)
        self._send("ATE0")   # echo off — cleaner responses
        self._send("ATL0")   # linefeeds off
        self._send("ATSP0")  # auto-select OBD protocol (talks to ECU to find it)
 
    def query_pid(self, mode, pid):
        """
        Send a raw Mode/PID request, e.g. mode='01', pid='0C' for RPM.
        Returns the raw hex response string.
        """
        response = self._send(f"{mode}{pid}")
        return response

    def read_dtcs(self):
        """Mode 03 — ask the ECU for stored fault codes."""
        return self._send("03")
 
    def close(self):
        self.ser.close()
 
 
if __name__ == "__main__":
    # Quick manual test — update the port for your Mac
    elm = ELM327("/dev/tty.usbserial-XXXX")
    print("RPM raw response:", elm.query_pid("01", "0C"))
    elm.close()