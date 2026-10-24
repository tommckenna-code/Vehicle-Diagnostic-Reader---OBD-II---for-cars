# Vehicle Diagnostic Reader

Python OBD-II tool using an ELM327 USB adapter. It reads live engine data and stored fault codes from a car's ECU, decoding the raw hex by hand instead of using a library.

## What you need

- An ELM327 !USB! adapter (Bluetooth versions won't work with this code)
- A petrol car from 2001+ or diesel from 2004+ (EU). The OBD port is usually under the dashboard by the driver's knees
- Python 3 on a Mac or Linux machine

## First run

1. Plug the adapter into the car's OBD port and your laptop's USB port
2. Turn the ignition on (engine can stay off)
3. Run `ls /dev/tty.usbserial*` and copy what it prints, e.g. `/dev/tty.usbserial-ABBC2GWD`
4. Paste that into the `PORT = "..."` line near the top of `reader.py` and `app.py`
5. Run `python3 reader.py`. You should see the fault codes, then live values updating every second

## Features

- Live RPM, speed, coolant temp and throttle position
- Reads and decodes stored fault codes (e.g. `P0133`) and check engine light status
- Works on CAN and older K-line cars
- Terminal reader or live browser dashboard (Flask)

## How it works

`obd_serial.py` sends commands to the ELM327 over USB serial. `pid_decoder.py` turns the hex replies into real values:

- Replies echo the request + `0x40` (`01` → `41`), the same rule UDS (ISO 14229) uses
- RPM = `((A × 256) + B) / 4`, coolant = `A − 40`
- Fault codes are packed into 2 bytes: letter (P/C/B/U), digit, then 3 hex digits

**Bug fixed:** waiting a fixed 0.3 s per reply worked on CAN but broke on slower K-line cars, so it now reads until the ELM327's `>` prompt.

## Run it

```bash
pip3 install -r requirements.txt
ls /dev/tty.usbserial*        # find your port, set PORT in reader.py / app.py
python3 pid_decoder.py        # tests, no car needed
python3 reader.py             # terminal
python3 app.py                # dashboard at localhost:5000
```

Ignition on; the engine doesn't need to be running.

## Next steps

- Raw CAN bus capture (CANable 2.0) to reverse-engineer non-standard signals
- More PIDs and CSV logging