# -*- coding: utf-8 -*-
"""
MortgageCalculator
"""


class MortgageCalculator():
    
    P = 0;
    i = 0;
    N = 0;
    
    def __init__(self, P, i, N):
        self.P = P
        self.i = i / 12.0
        self.N = N
        
    def calculate(self, P, i, N):
        
        return P * ( i / (1 - (1 + i) ** (- N)))