#!/usr/bin/env python3
import streamlit as st

def calculate_tax_new_regime(taxable_income, is_senior_citizen=False):
    """
    Calculate income tax under New Tax Regime for FY 2025–26 (AY 2026–27).
    Supports resident individuals, including senior citizens.
    """
    # New Regime slabs (FY 2025–26, Budget 2025)
    slabs = [
        (0, 400000, 0.0),  # Basic exemption ₹4 lakh
        (400001, 700000, 0.05),
        (700001, 1000000, 0.10),
        (1000001, 1200000, 0.15),
        (1200001, 1500000, 0.20),
        (1500001, float('inf'), 0.30),
    ]

    tax = 0
    for lower, upper, rate in slabs:
        if taxable_income > lower:
            tax += (min(taxable_income, upper) - lower) * rate
        else:
            break

    # Section 87A rebate: Up to ₹12 lakh taxable income, max ₹60,000
    rebate = 0
    if taxable_income <= 1200000:
        rebate = min(tax, 60000)
        tax -= rebate

    # Health and Education Cess (4%)
    cess = tax * 0.04
    total_tax = tax + cess

    return {
        "tax_before_rebate": round(tax, 2),
        "rebate_87A": round(rebate, 2),
        "cess": round(cess, 2),
        "total_tax": round(total_tax, 2)
    }

def main():
    st.set_page_config(page_title="Income Tax Calculator FY 2025–26", page_icon="💰")
    st.title("Indian Income Tax Calculator (FY 2025–26, New Tax Regime)")
    st.markdown("""
        Calculate your income tax under the New Tax Regime for FY 2025–26 (AY 2026–27).
        Includes Section 87A rebate up to ₹12 lakh taxable income and standard deduction of ₹75,000.
        Built for resident individuals, including senior citizens.
    """)

    # Input form
    with st.form("tax_form"):
        st.header("Enter Your Income Details (₹)")
        salary = st.number_input("Annual Salary Income", min_value=0.0, value=0.0, step=1000.0)
        interest = st.number_input("Interest Income (e.g., bank deposits)", min_value=0.0, value=0.0, step=1000.0)
        capital_gains = st.number_input("Capital Gains (short/long-term, if taxable)", min_value=0.0, value=0.0, step=1000.0)
        mutual_funds = st.number_input("Mutual Fund Income (if not taxed separately)", min_value=0.0, value=0.0, step=1000.0)
        other_income = st.number_input("Other Income (e.g., rent, pension)", min_value=0.0, value=0.0, step=1000.0)
        agriculture_income = st.number_input("Agricultural Income (exempt up to ₹5,000)", min_value=0.0, value=0.0, step=1000.0)
        senior_citizen = st.checkbox("I am a Senior Citizen (60+ years)")

        submitted = st.form_submit_button("Calculate Tax")

    if submitted:
        try:
            # Validate inputs
            if any(x < 0 for x in [salary, interest, capital_gains, mutual_funds, other_income, agriculture_income]):
                st.error("Income values cannot be negative.")
                return

            # Calculate gross income
            gross_income = salary + interest + capital_gains + mutual_funds + other_income

            # Apply deductions
            std_deduction = 75000 if salary > 0 else 0
            agriculture_exemption = min(agriculture_income, 5000)
            taxable_income = max(0, gross_income - std_deduction - agriculture_exemption)

            # Calculate tax
            tax_result = calculate_tax_new_regime(taxable_income, senior_citizen)

            # Display results
            st.header("Tax Calculation Results")
            st.write(f"**Taxpayer Status**: {'Senior Citizen (60+)' if senior_citizen else 'Resident Individual'}")
            st.write(f"**Salary Income**: ₹{salary:,.2f}")
            st.write(f"**Interest Income**: ₹{interest:,.2f}")
            st.write(f"**Capital Gains**: ₹{capital_gains:,.2f}")
            st.write(f"**Mutual Fund Income**: ₹{mutual_funds:,.2f}")
            st.write(f"**Other Income**: ₹{other_income:,.2f}")
            st.write(f"**Agricultural Income (Exempt up to ₹5,000)**: ₹{agriculture_income:,.2f}")
            st.write(f"**Gross Income**: ₹{gross_income:,.2f}")
            st.write(f"**Standard Deduction**: ₹{std_deduction:,.2f}")
            st.write(f"**Agricultural Exemption**: ₹{agriculture_exemption:,.2f}")
            st.write(f"**Taxable Income**: ₹{taxable_income:,.2f}")
            st.write(f"**Tax Before Rebate**: ₹{tax_result['tax_before_rebate']:,.2f}")
            st.write(f"**Section 87A Rebate**: ₹{tax_result['rebate_87A']:,.2f}")
            st.write(f"**Cess (4%)**: ₹{tax_result['cess']:,.2f}")
            st.write(f"**Total Tax Payable**: ₹{tax_result['total_tax']:,.2f}")

        except Exception as e:
            st.error(f"Calculation error: {str(e)}")

if __name__ == "__main__":
    main()
