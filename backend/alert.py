from datetime import datetime


def generate_alert(animal, confidence):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    alert = {
        "animal": animal,
        "confidence": confidence,
        "timestamp": timestamp,
        "buzzer": True,
        "led": True,
        "gsm": True
    }

    print("\n========== ANIMAL ALERT ==========")
    print(f"Animal      : {animal}")
    print(f"Confidence  : {confidence:.2f}")
    print(f"Time        : {timestamp}")
    print("Buzzer      : ON")
    print("LED         : ON")
    print("GSM         : ON")
    print("==================================\n")

    return alert