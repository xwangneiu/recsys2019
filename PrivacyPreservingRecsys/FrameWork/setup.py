# cython: language_level=3
from distutils.core import setup
from Cython.Build import cythonize

setup(name = 'myAlgo', ext_modules = cythonize("myAlgorithm.pyx"))
