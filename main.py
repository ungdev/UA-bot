from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
import os
import sys
import zoneinfo

# Charger les variables d'environnement
load_dotenv()

# Récupération des variables d'environnement
try:
    UA_TIMESTAMP: int = int(os.getenv('UA_TIMESTAMP', 0)) + 60
    if UA_TIMESTAMP == 60:
        raise ValueError("La variable d'environnement UA_TIMESTAMP est manquante ou invalide.")
    WEBHOOK_URL: str = os.getenv('WEBHOOK_URL', '')
    if not WEBHOOK_URL:
        raise ValueError("La variable d'environnement WEBHOOK_URL est manquante.")
except ValueError as e:
    print(f"Erreur de configuration : {e}")
    sys.exit(1)


def send_to_discord(message: str) -> None:
    """Envoie un message au canal Discord via un webhook."""
    try:
        response = requests.post(WEBHOOK_URL, data={'content': message})
        response.raise_for_status()
    except requests.RequestException as e:
        log(f"Erreur lors de l'envoi à Discord : {e}")


def log(message: str) -> None:
    """Écrit un message dans la console."""
    print(f'{datetime.now()} - {message}\n')


def main() -> None:
    """Fonction principale."""
    now: datetime = datetime.now(zoneinfo.ZoneInfo("Europe/Paris"))
    time_to_ua: timedelta = datetime.fromtimestamp(UA_TIMESTAMP) - now
    hours_to_ua: int = int(time_to_ua.total_seconds() // 3600)
    days_to_ua: int = int(time_to_ua.total_seconds() // 86400)

    if hours_to_ua < 1:
        send_to_discord("# Ils sont là ! :tada:")
        log("# Ils sont là ! :tada:")
        return

    if time_to_ua >= timedelta(weeks=1):
        if (now.hour, now.minute) == (17, 0):
            message = f"## Plus que {days_to_ua} jours (environ) avant l'UA ! :clock:"
            send_to_discord(message)
            log(message)
        else:
            log("Rien à faire pour l'instant.")
        return

    message = f"Ils débarquent dans **{hours_to_ua} heures** ! :fearful:"
    send_to_discord(message)
    log(message)


if __name__ == '__main__':
    main()