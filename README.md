# 📄 Invoice Finance IRR Simulator

This is a simple Streamlit app to simulate and compare **IRR (Internal Rate of Return)** across multiple invoice financing scenarios.
---
.
## 🔧 Features

- 📥 Upload invoice data via CSV
- ✍️ Manually edit invoice parameters in-app
- 💹 Calculates annualized IRR based on:
  - Invoice amount
  - Discount rate
  - Tenor (days)
  - Optional default probability and recovery rate
- 📊 Results presented in a dynamic table
- ⬇️ Download calculated IRR results as CSV

---

## 📁 Sample CSV Format

| Invoice Amount (₹) | Discount Rate (%) | Tenor (Days) | Default Probability (%) | Recovery Rate (%) |
|--------------------|--------------------|--------------|--------------------------|--------------------|
| 100000             | 2.0                | 60           | 0.0
