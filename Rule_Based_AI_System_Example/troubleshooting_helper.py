# Paul Sachse
# === Rule-Based Tech Troubleshooter ===
# Type a symptom like "no internet" or "won't turn on" and follow the prompts.
# Knowledge base of issues and step-by-step troubleshooting

ISSUES = {
    "no internet": [
        "Make sure Airplane Mode and any VPN are OFF, and Wi-Fi is ON.",
        "If multiple devices are affected: power-cycle router/modem (unplug 30–60s, replug, wait 2–3 min).",
        "If only this device: restart it, forget Wi-Fi and reconnect with the correct password.",
        "If still down: check your ISP outage page using mobile data."
    ],
    "no power": [
        "Try a different outlet/power strip; reseat the power cable firmly.",
        "Desktop: ensure PSU rocker switch is ON (|). Laptop: plug in a known-good charger.",
        "Hold power button 15–20 seconds, release, then press again.",
        "If still dead: likely PSU/charger/battery—seek service."
    ],
    "no display": [
        "Confirm the computer is ON (fans/lights) and the monitor has power (LED).",
        "Check the video cable (HDMI/DP) both ends; pick the correct input on the monitor.",
        "Desktop with GPU: cable must go into the GPU port (not motherboard).",
        "Try another cable or monitor/TV."
    ],
    "slow": [
        "Close unused apps/tabs; save work and restart.",
        "Ensure >10% free disk space; remove large/temp files.",
        "Use Task Manager/Activity Monitor to end runaway processes.",
        "Disable heavy startup apps; apply OS updates."
    ],
    "printer": [
        "Check power, paper, ink/toner; clear paper jams.",
        "Cancel all pending jobs; restart printer and computer.",
        "Ensure printer is on the SAME network; re-add or reinstall driver if needed."
    ],
    "bluetooth": [
        "Toggle Bluetooth OFF/ON; ensure accessory is charged and within 2 meters.",
        "Forget the device and re-pair.",
        "Turn off Bluetooth on other nearby devices that may auto-connect."
    ],
    "overheating": [
        "Move device to a hard, ventilated surface; keep vents clear.",
        "Close high-CPU apps; save work and restart.",
        "Clean dust from vents/fans if safe; avoid soft surfaces.",
        "If still hot: likely thermal paste/fan issue—seek service."
    ],
    "battery not charging": [
        "Use a known-good charger/outlet; firmly reseat cable.",
        "Power off for 2 minutes, then charge while off.",
        "Check for bent/dirty charging port; gently clean if needed.",
        "If still not charging: battery/charger/port fault—seek service."
    ],
    "no sound": [
        "Check volume/mute and output device (speakers/headphones).",
        "Unplug/replug headphones; try different port or device.",
        "Restart the app and then the computer.",
        "If still silent: update/reinstall audio driver."
    ],
    "microphone not working": [
        "Unmute mic; raise input volume; choose the correct input device.",
        "Allow mic permissions in OS/app settings.",
        "Unplug/replug mic or headset; try another port.",
        "If still broken: update audio driver or try a different mic."
    ],
    "webcam not working": [
        "Close other apps that might be using the camera.",
        "Allow camera permissions in OS/app settings.",
        "Unplug/replug external webcam or try a different USB port.",
        "If still no video: update camera driver or try another camera."
    ],
    "usb device not recognized": [
        "Unplug and replug; try a DIFFERENT USB port.",
        "Restart the computer; then plug the device in again.",
        "Try a different cable or hub (or remove the hub).",
        "If still not recognized: driver/device fault likely."
    ],
    "vpn not connecting": [
        "Verify internet works WITHOUT VPN first.",
        "Toggle VPN OFF/ON; try a different server/location.",
        "Restart device; check date/time and credentials.",
        "If still failing: firewall/network or account issue—contact admin/ISP."
    ],
    "email not syncing": [
        "Check internet; refresh mailbox; verify credentials.",
        "Confirm mailbox isn’t full; clear out very large attachments.",
        "Restart the mail app; remove and re-add the account.",
        "If still stuck: server or account issue—check provider status."
    ],
    "keyboard not working": [
        "Check NumLock and keyboard power/battery (if wireless).",
        "Reconnect Bluetooth/USB dongle or cable; try another port.",
        "Restart the computer.",
        "If specific keys fail: try another keyboard."
    ],
    "touchpad not working": [
        "Make sure touchpad isn’t disabled (function key/OS setting).",
        "Toggle touchpad setting OFF/ON; disconnect external mouse.",
        "Restart the computer.",
        "If still dead: driver/hardware issue—seek support."
    ],
    "external drive not detected": [
        "Try a different USB port/cable; listen for spin-up or lights.",
        "Check Disk Management/Disk Utility for the drive; assign a letter/mount it.",
        "Try another computer.",
        "If still missing: enclosure/drive failure likely."
    ],
    "app won’t open": [
        "Force-quit the app and reopen; or restart the device.",
        "Update the app; clear cache/temp files if available.",
        "Reinstall the app.",
        "If still crashing: check OS updates or app compatibility."
    ],
    "browser pages won’t load": [
        "Check internet; try another website.",
        "Clear cache; disable extensions; try an incognito/private window.",
        "Restart the browser and then the device.",
        "If still broken: DNS/firewall/VPN issue likely."
    ],
    "os update failed": [
        "Free up disk space (>10%); plug into power.",
        "Restart and retry the update.",
        "Disable VPN/security apps temporarily and try again.",
        "If still failing: run built-in update troubleshooter/recovery."
    ]
}

