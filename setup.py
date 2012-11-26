""" growcut package configuration """

import numpy
from setuptools import setup

from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    name='growcut',
    version='0.1',
    description='GrowCut - A cellular automata image segmentation.',
    author='Nathan Faggian',
    author_email='nathan.faggian@gmail.com',
    packages=['growcut'],
    cmdclass={
            'build_ext': build_ext
        },
    #ext_modules=[Extension("growcut.extension", ["growcut/extension.pyx"], )],
    #include_dirs=[numpy.get_include(), ],
    install_requires=[
       'matplotlib',
       'numpy,
       'scipy',
       'cython',
       ]
    )
