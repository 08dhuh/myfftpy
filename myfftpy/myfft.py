#!usr/bin/env python
"""
It is a custom, inefficient, unnecessary implementation of the radix-2 DIT Fast Fourier Transform (FFT) algorithm.

input: 1D array of complex numbers

output: 
"""
from math import *
#make recursive calls

def check_input_type_and_size(input:list):
    """
    Checks if the input is a 1-D array of complex numbers of size 2**n
    """
    #first flag: all item instances are either complex or float numbers
    flag1 = all(isinstance(i, (int, float, complex)) for i in input)
    #second flag: the size of the array is power of two, for best performance
    flag2 = power_of_two(len(input))
    return flag1 and flag2

def power_of_two(size:int):
    if size // 2 <= 1:
        return size % 2 == 0
    return power_of_two(size/2)