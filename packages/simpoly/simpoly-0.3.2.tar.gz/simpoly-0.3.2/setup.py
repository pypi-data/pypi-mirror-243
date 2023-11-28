from os import path
from distutils.core import setup
from Cython.Build import cythonize

setup(
    include_package_data=False,
    setup_requires=["cython"],
    ext_modules=cythonize(["*/*.pyx"]),
)
