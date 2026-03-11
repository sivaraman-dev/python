# loan_logic.py
# ─────────────────────────────────────────────────────────────────
# Core Loan Eligibility Logic — Pure Python
# Powers both the website (via server.py) and CLI (run directly).
# ─────────────────────────────────────────────────────────────────


def check_loan_eligibility(age, income, credit_score, loan_amount, employment):
    """
    Check loan eligibility using nested if/elif conditions.

    Parameters:
        age          (int)   : Applicant's age in years
        income       (int)   : Annual income in INR
        credit_score (int)   : Credit score (300 – 900)
        loan_amount  (int)   : Requested loan amount in INR
        employment   (str)   : Employment type

    Returns:
        dict: { status, heading, reasons, details }
    """

    # ── STEP 1: Age Check ─────────────────────────────────────────
    if age < 21 or age > 65:
        return {
            "status": "rejected",
            "heading": "Not Eligible",
            "sub": "Age requirement not met",
            "reasons": [
                "Applicant must be at least 21 years old." if age < 21
                else "Applicant must be below 65 years of age.",
                "Please re-apply when you meet the age criteria."
            ],
            "details": {}
        }

    # ── STEP 2: Employment Check ──────────────────────────────────
    elif employment == "unemployed":
        return {
            "status": "rejected",
            "heading": "Application Rejected",
            "sub": "Employment criteria not met",
            "reasons": [
                "Currently unemployed applicants are not eligible.",
                "Please apply once you have a stable income source."
            ],
            "details": {}
        }

    # ── STEP 3: Minimum Credit Score ─────────────────────────────
    elif credit_score < 500:
        return {
            "status": "rejected",
            "heading": "Application Rejected",
            "sub": "Credit score too low",
            "reasons": [
                f"Your credit score of {credit_score} is below the minimum threshold of 500.",
                "Work on improving your credit score before applying.",
                "Pay existing dues and reduce credit utilization."
            ],
            "details": {
                "Your Score":       credit_score,
                "Minimum Required": 500
            }
        }

    # ── STEP 4: Minimum Income ────────────────────────────────────
    elif income < 200000:
        return {
            "status": "rejected",
            "heading": "Application Rejected",
            "sub": "Insufficient annual income",
            "reasons": [
                f"Annual income of ₹{income:,} is below the minimum ₹2,00,000.",
                "A higher income source is required to qualify."
            ],
            "details": {
                "Your Income":  f"₹{income:,}",
                "Min Required": "₹2,00,000"
            }
        }

    # ── STEP 5: Detailed Eligibility (nested if) ──────────────────
    else:
        dti = loan_amount / income   # Debt-to-Income ratio (loan ÷ annual income)
        emi_ratio = loan_amount / (income / 12)  # EMI burden: loan vs monthly income

        monthly_rate = 0.0083        # ~10% annual / 12
        months = 60                  # 5-year tenure
        emi = (loan_amount * monthly_rate * (1 + monthly_rate) ** months) / \
              ((1 + monthly_rate) ** months - 1)
        emi = round(emi)

        # EMI should not exceed 50% of monthly income (affordability check)
        monthly_income = income / 12
        emi_affordable = emi <= (monthly_income * 0.5)

        interest_rates = {
            "premium":     "8.5%",
            "standard":    "10.5%",
            "conditional": "13.0%"
        }

        # ── Premium Approval ──────────────────────────────────────
        # High score + high income + low DTI
        if credit_score >= 750 and income >= 600000 and dti <= 10 and emi_affordable:
            return {
                "status": "approved",
                "heading": "Congratulations!",
                "sub": "You qualify for a Premium Loan",
                "reasons": [
                    "Excellent credit score of 750 or above.",
                    f"Strong annual income of ₹{income:,}.",
                    f"Healthy loan-to-income ratio of {dti:.1f}x.",
                    "Low-risk applicant — best rate applied."
                ],
                "details": {
                    "Interest Rate":    interest_rates["premium"],
                    "Est. Monthly EMI": f"₹{emi:,}",
                    "Loan-to-Income":   f"{dti:.1f}x",
                    "Loan Category":    "Premium"
                }
            }

        # ── Standard Approval ─────────────────────────────────────
        # Good score + decent income + affordable EMI
        elif credit_score >= 650 and income >= 200000 and dti <= 15 and emi_affordable:
            return {
                "status": "approved",
                "heading": "Loan Approved",
                "sub": "You qualify for a Standard Loan",
                "reasons": [
                    f"Credit score of {credit_score} meets the requirement (≥650).",
                    f"Annual income of ₹{income:,} is sufficient.",
                    f"EMI of ₹{emi:,} is within 50% of monthly income.",
                    "Loan amount is manageable relative to income."
                ],
                "details": {
                    "Interest Rate":    interest_rates["standard"],
                    "Est. Monthly EMI": f"₹{emi:,}",
                    "Loan-to-Income":   f"{dti:.1f}x",
                    "Loan Category":    "Standard"
                }
            }

        # ── Conditional / Under Review ────────────────────────────
        # Borderline score or slightly high DTI but EMI is still payable
        elif credit_score >= 550 and dti <= 20 and emi_affordable:
            return {
                "status": "review",
                "heading": "Under Review",
                "sub": "Conditional approval — manual check needed",
                "reasons": [
                    "Application meets minimum criteria but needs manual review.",
                    "A guarantor or collateral document may be required.",
                    "Additional income proof or bank statements may be requested.",
                    f"Higher interest rate of {interest_rates['conditional']} applies."
                ],
                "details": {
                    "Interest Rate":    interest_rates["conditional"],
                    "Est. Monthly EMI": f"₹{emi:,}",
                    "Loan-to-Income":   f"{dti:.1f}x",
                    "Status":           "Manual Review"
                }
            }

        # ── Rejected ──────────────────────────────────────────────
        else:
            issues = []
            if credit_score < 550:
                issues.append(f"Credit score ({credit_score}) is too low. Minimum required: 550.")
            if not emi_affordable:
                emi_pct = round((emi / monthly_income) * 100)
                issues.append(f"EMI (₹{emi:,}) is {emi_pct}% of monthly income — exceeds 50% limit. Request a smaller loan.")
            if dti > 20:
                issues.append(f"Loan amount (₹{loan_amount:,}) is {dti:.0f}x your annual income. Reduce the loan amount.")

            return {
                "status": "rejected",
                "heading": "Application Rejected",
                "sub": "Profile does not meet lending criteria",
                "reasons": issues if issues else ["Profile does not meet lending criteria."],
                "details": {
                    "Credit Score": credit_score,
                    "Income":       f"₹{income:,}",
                    "DTI Ratio":    f"{dti:.1f}x",
                    "Decision":     "Declined"
                }
            }


