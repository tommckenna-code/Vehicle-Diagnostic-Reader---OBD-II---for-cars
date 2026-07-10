# Vehicle Diagnostic Reader — OBD-II for Cars


vehicle-diagnostic-reader/
│
│   ├── obd_serial.py          # raw AT command handshake
│   ├── pid_decoder.py         # manual hex decoding (RPM/speed/temp/throttle)
│   ├── reader.py              # CLI test
│   ├── app.py                 # Flask + background polling thread
│   │    
│   ├── template/
│       └── index.html     # dashboard
│
└── README.md                # Project documentation

Python tool for interfacing with a vehicle's OBD-II (on board diagnostics) port via ELM327 
adapter, implementing the ISO 15765-4 CAN transport protocol.

## What it does
- Reads live engine PIDs (RPM, coolant temp, throttle position, vehicle speed)
- Retrieves and decodes Diagnostic Trouble Codes (DTCs) per SAE J1979
- Logs session data to CSV for offline analysis
- [In development] Enumerates exposed UDS (ISO 14229) services as a 
  security baseline

## Hardware
- ELM327 USB adapter (FTDI chip)
- Tested on: [VolksWagen golf TDI/diesel/2018]
- OBD-II connector: ISO 15765-4 (CAN 11-bit, 500kbps)

## Protocols
- SAE J1979 — OBD-II diagnostic services (Mode 01, 03, 07)
- ISO 15765-4 — CAN-based OBD-II transport layer
- ELM327 AT command set for adapter communication

## Why this matters for automotive security
The OBD-II port is an unauthenticated diagnostic interface present on 
all post-2001 vehicles. Mapping what services are exposed is foundational 
to ECU security assessment and Threat Analysis and Risk Assessment (TARA) 
under ISO 21434.

## Setup
pip install obd

python diagnostic_reader.py

## Planned extensions once standard functions are working
- UDS service enumeration (ISO 14229)
- CAN frame capture and logging mode
- DTC lookup against known vulnerability patterns
  
## NOTE
This is an active learning project, not an advertised diagnostics tool. Always follow manufacturer/manual guidance and never use diagnostic tools in a way that interferes safe driving, but feel free to use or expand thanks.


