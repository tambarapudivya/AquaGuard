def detect_leak(water_usage):
    if water_usage > 100:
        return "High Leakage Detected"
    elif water_usage > 50:
        return "Possible Leakage"
    else:
        return "Normal Water Usage"