# --- NATURAL LANGUAGE MATCHING IMPROVEMENTS (no imports) ---
# We normalize user text to handle punctuation, smart quotes, and variants like "won't" vs "wont".
def _normalize(text):
    t = text.lower()
    # Replace common smart quotes with ASCII apostrophe
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    # Remove punctuation by turning non-alnum into spaces
    cleaned = []
    for ch in t:
        if ch.isalnum() or ch.isspace():
            cleaned.append(ch)
        else:
            cleaned.append(" ")
    t = "".join(cleaned)
    # Collapse spaces and return tokens
    tokens = [w for w in t.split() if w]
    return tokens

# Triggers are lists of token-sets that must ALL be present (AND-match).
TRIGGERS = {
    "no internet": [
        ["no", "internet"], ["wifi", "down"], ["wifi", "not", "working"], ["no", "connection"],
        ["cant", "connect"], ["can't", "connect"], ["cannot", "connect"], ["lost", "internet"],
        ["no", "wifi"], ["internet", "down"], ["network", "down"]
    ],
    "no power": [
        ["no", "power"], ["wont", "turn", "on"], ["won't", "turn", "on"], ["doesnt", "turn", "on"],
        ["doesn't", "turn", "on"], ["cant", "turn", "on"], ["can't", "turn", "on"],
        ["wont", "power", "on"], ["won't", "power", "on"], ["no", "lights"], ["computer", "dead"],
        ["pc", "dead"], ["laptop", "dead"], ["won't", "start"], ["wont", "start"]
    ],
    "no display": [
        ["no", "display"], ["black", "screen"], ["no", "signal"], ["monitor", "not", "working"],
        ["screen", "blank"], ["screen", "black"]
    ],
    "slow": [
        ["slow"], ["lag"], ["freez"], ["unresponsive"], ["stutter"], ["sluggish"]
    ],
    "printer": [
        ["printer"], ["cant", "print"], ["can't", "print"], ["wont", "print"], ["won't", "print"], ["printer", "offline"]
    ],
    "bluetooth": [
        ["bluetooth"], ["cant", "pair"], ["can't", "pair"], ["wont", "pair"], ["won't", "pair"], ["not", "pairing"]
    ],
    "overheating": [
        ["overheat"], ["hot"], ["fan", "loud"], ["thermal"]
    ],
    "battery not charging": [
        ["battery", "not", "charging"], ["not", "charging"], ["won't", "charge"], ["wont", "charge"], ["charger", "not", "working"]
    ],
    "no sound": [
        ["no", "sound"], ["no", "audio"], ["sound", "not", "working"], ["speakers", "not", "working"], ["muted"]
    ],
    "microphone not working": [
        ["microphone"], ["mic", "not", "working"], ["mic", "muted"], ["no", "mic"]
    ],
    "webcam not working": [
        ["webcam"], ["camera", "not", "working"], ["no", "camera"], ["camera", "blocked"]
    ],
    "usb device not recognized": [
        ["usb", "not", "recognized"], ["usb", "device", "not", "recognized"], ["usb", "problem"]
    ],
    "vpn not connecting": [
        ["vpn"], ["vpn", "not", "connecting"], ["vpn", "won't", "connect"], ["vpn", "wont", "connect"]
    ],
    "email not syncing": [
        ["email", "not", "syncing"], ["mail", "not", "syncing"], ["inbox", "not", "updating"]
    ],
    "keyboard not working": [
        ["keyboard", "not", "working"], ["no", "keyboard"], ["keys", "not", "working"]
    ],
    "touchpad not working": [
        ["touchpad", "not", "working"], ["trackpad", "not", "working"], ["no", "touchpad"]
    ],
    "external drive not detected": [
        ["external", "drive", "not", "detected"], ["hard", "drive", "not", "detected"], ["ssd", "not", "detected"]
    ],
    "app won’t open": [
        ["app", "wont", "open"], ["app", "won't", "open"], ["app", "crash"], ["app", "not", "opening"]
    ],
    "browser pages won’t load": [
        ["browser", "not", "loading"], ["pages", "wont", "load"], ["pages", "won't", "load"], ["website", "not", "loading"]
    ],
    "os update failed": [
        ["update", "failed"], ["os", "update", "failed"], ["update", "error"], ["cant", "update"], ["can't", "update"]
    ]
}

