from datetime import datetime

try:
    from backend.config import ALERT_CONFIG
except ImportError:
    from config import ALERT_CONFIG


def generate_alert(animal, confidence=None):
    """
    Generate structured alert payload for a detected animal.
    """
    animal_key = str(animal).lower()
    config = ALERT_CONFIG.get(
        animal_key,
        {
            "severity": "UNKNOWN",
            "message": f"{animal.capitalize()} detected in field.",
            "buzzer": True,
            "led": True,
            "gsm": False
        }
    )

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    alert = {
        "animal": animal_key,
        "confidence": confidence,
        "severity": config["severity"],
        "message": config["message"],
        "timestamp": timestamp,
        "buzzer": config.get("buzzer", True),
        "led": config.get("led", True),
        "gsm": config.get("gsm", False)
    }

    print("\n========== ANIMAL ALERT ==========")
    print(f"Animal      : {animal.capitalize()}")
    if confidence is not None:
        print(f"Confidence  : {confidence:.2f}")
    print(f"Severity    : {alert['severity']}")
    print(f"Message     : {alert['message']}")
    print(f"Time        : {timestamp}")
    print(f"Buzzer      : {'ON' if alert['buzzer'] else 'OFF'}")
    print(f"LED         : {'ON' if alert['led'] else 'OFF'}")
    print(f"GSM         : {'ON' if alert['gsm'] else 'OFF'}")
    print("==================================\n")

    return alert