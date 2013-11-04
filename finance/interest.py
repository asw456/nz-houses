import numpy as np
import pandas as pd
import sys
import os
import struct
import random



class InterestRate():
	
	max_periods 	= 30*12
	rate_start  	= 0.068
	fixed_period 	= 4*12	
	flat_rate 		= 10.0
	
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


	def get_max_interest_rate():
		
		return np.max(self.interest_rate_array)
			
		
