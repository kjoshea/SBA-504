import os
import pandas as pd
from itertools import zip_longest
from prettytable import PrettyTable

# INPUT DEAL NAME
deal_name = input('Enter Deal Name:')

# ---------------------------------------------------------------------------------------------------------------------

# 1st LOAN

# INPUT 1st LOAN DETAILS
loan_amount = int(input('Enter 1st Loan Amount:'))
rate = float(input('Enter 1st Rate: ')) / 100
term = int(input('Enter 1st Term Months:'))
amort = int(input('Enter 1st Amortization Months:'))

# CREATE AMORTIZATION TABLE VARIABLES
mo_rate = rate / 12
term_periods = [x for x in range(1, term + 1)]
current_balance = loan_amount
mo_payment = loan_amount * (mo_rate * (1 + mo_rate) ** amort / (((1 + mo_rate) ** amort) - 1))

# CREATE AMORTIZATION TABLE
amort_table = [('Period', 'Current Balance', 'Monthly Payment', 'Principal', 'Interest', 'Remaining Balance')]
for i in term_periods:
    beg_balance = current_balance
    int_paid = current_balance * mo_rate
    principal = mo_payment - int_paid
    current_balance = current_balance - principal
    amort_table.append((i, int(beg_balance), int(mo_payment), int(principal), int(int_paid), int(current_balance)))

# ---------------------------------------------------------------------------------------------------------------------

# 2nd LOAN

# INPUT 2nd LOAN DETAILS
loan_amount2 = int(input('Enter 2nd Loan Amount:'))
rate2 = float(input('Enter 2nd Rate: ')) / 100
term2 = int(input('Enter 2nd Term Months:'))
amort2 = int(input('Enter 2nd Amortization Months:'))

# CREATE AMORTIZATION TABLE VARIABLES
mo_rate2 = rate2 / 12
term_periods2 = [x for x in range(1, term2 + 1)]
current_balance2 = loan_amount2
mo_payment2 = loan_amount2 * (mo_rate2 * (1 + mo_rate2) ** amort2 / (((1 + mo_rate2) ** amort2) - 1))

# CREATE AMORTIZATION TABLE
amort_table2 = [('Period', 'Current Balance', 'Monthly Payment', 'Principal', 'Interest', 'Remaining Balance')]
for i in term_periods2:
    beg_balance2 = current_balance2
    int_paid2 = current_balance2 * mo_rate2
    principal2 = mo_payment2 - int_paid2
    current_balance2 = current_balance2 - principal2
    amort_table2.append(
        (i, int(beg_balance2), int(mo_payment2), int(principal2), int(int_paid2), int(current_balance2)))

# ---------------------------------------------------------------------------------------------------------------------

# COMBINE TWO LOANS INTO AMORTIZATION TABLE (NEED ITERTOOLS(ZIP_LONGEST) TO GO LONGER THAN SHORTEST LOAN)
total_financing = loan_amount + loan_amount2
total_mo_payment = mo_payment + mo_payment2
amort_table3 = [
    ('Period', 'Current Balance', 'Monthly Payment', 'Principal', 'Interest', 'Remaining Balance', 'Blended Rate')]

# Used to avoid NoneType is not subscriptable error resulting from zip_longest
zero_list = [0, 0, 0, 0, 0, 0, 0]
for x, y in zip_longest(amort_table[1:], amort_table2[1:]):
    if x is None:
        x = zero_list
    if y is None:
        y = zero_list
    beg_balance3 = x[1] + y[1]
    mo_payment3 = x[2] + y[2]
    principal3 = x[3] + y[3]
    int_paid3 = x[4] + y[4]
    current_balance3 = x[5] + y[5]
    blended_rate = ((rate * (x[1] / beg_balance3)) + (rate2 * (y[1] / beg_balance3))) * 100
    amort_table3.append((y[0], '{:,}'.format(beg_balance3), '{:,}'.format(mo_payment3), '{:,}'.format(principal3),
                         '{:,}'.format(int_paid3), '{:,}'.format(current_balance3), '{:.2f}%'.format(blended_rate)))

blended_rate = amort_table3[1][6]

# ---------------------------------------------------------------------------------------------------------------------

# ORGANIZE LOAN SUMMARY INTO LIST OF LISTS AND TWO SEPARATE LISTS FOR FIELDS AND VALUES
loan_summary = [['Deal Name', '{}'.format(deal_name)], ['1st Loan Amount', '${:,}'.format(loan_amount)],
                ['1st Interest Rate', '{:.2f}%'.format(rate * 100)],
                ['1st Monthly Payment', '${:,.0f}'.format(mo_payment)],
                ['1st Loan Term', '{} months'.format(term)], ['1st Loan Amortization', '{} months'.format(amort)],
                ['', ''], ['2nd Loan Amount', '${:,}'.format(loan_amount2)],
                ['2nd Interest Rate', '{:.2f}%'.format(rate2 * 100)],
                ['2nd Monthly Payment', '${:,.0f}'.format(mo_payment2)], ['2nd Loan Term', '{} months'.format(term2)],
                ['2nd Loan Amortization', '{} months'.format(amort2)], ['', ''],
                ['Total Financing', '${:,}'.format(total_financing)],
                ['Blended Rate', '{}'.format(blended_rate)],
                ['Total Monthly Payment', '${:,.0f}'.format(total_mo_payment)]]
loan_summary_fields = [_[0] for _ in loan_summary]
loan_summary_values = [_[1] for _ in loan_summary]

print('')
print('Total Financing: ${:,}'.format(total_financing))
print('Blended Rate: {}'.format(blended_rate))
print('Total Monthly Payment: ${:,.0f}'.format(total_mo_payment))
print('')

# ---------------------------------------------------------------------------------------------------------------------

# CONVERT AMORTIZATION TABLE TO PRETTY TABLE AND PRINT TO COMMAND LINE
new_table = PrettyTable(amort_table3[0])

for x in range(1, len(amort_table3)):
    new_table.add_row(amort_table3[x])

print(new_table)

# ---------------------------------------------------------------------------------------------------------------------

# CONVERT AMORTIZATION TABLE TO A PANDA DATAFRAME
df = pd.DataFrame(amort_table3)

# RETRIEVE EXCEL FILE OUTPUT PATH FROM ENVIRONMENT VARIABLE
output_path = os.environ['AMORTIZATION_OUTPUT']

# CREATE EXCEL FILE AND NAME 1st WORKSHEET
writer = pd.ExcelWriter(f"{output_path}/{deal_name}.xlsx", engine='xlsxwriter')
df.to_excel(writer, sheet_name='Amortization')

# ADD WORKSHEET WITH THE LOAN SUMMARY PRINTED IN THE TOP LEFT AS TWO COLUMNS
workbook = writer.book
worksheet_2 = workbook.add_worksheet('Deal Info')
worksheet_2.write_column('A1', loan_summary_fields)
worksheet_2.write_column('B1', loan_summary_values)

writer.save()

# ---------------------------------------------------------------------------------------------------------------------
# TO DO
# 1) Make it work when length of the 1st term is longer than the 2nd's term
# 2) Format input (So it shows a % when you input rate or comma's when you enter the loan amounts)
# 3) Add additional tabs of loan information
# ---------------------------------------------------------------------------------------------------------------------