# Small set of "cue words" per issue to score fuzzy matches (OR-match).
CUES = {
    "no internet": ["internet", "wifi", "network", "connect", "connection"],
    "no power": ["power", "dead", "turn", "start"],
    "no display": ["display", "screen", "signal", "monitor"],
    "slow": ["slow", "lag", "freeze", "stutter", "sluggish", "unresponsive"],
    "printer": ["printer", "print", "offline"],
    "bluetooth": ["bluetooth", "pair", "pairing"],
    "overheating": ["overheat", "hot", "thermal", "fan"],
    "battery not charging": ["battery", "charge", "charging", "charger"],
    "no sound": ["sound", "audio", "speaker", "volume", "muted"],
    "microphone not working": ["mic", "microphone", "input", "record"],
    "webcam not working": ["webcam", "camera", "video"],
    "usb device not recognized": ["usb", "recognized", "device"],
    "vpn not connecting": ["vpn", "connect", "connecting", "tunnel"],
    "email not syncing": ["email", "mail", "inbox", "sync"],
    "keyboard not working": ["keyboard", "keys", "typing"],
    "touchpad not working": ["touchpad", "trackpad", "cursor"],
    "external drive not detected": ["external", "drive", "disk", "hdd", "ssd", "detected"],
    "app won’t open": ["app", "open", "opening", "crash"],
    "browser pages won’t load": ["browser", "page", "website", "load", "loading"],
    "os update failed": ["update", "upgrade", "patch", "failed", "error"]
}

# Try an AND-match on trigger token patterns first; if none match, score by cue overlap.
def pick_issue(user_text):
    tokens = _normalize(user_text)
    token_set = set(tokens)

    # 1) Strict pattern match: if ANY pattern (all tokens present) matches, return that issue
    best_issue = None
    for issue, patterns in TRIGGERS.items():
        for pattern in patterns:
            # normalize pattern tokens the same way (apostrophes removed by _normalize)
            norm_pattern = _normalize(" ".join(pattern))
            if set(norm_pattern).issubset(token_set):
                return issue  # immediate confident match

    # 2) Fuzzy scoring: count cue word overlaps, pick highest score
    best_score = 0
    for issue, words in CUES.items():
        score = 0
        for w in words:
            # if cue word (normalized) appears in tokens, add to score
            if _normalize(w)[0] in token_set:
                score += 1
        if score > best_score:
            best_issue = issue
            best_score = score

    # Require at least 1 cue hit to avoid wild guesses
    return best_issue if best_score > 0 else None

# Run troubleshooting flow for a symptom (unchanged behavior)
def troubleshoot(symptom):
    issue = pick_issue(symptom)
    if not issue:
        print("Sorry, I don’t have a rule for that.")
        print("Try: no internet, no power, no display, slow, printer, bluetooth, overheating, battery not charging, no sound, microphone not working, webcam not working, usb device not recognized, vpn not connecting, email not syncing, keyboard not working, touchpad not working, external drive not detected, app won’t open, browser pages won’t load, os update failed.")
        return
    print("\n=== " + issue.upper() + " ===")
    for step in ISSUES[issue]:
        print("• " + step)
        ans = input("Did that fix it? (yes/no) ").strip().lower()
        if ans.startswith("y"):
            print("✅ Resolved!")
            return
    print("➡️ Still not fixed. Needs deeper support/repair.")

# --- Interactive loop (unchanged) ---
print("Simple Tech Troubleshooter (rule-based)")
print("Type 'exit' to quit.")

while True:
    text = input("\nDescribe the problem (e.g., 'no internet'): ").strip()
    if text.lower() == "exit":
        print("Goodbye!")
        break
    if text:
        troubleshoot(text)
