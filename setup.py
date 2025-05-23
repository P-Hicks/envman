from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("env_manager.pyx", compiler_directives={"language_level": "3"})
)