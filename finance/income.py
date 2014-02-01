import numpy as np
import pandas as pd
import sys
import os
import struct
import random


def rental_income():
	
	weekly_rent 		= 350
	monthly_rent 		= weekly_rent*4.34812
	return monthly_rent
	

def flat_income():
		
	weekly_flat 		= 110
	flatmates 			= 2
	unoccupied_weeks 	= 8
	monthly_flat 		= weekly_flat*flatmates*4.34812*((52.0-unoccupied_weeks)/52)
	return monthly_flat

	
def salary_income():

	yearly_gross_income = 75000
	yearly_tax 			= 14000*0.105 + (48000-14000)*0.175 + (70000-48000)*0.30 + (yearly_gross_income-70000)*0.33
		
	yearly_income 		= yearly_gross_income - yearly_tax
	monthly_income 		= yearly_income/12.0
		
	monthly_payment 	= monthly_income / 2.0
			
	return monthly_payment




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
