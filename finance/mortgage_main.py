#!usr/bin/env python

import numpy as np
import pandas as pd
import sys
import os
import struct
import random
import matplotlib.pyplot as pyplot
#import scikit-learn as skl

import expenses
import income
import interest
from ggplot import *

#p + geom_point() + geom_line(color='lightblue') + ggtitle("Beef: It's What's for Dinner") + xlab("Date") + ylab("Head of Cattle Slaughtered")
#p = ggplot(mtcars, aes(x='wt', y='mpg', colour='factor(cyl)', size='mpg', linetype='factor(cyl)'))
#print p + geom_line() + geom_point()




def simulate():

	deposit = 80000.0
	price   = 350000.0
	price   = price - deposit
	
	interest 			= InterestRate()
	interest.plot_rate_array()
	exit()
	interest_rate_array = interest.get_interest_rate_array()
	
	rental_income 	= RentalIncome()
	salary_income 	= SalaryIncome()
	house_expenses 	= HouseExpenses()
	
	#print 'monthly payment = ' + str(salary_income.get_monthly_salary_payment())
	
	max_periods = 30*12
	
	principal_array 		= np.zeros((max_periods),dtype=np.float64)
	interest_payment_array 	= np.zeros((max_periods),dtype=np.float64)
	net_payment_array		= np.zeros((max_periods),dtype=np.float64)
	
	principal_array[0] 			= price
	interest_payment_array[0] 	= 0
	net_payment_array[0]		= 0
	
	for i in range(1,max_periods):
		
		interest_payment_array[i] 	= principal_array[i-1]*interest_rate_array[i]
		
		if i <= 2*12:
			net_payment_array[i] = -interest_payment_array[i] - house_expenses.get_monthly_expenses() \
										+ rental_income.get_monthly_rental_income() \
										+ salary_income.get_monthly_salary_payment()
		else:
			net_payment_array[i] = -interest_payment_array[i] - house_expenses.get_monthly_expenses() \
										+ rental_income.get_monthly_flat_income() \
										+ salary_income.get_monthly_salary_payment()
		
		if net_payment_array[i] <= 0:
			print 'if you have to ask ... you can\'t afford it.'
			print 'underwater at = ' + str(i/12.0) + ' years'
			break
		
		principal_array[i] = principal_array[i-1] - net_payment_array[i]
	
		if principal_array[i] <= 0:
			print 'paid off at = ' + str(i/12.0) + ' years'
			print 'interest paid = ' + str(int(np.sum(interest_payment_array)))
			break

	return


def simulate2(mortgage,period,interest_method):
	
	# principal is at start of month
	# payment is at end of month
	
	columns = ['month','principal','interest','rates','insurance','house_expenses','misc_expenses',
				'income','flat_income','total_payment','principal_payment','income_payment']
	
	df_ 	= pd.DataFrame(index=index, columns=columns)
	
	
	
def monthly_payment_vs_mortgage_chart():
	
	ir 					= interest.InterestRate()
	monthly_interest 	= ir.flat_rate/12.0/100
	
	monthly_interest 	= 8.0/12/100
	principal 			= np.arange(200000,400000,25000,dtype=np.float64)
	monthly_payment 	= np.zeros(principal.shape[0],dtype=np.float64)
	
	for i in range(0,principal.shape[0]):
		monthly_payment[i] 	= principal[i] * monthly_interest/(1-(1+monthly_interest) ** (-20*12))
	
	print principal[0]
	print monthly_payment[0]
	
	#pyplot.plot(principal,monthly_payment)
	#pyplot.show()
	
	df = pd.DataFrame({
    "x": principal,
    "y": monthly_payment,
	})
	

	p = ggplot(df, aes('factor(x)')) + geom_bar()
	plt.show()	

	
	
if __name__ == "__main__":
	
	#get_max_interest_rate()
	
	
	monthly_payment_vs_mortgage_chart()
	
	
	#print str(i) + '\t\t' + str(net_payment_array[i]) #+ str(principal_array[i])
	
	#np.savetxt('/Users/james/development/code_personal/nz-houses/data/math/payment.txt',self.rate_array)
		
		
		
		 
		
		
		
	
	
	
	
	
	
	
	
	
	
	
	
	

