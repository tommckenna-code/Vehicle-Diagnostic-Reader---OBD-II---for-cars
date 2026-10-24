"""
pid_decoder.py
Manually decodes OBD-II PID hex responses into real values.
This is deliberately NOT using python-obd's built-in decoding —
doing it by hand is what actually demonstrates protocol understanding
on a CV/portfolio.

Response format from ELM327 for Mode 01 requests looks like:
    "41 0C 1A F8"
    41       = response to mode 01 (mode + 0x40)
    0C       = PID echoed back (RPM)
    1A F8    = data bytes A and B
"""


def clean_response(raw):
    """Keep only the last line, and only if it's a real reply (starts with 4x).
    Handles 'BUS INIT: ...OK' on K-line cars and errors like 'NO DATA'."""
    lines = raw.replace(">", "").strip().splitlines()
    parts = lines[-1].split() if lines else []
    return parts if parts and parts[0].startswith("4") else []


def decode_rpm(raw):
    """PID 0C — Engine RPM. Formula: ((A*256)+B)/4"""
    parts = clean_response(raw)
    if len(parts) < 4:
        return None
    A = int(parts[2], 16)
    B = int(parts[3], 16)
    return ((A * 256) + B) / 4


def decode_speed(raw):
    """PID 0D — Vehicle speed in km/h. Formula: A"""
    parts = clean_response(raw)
    if len(parts) < 3:
        return None
    return int(parts[2], 16)


def decode_coolant_temp(raw):
    """PID 05 — Coolant temp in Celsius. Formula: A - 40"""
    parts = clean_response(raw)
    if len(parts) < 3:
        return None
    return int(parts[2], 16) - 40


def decode_throttle_pos(raw):
    """PID 11 — Throttle position %. Formula: A * 100 / 255"""
    parts = clean_response(raw)
    if len(parts) < 3:
        return None
    return round(int(parts[2], 16) * 100 / 255, 1)


def decode_status(raw):
    """PID 01 -> (check engine light on?, number of stored codes)"""
    parts = clean_response(raw)
    if len(parts) < 3:
        return None
    A = int(parts[2], 16)
    return bool(A & 0x80), A & 0x7F


def decode_dtcs(raw):
    """Mode 03 response -> ['P0133', ...]. Each code is 2 bytes."""
    codes = []
    for line in raw.splitlines():
        b = line.split()
        if not b or b[0] != "43":
            continue
        start = 2 if (len(b) - 1) % 2 else 1   # CAN cars add a count byte, K-line doesn't
        for i in range(start, len(b) - 1, 2):
            v = int(b[i] + b[i + 1], 16)
            if v:
                codes.append("PCBU"[v >> 14] + str((v >> 12) & 3) + f"{v & 0xFFF:03X}")
    return codes


DECODERS = {
    "0C": decode_rpm,
    "0D": decode_speed,
    "05": decode_coolant_temp,
    "11": decode_throttle_pos,
}


if __name__ == "__main__":
    assert decode_rpm("41 0C 1A F8") == 1726.0
    assert decode_rpm("BUS INIT: ...OK\r41 0C 1A F8") == 1726.0   # K-line first reply
    assert decode_coolant_temp("41 05 5A") == 50
    assert decode_coolant_temp("UNABLE TO CONNECT") is None
    assert decode_status("41 01 82 07 65 04") == (True, 2)
    assert decode_dtcs("43 01 33 00 00 00 00") == ["P0133"]       # K-line (Polo)
    assert decode_dtcs("43 01 01 33") == ["P0133"]                # CAN (Golf)
    print("ok")