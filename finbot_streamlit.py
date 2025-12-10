import streamlit as st
from data_handler import load_user_database, normalize_account_no, get_user
from finbot_core import (
    load_db, evaluate_application, extract_salary_from_slip,
    create_sanction_pdf_if_approved
)
from sanction_letter import generate_sanction_letter

st.set_page_config(page_title="FinBot", layout="centered")

st.title("🤖 FinBot – Autonomous Loan Assistant")
st.write("Smart, fast and policy-compliant loan processing.")

# Load DB once
db = load_db()

with st.form("loan_form"):
    account_input = st.text_input("Account Number (e.g. ACC1001)")
    name = st.text_input("Applicant Name")
    loan_type = st.selectbox(
        "Loan Type", ["Personal Loan", "Home Loan", "Auto Loan"])

    amount = st.number_input("Requested Amount (₹)",
                             min_value=0.0, step=5000.0, format="%.2f")
    tenure = st.selectbox("Tenure (Months)", [12, 24, 36, 48, 60])

    salary_slip = st.file_uploader(
        "Upload Salary Slip (Optional)", type=["jpg", "png", "pdf"])
    submitted = st.form_submit_button("Check Eligibility")

if submitted:
    st.subheader("📌 Decision:")

    account = normalize_account_no(account_input)
    if not account:
        st.error("Please enter a valid account number.")
        st.stop()

    if account not in db:
        st.error("Account number not found in database.")
        st.stop()

    extracted_salary = None
    if salary_slip:
        with st.spinner("Extracting salary from uploaded file..."):
            extracted_salary = extract_salary_from_slip(salary_slip)
        if extracted_salary is None:
            st.info("Could not automatically extract salary from the uploaded file. You can re-upload a clearer image or leave it blank.")

    # Evaluate
    result = evaluate_application(
        account, amount, tenure, db, extracted_salary)

    status = result.get("status")
    if status in ("approved_instant", "approved_after_salary"):
        st.success("🎉 Loan Approved!")
        emi = result.get("emi", 0.0)
        rate = result.get("rate", 0.0)

        # Create sanction PDF
        pdf_path = create_sanction_pdf_if_approved(
            result, name or db[account].get("name", "Applicant"), amount, tenure)
        if pdf_path:
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "Download Sanction Letter (PDF)", f, file_name=pdf_path.name)
        st.metric("Monthly EMI", f"₹{emi:,.0f}")
        st.write(f"Interest Rate: {rate}%")

    elif status == "salary_required":
        st.warning(result.get("reason", "Salary slip required for this amount."))
        st.info("Upload a salary slip and try again.")
    elif status == "rejected":
        st.error(result.get("reason", "Application rejected."))
    else:
        st.error(result.get("reason", "An error occurred during evaluation."))
