"""
It is a custom implementation of the radix-2 DIT Fast Fourier Transform (FFT) algorithm.

It will accept 1D signals as an array of real or complex numbers
and outputs fft results as a 1D array of complex numbers.
"""
#!usr/bin/env python
import cmath
import logging
import argparse
import matplotlib.pyplot as plt
import numpy as np

#TODO: pad the input data array with zeros increase the sample size

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
    flag2 = is_power_of_two(len(input))
    logging.info(f"size of the array: power of two? {flag2}")
    return flag1 and flag2


def ditfft2(input:list, inverse=False):
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
    evens = ditfft2(input[::2],inverse)
    odds = ditfft2(input[1::2],inverse)
    
    factor = cmath.exp( 2j * cmath.pi / size) if inverse \
        else cmath.exp( -2j * cmath.pi / size) 

    result = [0] * size
    for k in range(size // 2):
        even = evens[k]
        odd = factor**k * odds[k]
        result[k] = even + odd
        result[k + size // 2] = even - odd

    return result

def myfftpy(input:list, inverse=False):
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
    
    result = ditfft2(input)
    if inverse:
        size = len(result)
        result = [r/size for r in result]
    return result

def is_power_of_two(size:int):
    """
    Check if the given size is power of two

    Parameters
    ----------
    size: int
        size of an array
    
    Returns
    ----------
    Boolean
        True if the param is power of two
    """
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

def convert_input_to_complex(input_str:str) -> list:
    """
    Convert a string of complex numbers to a list of complex numbers

    Parameters
    ----------
    input_str: str
        a string of comma-separated complex numbers or floats
    
    Returns
    --------
    parsed_input: list
        a list of complex numbers
    """
    input_list = input_str.split(',')
    input_stripped = [i.replace(' ','') for i in input_list]
    parsed_input = [complex(i) for i in input_stripped]
    return parsed_input

def save_to_file(output, filename=None):
    """
    Writes the result to a given filepath
    """
    if filename is None:
        filename= 'myfftpy/result_data/fft_results.csv'
    log.info(f'current storage path: {filename}')
    with open(filename, 'w') as f:
        for out in output:
            print(f"{out.real}+{out.imag}j,", file=f)
    log.info(f'stored the output to {filename}')

def plot_output(output):
    fig, ax = plt.subplots()
    x = np.arange(len(output))
    output = np.array(output)
    real = output.real
    imag = output.imag

    ax.plot(x, real, label="real")
    ax.plot(x, imag, '--',label="imaginary")

    ax.set_xlabel("freq")
    ax.set_ylabel("amplitude")
    ax.legend()

    return fig

def save_fig(fig, filepath):
    fig.savefig(filepath)
    plt.close(fig)

def main():
    parser = myfftpy_parser()
    options = parser.parse_args()

    try:
        input = convert_input_to_complex(options.input)
    except ValueError as e:
        log.error(e)
        log.critical("Could not handle input argument")

    assert input is not None and check_input_type_and_size(input)
    logging.info("Input is the correct type")

    output = myfftpy(input)
    save_to_file(output, None)

    fig = plot_output(output)
    save_fig(fig, 'myfftpy/result_data/fft_results.png')

if __name__=='__main__':
    main()
