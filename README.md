🚀 FinBot – Automated Loan Eligibility & Sanction Letter Generator

FinBot is a lightweight, intelligent loan-processing assistant that automates eligibility checks, EMI calculation, and PDF sanction letter generation using Python.
It includes a web UI (Streamlit) and console interface, backed by a modular core engine.


🔧 Features

✔ Automated loan eligibility check
✔ Accurate EMI calculation
✔ Instant PDF sanction letter generation (FPDF)
✔ Streamlit-based web interface
✔ Console-based CLI interface
✔ Modular architecture (easy to extend with APIs / ML / rule updates)


📁 Project Structure

├── finbot_core.py          # Main loan processing engine
├── finbot_console.py       # Console interface (terminal-based)
├── finbot_streamlit.py     # Streamlit web UI
├── sanction_letter.py      # PDF generator using FPDF
├── data_handler.py         # Input handler + preprocessing utilities
├── sample_db.json          # Dummy dataset for analytics/demo


⚙️ How It Works

User enters loan details (via Web UI or Console)
System fetches/reads required data (mock or uploaded)
Eligibility rules are applied
EMI is computed
Decision Engine approves/rejects
A beautifully formatted PDF sanction letter is generated


▶️ Run the Project

1️⃣ Run Streamlit Web App
streamlit run finbot_streamlit.py
2️⃣ Run Console Version
python finbot_console.py


📊 Analytics Demo

A dummy dataset (sample_db.json) is included for:
Loan tenure distribution
Credit score ranges
Feature correlation heatmaps
You can plug this into any ML/analytics pipeline later.


🛠 Technologies Used

Python
Streamlit
Pandas / NumPy
FPDF
JSON


🚀 Future Enhancements

API-based real-time KYC and income verification
Conversation-style chatbot UI
Advanced risk scoring engine
Underwriter dashboard
