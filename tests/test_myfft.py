import numpy as np

def test_import():
    import myfftpy
    import numpy

def test_power_of_two():
    from myfftpy.myfftpy import is_power_of_two
    assert is_power_of_two(1)
    assert not is_power_of_two(3)

def test_convert_input_to_complex():
    from myfftpy.myfftpy import convert_input_to_complex
    ex1 = "2 + 3j, 4 - 1j, -1.5 + 2j, 0.5 - 0.5j"
    ex2 = '1,2,3,2.4,123,1.4'
    test1 = convert_input_to_complex(ex1)
    test2 = convert_input_to_complex(ex2)
    all_complex = lambda lst: all(isinstance(x, complex) for x in lst)
    assert all_complex(test1)
    assert all_complex(test2)

def test_ditfft2():
    from myfftpy.myfftpy import ditfft2

    tolerance = 0.01

    fs = 128
    t = np.arange(0,1,1/fs)
    signal = np.sin( 2*np.pi*t)

    np_fft = np.fft.fft(signal)
    my_fft = ditfft2(signal)

    abs_diff = np.abs(np_fft-my_fft)
    assert all( abs_diff < tolerance )


def test_myfftpy_inverse():
    from myfftpy.myfftpy import myfftpy
    tolerance = 0.01
    fs = 128
    t = np.arange(0,1,1/fs)
    signal = np.sin( 2*np.pi*t)

    my_fft_inv = myfftpy(myfftpy(signal), True)
    np_inv = np.fft.ifft(np.fft.fft(signal))

    abs_diff = np.abs(my_fft_inv) - np.abs(signal)
    np_diff = np.abs(np_inv) - np.abs(my_fft_inv)

    assert all( abs_diff < tolerance)
    assert all( np_diff < tolerance)
