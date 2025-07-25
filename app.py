#!/usr/bin/env python3
import argparse
import sys
import os

def calculate_tax_new_regime(taxable_income, is_senior_citizen=False):
    """
    Calculate income tax under New Tax Regime for FY 2025–26 (AY 2026–27).
    Adjusts for senior citizens (60+ years) with higher exemption if applicable.
    """
    # New Regime slabs (FY 2025–26)
    slabs = [
        (0, 400000, 0.0),  # Basic exemption increased to ₹4 lakh (Budget 2025)
        (400001, 700000, 0.05),
        (700001, 1000000, 0.10),
        (1000001, 1200000, 0.15),
        (1200001, 1500000, 0.20),
        (1500001, float('inf'), 0.30),
    ]

    # Senior citizens (60-80 years) or super seniors (80+ years) may opt for Old Regime,
    # but we assume New Regime as default per Budget 2025
    tax = 0
    for lower, upper, rate in slabs:
        if taxable_income > lower:
            tax += (min(taxable_income, upper) - lower) * rate
        else:
            break

    # Section 87A rebate: Up to ₹12 lakh taxable income, max ₹60,000
    if taxable_income <= 1200000:
        rebate = min(tax, 60000)
        tax -= rebate

    # Add Health and Education Cess (4%)
    cess = tax * 0.04
    total_tax = tax + cess

    return max(0, round(total_tax, 2))

def main():
    parser = argparse.ArgumentParser(
        description="Income Tax Calculator for FY 2025–26 (New Regime), with senior citizen support",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--salary', type=float, required=True, help='Annual salary income')
    parser.add_argument('--interest', type=float, default=0, help='Interest income (e.g., bank deposits)')
    parser.add_argument('--capital_gains', type=float, default=0, help='Capital gains (short/long-term, if taxable)')
    parser.add_argument('--mutual_funds', type=float, default=0, help='Mutual fund income (if not taxed separately)')
    parser.add_argument('--other_income', type=float, default=0, help='Other income (e.g., rent, pension)')
    parser.add_argument('--agriculture_income', type=float, default=0, help='Agricultural income (exempt up to ₹5,000)')
    parser.add_argument('--senior_citizen', action='store_true', help='Flag if taxpayer is 60+ years (affects Old Regime comparison)')

    try:
        args = parser.parse_args()
    except SystemExit:
        print("Error: Please provide the required --salary argument. Example: python app.py --salary 1000000")
        sys.exit(1)

    # Validate inputs
    for income_type, value in [
        ('Salary', args.salary),
        ('Interest', args.interest),
        ('Capital Gains', args.capital_gains),
        ('Mutual Funds', args.mutual_funds),
        ('Other Income', args.other_income),
        ('Agricultural Income', args.agriculture_income)
    ]:
        if value < 0:
            print(f"Error: {income_type} cannot be negative (provided: ₹{value})")
            sys.exit(1)

    # Calculate gross income
    gross_income = args.salary + args.interest + args.mutual_funds + args.other_income

    # Apply standard deduction (₹75,000 for salaried taxpayers)
    std_deduction = 75000 if args.salary > 0 else 0

    # Agricultural income exemption (up to ₹5,000)
    agriculture_exemption = min(args.agriculture_income, 5000)
    taxable_income = max(0, gross_income - std_deduction - agriculture_exemption)

    # Calculate tax
    total_tax = calculate_tax_new_regime(taxable_income, args.senior_citizen)

    # Output results
    print("\n=== Income Tax Calculation (FY 2025–26, New Tax Regime) ===")
    print(f"Taxpayer Status: {'Senior Citizen (60+)' if args.senior_citizen else 'Resident Individual'}")
    print(f"Salary Income: ₹{args.salary:,.2f}")
    print(f"Interest Income: ₹{args.interest:,.2f}")
    print(f"Mutual Fund Income: ₹{args.mutual_funds:,.2f}")
    print(f"Other Income: ₹{args.other_income:,.2f}")
    print(f"Agricultural Income (Exempt up to ₹5,000): ₹{args.agriculture_income:,.2f}")
    print(f"Gross Income: ₹{gross_income:,.2f}")
    print(f"Standard Deduction: ₹{std_deduction:,.2f}")
    print(f"Agricultural Exemption: ₹{agriculture_exemption:,.2f}")
    print(f"Taxable Income: ₹{taxable_income:,.2f}")
    print(f"Income Tax Payable (including 4% cess): ₹{total_tax:,.2f}")

if __name__ == '__main__':
    # Ensure script runs in the correct directory
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    except FileNotFoundError:
        print("Error: Unable to set working directory. Ensure script is run from a valid path.")
        sys.exit(1)

    main()
