import json
from pathlib import Path

DB_FILE = Path("sample_db.json")


def load_user_database():
    """Loads the JSON database containing user account details."""
    try:
        with DB_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print("❌ ERROR: sample_db.json not found!")
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: sample_db.json decode error: {e}")
        return {}


def normalize_account_no(account_no: str) -> str:
    """Normalize account number input to match keys in the DB."""
    if account_no is None:
        return ""
    return str(account_no).strip().upper()


def get_user(account_no):
    """Returns user data for the given account number (normalized)."""
    database = load_user_database()
    key = normalize_account_no(account_no)
    return database.get(key, None)
