from distutils.core import setup
from Cython.Build import cythonize

setup(
    name="Kepler vs Dynamical",
    author="Luca Malavolta",
    ext_modules = cythonize("./routines/*.pyx")
    language_level="3"
)
