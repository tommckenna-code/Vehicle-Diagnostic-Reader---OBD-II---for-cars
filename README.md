# Vehicle-Diagnostic-Reader---OBD-II---for-cars
On Board Diagnostics 2 are the automotive diagnostics tool and this project will be designed around it as an open source interface paired with ELM327 adapters, Python and Visual Basic.NET. This will demonstrate cross platform capability in reading real time vehicle telemetry, decoding diagnostic troubleshooting codes and displaying/reading live engine metrics.

Built as a personal project to explore embeedded systems, vehical telemetry and hte intersection of software engineering with the automotive industry.

## How it works

The tool connects to an ELM327 Bluetooth OBD-II adapter plugged into
any car manufactured from 2001 (petrol) / 2004 (diesel) onwards in
the UK/EU. It queries the vehicle's ECU for live data and diagnostic
trouble codes (DTCs).

## Features

- Live engine data: RPM, speed, coolant temperature, throttle position
- Stored fault code (DTC) reading
- Demo mode for testing without hardware

## How to run

```
pip install obd
python obd_reader.py
```

Set `DEMO_MODE = True` to test without a vehicle connected, or
`False` once your ELM327 adapter is paired and the vehicle is running.

## Hardware required

- ELM327 Bluetooth OBD-II adapter (~£10)
- Any OBD-II compliant vehicle

## Tech used

- Python 3
- python-obd library

## NOTE
This is an active learning project, not an advertised diagnostics tool. Always follow manufacturer/manual guidance and never use diagnostic tools in a way that could distract safe driving, but feel free to use thanks.


