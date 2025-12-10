from datetime import datetime
from pathlib import Path
from sanction_letter import generate_sanction_letter

OUT_DIR = Path("sanction_letters")
OUT_DIR.mkdir(exist_ok=True)


def generate_sanction_letter_console(name, account_no, amount, tenure_months, emi, rate, out_dir=OUT_DIR):
    """
    Console wrapper to create a sanction letter (uses sanction_letter.generate_sanction_letter).
    Returns Path.
    """
    return generate_sanction_letter(name, account_no, amount, tenure_months, emi, rate, out_dir=out_dir)


# Example usage if run directly (won't run unless imported/run manually)
if __name__ == "__main__":
    p = generate_sanction_letter_console(
        "Test User", "ACC0000", 100000, 24, 4600, 10.5)
    print(f"Generated: {p}")
