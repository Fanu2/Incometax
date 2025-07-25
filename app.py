import argparse

def calculate_tax_new_regime(taxable_income):
    # New Regime slabs (FY 2025–26)
    slabs = [
        (0, 300000, 0.0),
        (300000, 600000, 0.05),
        (600000, 900000, 0.10),
        (900000, 1200000, 0.15),
        (1200000, 1500000, 0.20),
        (1500000, float('inf'), 0.30),
    ]

    tax = 0
    for lower, upper, rate in slabs:
        if taxable_income > lower:
            taxable_amount = min(taxable_income, upper) - lower
            tax += taxable_amount * rate
        else:
            break

    # Rebate under section 87A
    if taxable_income <= 1200000:
        rebate = min(tax, 60000)
        tax -= rebate

    return max(0, round(tax))

def main():
    parser = argparse.ArgumentParser(description="Income Tax Calculator for Indian Senior Citizens (FY 2025–26, New Regime)")
    parser.add_argument('--salary', type=float, required=True, help='Annual Salary Income')
    parser.add_argument('--interest', type=float, default=0, help='Interest Income')
    parser.add_argument('--capital_gains', type=float, default=0, help='Capital Gains (taxed separately, excluded here)')
    parser.add_argument('--mutual_funds', type=float, default=0, help='Mutual Funds Income (include only if not taxed separately)')
    parser.add_argument('--other_income', type=float, default=0, help='Other Income (e.g. rent, pension)')
    parser.add_argument('--agriculture_income', type=float, default=0, help='Agricultural Income (exempt)')

    args = parser.parse_args()

    gross_income = args.salary + args.interest + args.mutual_funds + args.other_income
    std_deduction = 75000
    taxable_income = max(0, gross_income - std_deduction)

    tax_payable = calculate_tax_new_regime(taxable_income)

    print("\n=== Income Tax Calculation (FY 2025–26) ===")
    print(f"Salary Income: ₹{args.salary:,.2f}")
    print(f"Interest Income: ₹{args.interest:,.2f}")
    print(f"Mutual Fund Income: ₹{args.mutual_funds:,.2f}")
    print(f"Other Income: ₹{args.other_income:,.2f}")
    print(f"Agricultural Income (Exempt): ₹{args.agriculture_income:,.2f}")
    print(f"Gross Income: ₹{gross_income:,.2f}")
    print(f"Standard Deduction: ₹{std_deduction:,.2f}")
    print(f"Taxable Income: ₹{taxable_income:,.2f}")
    print(f"Income Tax Payable (New Regime): ₹{tax_payable:,.2f}")

if __name__ == '__main__':
    main()
