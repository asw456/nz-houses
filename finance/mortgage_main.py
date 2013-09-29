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
		self.flatmates = 3
		self.monthly_flat = self.weekly_flat*self.flatmates*4.34812*((52.0-3)/52)
		
	def get_monthly_rental_income():
		return self.monthly_rent
		
	def get_monthly_flat_income():
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
	
class Income():

	def __init__(self):
		self.yearly_gross_income = 75000
		self.yearly_tax = 14000*0.105 + (48000-14000)*0.175 + (70000-48000)*0.30 + (self.yearly_gross_income-70000)*0.33
		
		self.yearly_income = self.yearly_gross_income - self.yearly_tax
		self.monthly_income = self.yearly_income/12.0
		
		self.monthly_payment = self.monthly_income / 2.0
			
	def get_monthly_payment(self):
		return self.monthly_payment

class CapitalGains():
	
	max_periods = 30*12
	price_start  = 0.0515	
	
	price_array = np.zeros((max_periods,1),dtype=np.float64)
	multiplier = 1.0
	
	def __init__(self):
		self.random_walk_probabilities = np.loadtxt('/Users/james/development/resources/nz-houses/data/math/capital_gains_walk_probabilities.txt',dtype=np.float64)
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
			
		np.savetxt('/Users/james/development/resources/nz-houses/data/math/interest_price_array.txt',self.price_array)
		
		print 'maximum price = ' + str(max(self.price_array))
			
	def get_interest_price_array(self):
		return self.price_array
		
	def plot_price_array(self):
		pyplot.plot(self.price_array)
		pyplot.show()

class InterestRate():
	
	max_periods = 30*12
	rate_start  = 0.0515	
	
	rate_array = np.zeros((max_periods,1),dtype=np.float64)
	multiplier = 1.0
	
	def __init__(self):
		self.random_walk_probabilities = np.loadtxt('/Users/james/development/resources/nz-houses/data/math/interest_rate_walk_probabilities.txt',dtype=np.float64)
		self.populate_rate_array()	
	
	def populate_rate_array(self):
		
		a = random.Random()
		b = random.Random()
		
		rate = self.rate_start
		
		for i in range(0,self.max_periods):
			#if (i % 6) == 0:
			
			ra = a.random()
			for j in range(0,self.random_walk_probabilities.shape[0]):
				if ra <= self.random_walk_probabilities[j,3]:
					rate_increase = self.random_walk_probabilities[j,0]*0.01
					break
			
			rb = b.random()
			if rb < 0.35:
				rate_increase = -1.0*rate_increase
			
			rate = rate + self.multiplier*rate_increase
			self.rate_array[i] = rate
			
		np.savetxt('/Users/james/development/resources/nz-houses/data/math/interest_rate_array.txt',self.rate_array)
		
		print 'maximum rate = ' + str(max(self.rate_array))
			
	def get_interest_rate_array(self):
		return self.rate_array
		
	def plot_rate_array(self):
		pyplot.plot(self.rate_array)
		pyplot.show()



	
	
if __name__ == "__main__":
	
	deposit = 80000.0
	
	
	
	interest = InterestRate()
	rental_income = RentalIncome()
	income = Income()
	house_expenses = HouseExpenses()
	
	print income.get_monthly_payment()
	
	
	
	
	
	
	
	
	
	
	
	
	
	

