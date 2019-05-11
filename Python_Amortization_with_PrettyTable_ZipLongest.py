from itertools import zip_longest
#INPUT DEAL NAME
name = input('Enter Deal Name:')

# INPUT LOAN AMOUNT
loan_amount = int(input('Enter 1st Loan Amount:'))

# INPUT INTEREST RATE
rate = float(input('Enter 1st Rate: '))/100
mo_rate = rate/12

# INPUT TERM IN MONTHS
term = int(input('Enter  1st Term Months:'))
term_periods = [x for x in range(1,term+1)]

# INPUT AMORT IN MONTHS
amort = int(input('Enter 1st Amortization Months:'))
amort_periods = [y for y in range(1,amort+1)]

# CREATE AMORTIZATION VARIABLES
current_balance = loan_amount
mo_payment = loan_amount*(mo_rate*(1+mo_rate)**amort/(((1+mo_rate)**amort)-1))

# MAKE AMORTIZATION TABLE
amort_table = [('Period','Current Balance','Monthly Payment','Principal','Interest','Remaining Balance')]
for i in term_periods:
  beg_balance = current_balance
  int_paid = current_balance*mo_rate
  principal = mo_payment-int_paid
  current_balance = current_balance - principal
  amort_table.append((i, int(beg_balance), int(mo_payment), int(principal),int(int_paid), int(current_balance)))

# -------------------------------------------------------------------------------------
# 2ND LOAN

# INPUT LOAN AMOUNT
loan_amount2 = int(input('Enter 2nd Loan Amount:'))

# INPUT INTEREST RATE
rate2 = float(input('Enter 2nd Rate: '))/100
mo_rate2 = rate2/12

# INPUT TERM IN MONTHS
term2 = int(input('Enter 2nd Term Months:'))
term_periods2 = [x for x in range(1,term2+1)]

# INPUT AMORT IN MONTHS
amort2 = int(input('Enter 2nd Amortization Months:'))
amort_periods2 = [y for y in range(1,amort2+1)]

# CREATE AMORTIZATION VARIABLES
current_balance2 = loan_amount2
mo_payment2 = loan_amount2*(mo_rate2*(1+mo_rate2)**amort2/(((1+mo_rate2)**amort2)-1))

# MAKE AMORTIZATION TABLE
amort_table2 = [('Period','Current Balance','Monthly Payment','Principal','Interest','Remaining Balance')]
for i in term_periods2:
  beg_balance2 = current_balance2
  int_paid2 = current_balance2*mo_rate2
  principal2 = mo_payment2-int_paid2
  current_balance2 = current_balance2 - principal2
  amort_table2.append((i, int(beg_balance2), int(mo_payment2), int(principal2),int(int_paid2), int(current_balance2)))

# -------------------------------------------------------------------------------------
# COMBINE TWO LOANS INTO AMORTIZATION TABLE (NEED ITERTOOLS(ZIP_LONGEST) TO GO LONGER THAN SHORTEST LOAN)
total_financing = loan_amount + loan_amount2
total_mo_payment = mo_payment + mo_payment2
amort_table3 = [('Period','Current Balance','Monthly Payment','Principal','Interest', 'Remaining Balance', 'Blended Rate')]
# Used to avoid NoneType is not subscriptable error resulting from zip_longest
zero_list = [0,0,0,0,0,0,0]
for x,y in zip_longest(amort_table[1:],amort_table2[1:]):
  if x == None:
    x = zero_list
  if y == None:
    y = zero_list
  beg_balance3 = x[1] + y[1]
  mo_payment3 = x[2] + y[2]
  principal3 = x[3] + y[3]
  int_paid3 = x[4] + y[4]
  current_balance3 = x[5] + y[5]
  blended_rate = ((rate*(x[1]/beg_balance3)) + (rate2*(y[1]/beg_balance3)))*100
  amort_table3.append((y[0], '{:,}'.format(beg_balance3), '{:,}'.format(mo_payment3), '{:,}'.format(principal3), '{:,}'.format(int_paid3), '{:,}'.format(current_balance3), '{:.4f}%'.format(blended_rate)))

blended_rate = amort_table3[1][6]

# -------------------------------------------------------------------------------------
# PRINT OUT LOAN SUMMARY
# print('1st Loan Amount: ${:,}'.format(loan_amount))
# print('1st Interest Rate: {:.2f}%'.format(rate*100))
# print('Monthly Payment: ${:,.0f}'.format(mo_payment))
# print('1st Loan Term: {} months'.format(term))
# print('1st Amortization: {} months'.format(amort))

# print('')

# print('2nd Loan Amount: ${:,}'.format(loan_amount2))
# print('2nd Interest Rate: {:.2f}%'.format(rate2*100))
# print('Monthly Payment: ${:,.0f}'.format(mo_payment2))
# print('2nd Loan Term: {} months'.format(term2))
# print('2nd Amortization: {} months'.format(amort2))

print('')

print('Total Financing: ${:,}'.format(total_financing))
print('Blended Rate: {}'.format(blended_rate))
print('Total Monthly Payment: {:,.0f}'.format(total_mo_payment))

print('')

# for x in amort_table: print(x)

# for x in amort_table2: print(x)

# for x in amort_table3: print(x)
#----------------------------------------------------------------------------------------------------------------------------------
# PRETTY TABLE
from prettytable import PrettyTable

new_table = PrettyTable(amort_table3[0])

for x in range(1,len(amort_table3)):
    new_table.add_row(amort_table3[x])

print(new_table)




# ----------------------------------------------------------------------------------------------------------------------------------------------------
# TO DO
# 1) Make it work when length of the 1st term is longer than the 2nd's term
# 2) Format input (So it shows a % when you input rate or comma's when you enter the loan amounts)
# 3) Output the amortization table in an excel or csv file

# -------------------------------------------------------------------------------------------------------------------------------

#OUTPUT TO CSV
import csv

#myFile = open(r"C:\Users\PC\PycharmProjects\AmortizationTable\", 'wb')
with open("C:/Users/PC/PycharmProjects/AmortizationTable/{}.csv".format(name), 'w') as f:
	writer = csv.writer(f)
	writer.writerows(amort_table3)

print('Outputted to csv file')
