# ─── DISPLAY HELPER ───────────────────────────────────────────────────────────
def display_result(result):
    print("\n" + "=" * 55)
    print(f"  {result['heading']}")
    print("=" * 55)

    if result["details"]:
        print("\n  📊 Details:")
        for k, v in result["details"].items():
            print(f"     {k:<22}: {v}")

    print("\n  📋 Key Factors:")
    for reason in result["reasons"]:
        print(f"     • {reason}")
    print()


# ─── INTERACTIVE CLI ──────────────────────────────────────────────────────────
def main():
    print("\n╔══════════════════════════════════════╗")
    print("║       LoanIQ — Eligibility Check     ║")
    print("╚══════════════════════════════════════╝\n")

    try:
        age          = int(input("  Enter your Age                   : "))
        income       = int(input("  Enter Annual Income (₹)          : "))
        credit_score = int(input("  Enter Credit Score (300-900)     : "))
        loan_amount  = int(input("  Enter Loan Amount Requested (₹)  : "))
        print("  Employment types: salaried, self_employed, business, freelance, retired, unemployed")
        employment   = input("  Enter Employment Type            : ").strip().lower()
    except ValueError:
        print("\n  ❌ Invalid input. Please enter numbers only where required.")
        return

    result = check_loan_eligibility(age, income, credit_score, loan_amount, employment)
    display_result(result)


if __name__ == "__main__":
    main()
