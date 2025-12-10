# finbot_core.py
from pathlib import Path
from datetime import datetime
import json
import re
from typing import Optional

from PIL import Image
import pytesseract

from sanction_letter import generate_sanction_letter

# Make Tesseract path optional (works cross-platform if tesseract is in PATH)
# If you need a specific path, set an environment variable TESSERACT_CMD or uncomment and set here.
# Example (Windows): pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

DB_FILE = Path("sample_db.json")
SALARY_SLIP_DIR = Path("salary_slips")
SALARY_SLIP_DIR.mkdir(exist_ok=True)
SANCTION_DIR = Path("sanction_letters")
SANCTION_DIR.mkdir(exist_ok=True)


def load_db():
    """Load the JSON DB. Returns dict (empty on error)."""
    try:
        with DB_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading DB: {e}")
        return {}


def normalize_account_no(account_no: str) -> str:
    if not account_no:
        return ""
    return str(account_no).strip().upper()


def calculate_emi(principal: float, annual_rate_percent: float, tenure_months: int) -> float:
    """
    Standard EMI formula. Handles zero interest and invalid inputs gracefully.
    """
    try:
        principal = float(principal)
        r = float(annual_rate_percent) / (12.0 * 100.0)
        n = int(tenure_months)
        if n <= 0:
            return 0.0
        if abs(r) < 1e-12:
            return principal / n
        # guard against overflow by using pow with floats
        numerator = principal * r * (1 + r) ** n
        denominator = (1 + r) ** n - 1
        if abs(denominator) < 1e-12:
            return principal / n
        emi = numerator / denominator
        if not (emi == emi):  # NaN check
            return 0.0
        return emi
    except Exception:
        return 0.0


def extract_salary_from_slip(uploaded_file) -> Optional[float]:
    """
    Accepts a file from Streamlit's uploader (has .name and getbuffer()).
    Returns extracted salary (int/float) or None if extraction failed.
    """
    try:
        # Save file locally
        file_path = SALARY_SLIP_DIR / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # If PDF, skip advanced OCR in this simplified version
        if uploaded_file.name.lower().endswith(".pdf"):
            return None

        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)

        # look for 4-8 digit numbers (salary-like); choose the largest plausible one
        numbers = re.findall(r"\d{4,9}", text.replace(",", ""))
        if not numbers:
            return None
        nums = [int(n) for n in numbers]
        # Heuristic: salary is the largest extracted numeric value but not unreasonably large
        cand = max(nums)
        if cand > 10_000_000:  # improbable salary
            return None
        return float(cand)
    except Exception:
        return None


def evaluate_application(raw_account_no: str, requested_amount: float, tenure_months: int, db: dict, provided_salary: Optional[float] = None) -> dict:
    """
    Evaluate loan application and return a consistent result dict.

    Possible statuses:
      - error (with reason)
      - rejected (with reason)
      - salary_required (with reason)
      - approved_instant (emi, rate)
      - approved_after_salary (emi, rate)
    """
    try:
        account_no = normalize_account_no(raw_account_no)
        if not account_no:
            return {"status": "error", "reason": "Invalid account number."}

        customer = db.get(account_no)
        if not customer:
            return {"status": "error", "reason": "Account not found."}

        pre_limit = float(customer.get("preapproved_limit", 0))
        credit_score = int(customer.get("credit_score", 0))

        # Rule 1: credit score check
        if credit_score < 700:
            return {"status": "rejected", "reason": f"Credit score below threshold (score={credit_score})."}

        # Rule 2: instant approval if within preapproved limit
        if requested_amount <= pre_limit:
            rate = 10.5
            emi = calculate_emi(requested_amount, rate, tenure_months)
            return {"status": "approved_instant", "emi": emi, "rate": rate, "account": account_no}

        # Rule 3: needs salary verification for up to 2x pre_limit
        if requested_amount <= 2 * pre_limit:
            if provided_salary is None:
                return {"status": "salary_required", "reason": "Salary slip required for this requested amount.", "account": account_no}
            rate = 10.5
            emi = calculate_emi(requested_amount, rate, tenure_months)
            # EMI-to-salary check: EMI must be <= 50% of salary
            if emi <= 0.5 * provided_salary:
                return {"status": "approved_after_salary", "emi": emi, "rate": rate, "account": account_no}
            else:
                return {"status": "rejected", "reason": f"EMI ₹{emi:,.0f} exceeds 50% of salary ₹{provided_salary:,.0f}.", "account": account_no}

        # Rule 4: requested > 2x pre-limit => reject
        return {"status": "rejected", "reason": "Requested amount exceeds 2× pre-approved limit.", "account": account_no}
    except Exception as e:
        return {"status": "error", "reason": f"Evaluation error: {e}"}


def create_sanction_pdf_if_approved(result: dict, applicant_name: str, requested_amount: float, tenure_months: int):
    """
    If result indicates approval, create a PDF and return its Path.
    Otherwise return None.
    """
    if result.get("status") in ("approved_instant", "approved_after_salary"):
        emi = result.get("emi", 0.0)
        rate = result.get("rate", 0.0)
        account = result.get("account", "UNKNOWN")
        return generate_sanction_letter(applicant_name, account, requested_amount, tenure_months, emi, rate)
    return None
