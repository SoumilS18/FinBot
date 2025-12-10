from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime
from pathlib import Path

OUT_DIR = Path("sanction_letters")
OUT_DIR.mkdir(exist_ok=True)


def generate_sanction_letter(name, account_no, amount, tenure_months, emi, rate, out_dir=OUT_DIR):
    """
    Create a nicely formatted sanction letter PDF and return Path to file.
    """
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = out_dir / \
        f"sanction_{str(account_no).replace(' ', '_')}_{ts}.pdf"

    c = canvas.Canvas(str(filename), pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, height - 80, "Loan Sanction Letter")
    c.setLineWidth(1)
    c.line(50, height - 90, width - 50, height - 90)

    # Body
    c.setFont("Helvetica", 12)
    y = height - 130
    c.drawString(50, y, f"Date: {datetime.now().strftime('%d %b %Y')}")
    y -= 30
    c.drawString(50, y, f"Applicant Name: {name}")
    y -= 20
    c.drawString(50, y, f"Account Number: {account_no}")
    y -= 30

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Loan Details:")
    y -= 22

    c.setFont("Helvetica", 12)
    try:
        c.drawString(50, y, f"Loan Amount Approved: ₹{amount:,.0f}")
    except Exception:
        c.drawString(50, y, f"Loan Amount Approved: ₹{amount}")
    y -= 18
    c.drawString(50, y, f"Tenure: {tenure_months} months")
    y -= 18
    c.drawString(50, y, f"Interest Rate: {rate}%")
    y -= 18
    try:
        c.drawString(50, y, f"Monthly EMI: ₹{emi:,.0f}")
    except Exception:
        c.drawString(50, y, f"Monthly EMI: ₹{emi}")
    y -= 30

    c.setFont("Helvetica-Oblique", 11)
    c.drawString(
        50, y, "This sanction is subject to document verification and final approval.")
    y -= 18
    c.drawString(50, y, "Please retain this document for your records.")

    # Footer / sign
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 80, "Authorized Signatory")
    c.drawString(50, 65, "FinBot Lending Services")

    c.save()
    return filename
