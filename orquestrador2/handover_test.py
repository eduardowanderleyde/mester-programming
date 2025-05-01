import time
from wifi_scanner import scan_wifi

previous_bssid = None

def detect_handover():
    global previous_bssid
    wifi_info = scan_wifi()

    if wifi_info and isinstance(wifi_info, list):
        current_bssid = wifi_info[0]["BSSID"]

        if previous_bssid is not None and previous_bssid != current_bssid:
            print(f"⚠️ Handover detectado: {previous_bssid} → {current_bssid}")
            previous_bssid = current_bssid
            return {"handover": True, "new_bssid": current_bssid}

        previous_bssid = current_bssid
    return {"handover": False}

if __name__ == "__main__":
    while True:
        print(detect_handover())
        time.sleep(5)
