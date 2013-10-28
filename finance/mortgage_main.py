#!usr/bin/env python

import numpy as np
import pandas
import sys
import os
import struct
import random
#import scikit-learn as skl
import matplotlib.pyplot as pyplot


class RentalIncome():
	
	def __init__(self):
		self.weekly_rent = 400
		self.monthly_rent = self.weekly_rent*4.34812
		
		self.weekly_flat = 100
		self.flatmates = 1
		self.unoccupied_weeks = 8
		self.monthly_flat = self.weekly_flat*self.flatmates*4.34812*((52.0-self.unoccupied_weeks)/52)
		
	def get_monthly_rental_income(self):
		return self.monthly_rent
		
	def get_monthly_flat_income(self):
		return self.monthly_flat
		
class HouseExpenses():
	
	def __init__(self):
		self.yearly_rates = 2000
		self.monthly_rates = self.yearly_rates/12.0
		
		self.yearly_maintenance = 2000
		self.monthly_maintenance = self.yearly_maintenance/12.0
		
		self.monthly_expenses_total = self.monthly_rates + self.monthly_maintenance
		
	def get_monthly_expenses(self):
		return self.monthly_expenses_total
	
class SalaryIncome():

	def __init__(self):
		self.yearly_gross_income = 75000
		self.yearly_tax = 14000*0.105 + (48000-14000)*0.175 + (70000-48000)*0.30 + (self.yearly_gross_income-70000)*0.33
		
		self.yearly_income = self.yearly_gross_income - self.yearly_tax
		self.monthly_income = self.yearly_income/12.0
		
		self.monthly_payment = self.monthly_income / 2.0
			
	def get_monthly_salary_payment(self):
		return self.monthly_payment

class CapitalGains():
	
	max_periods = 30*12
	price_start  = 0.0515	
	
	price_array = np.zeros((max_periods),dtype=np.float64)
	multiplier = 1.0
	
	def __init__(self):
		self.random_walk_probabilities = np.loadtxt('/Users/james/development/code_personal/nz-houses/data/math/capital_gains_walk_probabilities.txt',dtype=np.float64)
		self.populate_price_array()	
	
	def populate_price_array(self):
		
		a = random.Random()
		b = random.Random()
		
		price = self.price_start
		
		for i in range(0,self.max_periods):
			#if (i % 6) == 0:
			
			ra = a.random()
			for j in range(0,self.random_walk_probabilities.shape[0]):
				if ra <= self.random_walk_probabilities[j,3]:
					price_increase = self.random_walk_probabilities[j,0]*0.01
					break
			
			rb = b.random()
			if rb < 0.35:
				price_increase = -1.0*price_increase
			
			price = price + self.multiplier*price_increase
			self.price_array[i] = price
			
		np.savetxt('/Users/james/development/code_personal/nz-houses/data/math/capital_gains_array.txt',self.price_array)
		
		print 'maximum price = ' + str(max(self.price_array))
			
	def get_interest_price_array(self):
		return self.price_array
		
	def plot_price_array(self):
		pyplot.plot(self.price_array)
		pyplot.show()

class InterestRate():
	
	max_periods 	= 30*12
	rate_start  	= 0.068
	fixed_period 	= 4*12	
	
	rate_array = rate_start*np.ones((max_periods),dtype=np.float64)
	
	def __init__(self):
		self.random_walk_probabilities = np.loadtxt('/Users/james/development/code_personal/nz-houses/data/math/interest_rate_walk_probabilities.txt',dtype=np.float64)
		self.populate_rate_array()	
	
	def populate_rate_array(self):
		
		a = random.Random()
		b = random.Random()
		
		rate = 0.08
		
		for i in range(self.fixed_period,self.max_periods):
			
			# determine a rate increase for this time-step
			for j in range(0,self.random_walk_probabilities.shape[0]):
				if a.random() <= self.random_walk_probabilities[j,3]:
					rate_increase = self.random_walk_probabilities[j,0]*0.01
					break
			
			# determine whether the step is positive or negative
			if b.random() < 0.3:
				rate_increase = -1.0*rate_increase
			
			
			# increment the interest rate and store the result
			rate += rate_increase
			self.rate_array[i] = rate
			
		np.savetxt('/Users/james/development/code_personal/nz-houses/data/math/interest_rate_array.txt',self.rate_array)
		
	def get_interest_rate_array(self):
		
		return self.rate_array/12.0
		
	def plot_rate_array(self):
		pyplot.plot(self.rate_array)
		pyplot.show()




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

def get_max_interest_rate():
	
	max = 0
	for i in range(0,100):	
		interest 			= InterestRate()
		interest_rate_array = interest.get_interest_rate_array()
		if np.max(interest_rate_array) > max:
			max = np.max(interest_rate_array)
		
	print 'maximum rate = ' + str(max)
	return max
	
	
if __name__ == "__main__":
	
	#get_max_interest_rate()
	
	
	simulate()
	
	
	#print str(i) + '\t\t' + str(net_payment_array[i]) #+ str(principal_array[i])
	
	#np.savetxt('/Users/james/development/code_personal/nz-houses/data/math/payment.txt',self.rate_array)
		
		
		
		 
		
		
		
	
	
	
	
	
	
	
	
	
	
	
	
	

