# Indian Income Tax Calculator (FY 2025–26) - New Tax Regime

This is a **CLI-based income tax calculator** for Indian individual senior citizens under the **New Tax Regime** for the financial year 2025–26 (Assessment Year 2026–27).

---

## Features

- Calculates tax based on updated tax slabs and rebate limits announced in Union Budget 2025
- Applies standard deduction of ₹75,000 for salaried individuals
- Applies Section 87A rebate of up to ₹60,000 for taxable income up to ₹12,00,000
- Handles income types: salary, interest, mutual funds, other income, and exempt agricultural income
- Simple command-line interface using Python standard library (`argparse`)

---

## Usage

```bash
python income_tax_calculator.py --salary 950000 --interest 50000 --mutual_funds 20000 --other_income 30000 --agriculture_income 150000
