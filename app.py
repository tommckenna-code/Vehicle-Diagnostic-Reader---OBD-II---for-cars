"""
app.py
Flask dashboard for the Vehicle Diagnostic Reader.
Mirrors the NetScan project structure: a background poller feeds
live data, a simple API endpoint serves it, the frontend polls that
endpoint on an interval.
"""
 
from flask import Flask, jsonify, render_template
from obd_serial import ELM327
from pid_decoder import DECODERS
import threading
import time
 
PORT = "/dev/tty.usbserial-ABBC2GWD "   # <-- update after plugging in
 
app = Flask(__name__)
 
latest_data = {
    "rpm": None,
    "speed": None,
    "coolant_temp": None,
    "throttle": None,
    "connected": False,
}
 
PID_MAP = {
    "0C": "rpm",
    "0D": "speed",
    "05": "coolant_temp",
    "11": "throttle",
}
 
 
def poll_loop():
    """Background thread: keeps latest_data updated continuously."""
    global latest_data
    try:
        elm = ELM327(PORT)
        latest_data["connected"] = True
    except Exception as e:
        print(f"OBD connection failed: {e}")
        return
 
    while True:
        for pid, key in PID_MAP.items():
            raw = elm.query_pid("01", pid)
            latest_data[key] = DECODERS[pid](raw)
        time.sleep(1)
 
 
@app.route("/")
def index():
    return render_template("index.html")
 
 
@app.route("/api/data")
def api_data():
    return jsonify(latest_data)
 
 
if __name__ == "__main__":
    thread = threading.Thread(target=poll_loop, daemon=True)
    thread.start()
    app.run(debug=True, port=5000)