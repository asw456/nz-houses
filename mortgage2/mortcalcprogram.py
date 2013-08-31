#!/usr/bin/env python
"""
script
"""

import MortgageCalculator as mortcalc

print "Please enter the principal amount"
user_principal = raw_input(">")
principal = float(user_principal)

print "Please enter the interest rate"
user_interest = raw_input(">")
interest = float(user_interest) / 12

print "Please enter the term in years"
user_term = raw_input(">")
term = float(user_term) * 12

initalize = mortcalc.MortgageCalculator(principal, interest, term)

result = mortcalc.MortgageCalculator.calculate(initalize, principal, interest, term)

print '${0:.2f}'.format(result)

print "Would you like to see the amortization?  Please press 'y' to continue:"
user_amort = raw_input(">")

if user_amort == 'y':
    print "Ok"
    
    monthly_payment = result
    remaining_balance = principal
    interest_paid = remaining_balance * interest 
    principal_paid = monthly_payment - interest_paid
    
    remaining_balance = remaining_balance - principal_paid
    
    print "Month      Interest       Principal     Balance"
    for i in range(0, int(term), 1):
        print i + 1, '${0:.2f}'.format(interest_paid), '${0:.2f}'.format(principal_paid), '${0:.2f}'.format(remaining_balance)
        interest_paid = remaining_balance * interest
        principal_paid = monthly_payment - interest_paid
        remaining_balance = remaining_balance - principal_paid
else: 
    print "Goodbye"
