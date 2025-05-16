import streamlit as st
import pandas as pd
import datetime
from scipy.optimize import newton
from io import StringIO

# --- Page Config ---
st.set_page_config(page_title="Invoice IRR Calculator", layout="wide")

# --- Title Section ---
st.markdown("""
    <h1 style='text-align: center; color: #003366;'>📄 Invoice Finance IRR Simulator</h1>
    <p style='text-align: center; color: gray;'>Model and compare invoice-level IRRs with optional risk adjustments</p>
    <hr style='border: 1px solid #ccc;'>
""", unsafe_allow_html=True)

# IRR Calculation Helpers
def xnpv(rate, cashflows, days):
    return sum([cf / (1 + rate) ** (d / 365) for cf, d in zip(cashflows, days)])

def xirr(cashflows, days, guess=0.1):
    try:
        return newton(lambda r: xnpv(r, cashflows, days), guess)
    except (RuntimeError, OverflowError):
        return None

# --- Sidebar ---
st.sidebar.title("📁 Data Input")
st.sidebar.markdown("Upload a CSV file or enter manually.")

uploaded_file = st.sidebar.file_uploader("Upload Invoice CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.sidebar.subheader("Manual Entry")
    row_count = st.sidebar.number_input("Number of Invoices", min_value=1, max_value=20, value=3)
    df = pd.DataFrame({
        "Invoice Amount (₹)": [100000] * row_count,
        "Discount Rate (%)": [2.0] * row_count,
        "Tenor (Days)": [60] * row_count,
        "Default Probability (%)": [0.0] * row_count,
        "Recovery Rate (%)": [0.0] * row_count
    })

# --- Data Entry Table ---
st.markdown("## 📊 Invoice Data")
st.markdown("Use the table below to enter or adjust invoice parameters.")
edited_df = st.data_editor(df, num_rows="dynamic")

# --- IRR Calculations ---
st.markdown("## 🧮 IRR Calculation Results")
today = datetime.date.today()
results = []

for i, row in edited_df.iterrows():
    invoice_amt = row["Invoice Amount (₹)"]
    discount = row["Discount Rate (%)"]
    tenor = row["Tenor (Days)"]
    default_prob = row.get("Default Probability (%)", 0.0)
    recovery_rate = row.get("Recovery Rate (%)", 0.0)

    disbursed = invoice_amt * (1 - discount / 100)
    expected_payback = (invoice_amt * (1 - default_prob / 100)) + \
                       (invoice_amt * (default_prob / 100) * (recovery_rate / 100))

    cashflows = [-disbursed, expected_payback]
    days = [0, tenor]
    irr = xirr(cashflows, days)
    annualized_irr = irr * 100 if irr is not None else None

    results.append({
        "Invoice Amount (₹)": invoice_amt,
        "Disbursed (₹)": round(disbursed, 2),
        "Expected Payback (₹)": round(expected_payback, 2),
        "IRR (%)": round(annualized_irr, 2) if annualized_irr else "Error"
    })

result_df = pd.DataFrame(results)
st.dataframe(result_df, use_container_width=True)

# --- Download Button ---
csv = result_df.to_csv(index=False)
st.download_button(
    label="⬇️ Download Results as CSV",
    data=csv,
    file_name="invoice_irr_results.csv",
    mime="text/csv",
    help="Download the IRR results as a CSV file."
)

# --- Footer ---
st.markdown("""
    <hr>
    <p style='text-align: center; color: gray;'>Created by <b>Jayakrishnan K.S.</b> | A finance-analytics portfolio project</p>
""", unsafe_allow_html=True)
