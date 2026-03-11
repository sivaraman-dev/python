# 🏦 LoanIQ — Loan Eligibility Checker

A full web project powered by **Pure Python** (no frameworks needed).

## 📁 Project Structure

```
loaniq/
├── index.html       ← Web page (HTML structure)
├── style.css        ← Styling and animations
├── script.js        ← UI interactions + sends data to Python
├── loan_logic.py    ← Eligibility logic (used by server + CLI)
├── server.py        ← Pure Python web server (http.server)
└── README.md        ← This file
```

## 🚀 How to Run the Website

1. Open terminal inside the `loaniq` folder
2. Run:   python server.py
3. Open browser → http://localhost:5000
4. Fill form → click Check My Eligibility
5. Ctrl+C to stop

## 💻 Run as CLI

  python loan_logic.py

## 🔗 How the Files Connect

  Browser (index.html)
    ├── loads style.css
    ├── loads script.js
    └── POST /check ──► server.py ──► loan_logic.py ──► JSON back to browser

## 🧠 Eligibility Rules

  Age < 21 or > 65              → Rejected
  Unemployed                    → Rejected
  Credit Score < 500            → Rejected
  Income < ₹2,00,000            → Rejected
  Score≥750, Income≥₹8L, DTI≤5  → Premium Approved
  Score≥650, Income≥₹4L, DTI≤8  → Standard Approved
  Score≥600, Income≥₹3L, DTI≤10 → Under Review
  Everything else               → Rejected
