"""
It is a custom implementation of the radix-2 DIT Fast Fourier Transform (FFT) algorithm.

It will accept 1D signals as an array of real or complex numbers
and outputs fft results as a 1D array of complex numbers.
"""
#!usr/bin/env python
import cmath
import logging
import argparse

logging.basicConfig(format="%(name)s:%(levelname)s %(message)s", level=logging.INFO)
log = logging.getLogger(__name__)

def check_input_type_and_size(input:list):
    """
    Checks if the input is a 1-D array of complex numbers of size 2**n

    Params
    ----------
    input: list of complex numbers

    Returns
    ----------
    True if the input is a 1-D array of complex numbers of size 2**
    False otherwise
    """
    #TODO: flexible input size?
    #first flag: all item instances are either complex or float numbers
    flag1 = all(isinstance(i, (int, float, complex)) for i in input)
    logging.info(f"Each item in input should be numeric: {flag1}")
    #second flag: the size of the array is power of two, for best performance
    flag2 = power_of_two(len(input))
    logging.info(f"size of the array: power of two? {flag2}")
    return flag1 and flag2


def ditfft2(input:list):
    """
    computes 1-D Cooley Tukey FFT

    Params
    ---------- 
    input: list
        1-D array of complex numbers

    Returns
    ----------
    result: list
        FFT result of the input as a 1-D array of complex number
    """
    size = len(input)
    if size== 1:
        return [input[0]]
    evens = ditfft2(input[::2])
    odds = ditfft2(input[1::2])
    
    result = [0] * size
    for k in range(size // 2):
        even = evens[k]
        odd = cmath.exp( -2j * cmath.pi * k / size) * odds[k]
        result[k] = even + odd
        result[k + size // 2] = even - odd
    return result

def myfftpy(input:list):
    """
    Performs FFT on the input array

    Params
    ---------- 
    input: list
        1-D array of size 2^n 

    Returns
    ----------
    result: list
        FFT result of the input as a 1-D array of complex number

    """
    assert check_input_type_and_size(input)
    input = to_complex(input)
    logging.info("Input type and size are correct")
    return ditfft2(input)

def to_complex(input:list):
    return [complex(x) for x in input]


def power_of_two(size:int):
    return size & (size - 1) == 0 and size > 0

def myfftpy_parser():
    """
    Configure the argparse for myfftpy

    Returns
    --------
    parser: argparse.ArgumentParser
        The parser
    """
    parser = argparse.ArgumentParser(prog='myfftpy',
                                     prefix_chars='-')
    parser.add_argument('--input', 
                        dest='input',
                        type=str,
                        default=None,
                        help="Input array should be a comma-separated array of numeric elements of size 2^n, where n in a positive integer"
                        )
    return parser

def parse_input(input_str:str):
    parsed_input = [float(i) for i in input_str.split(',')]
    return parsed_input

def save_to_file(output, filename=None):
    if filename is None:
        filename= 'myfftpy/result_data/fft_results.csv'
    log.info(f'current storage path: {filename}')
    with open(filename, 'w') as f:
        for out in output:
            print(f"{out.real} + {out.imag}j", file=f)
    log.info(f'stored the output to {filename}')


def main():
    parser = myfftpy_parser()
    options = parser.parse_args()
    input = parse_input(options.input)
    assert input is not None
    output = myfftpy(input)
    save_to_file(output, None)

if __name__=='__main__':
    main()
