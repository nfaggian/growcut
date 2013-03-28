""" growcut package configuration """

import numpy
from setuptools import setup, Extension
from Cython.Distutils import build_ext

setup(
    name='growcut',
    version='0.1',
    description='GrowCut - A cellular automata image segmentation.',
    author='Nathan Faggian',
    author_email='nathan.faggian@gmail.com',
    packages=['growcut'],
    cmdclass={'build_ext': build_ext},
    ext_modules=[
        Extension("growcut.growcut_cy", ["growcut/_growcut_cy.pyx"]),
        Extension("growcut.automate_cy", ["growcut/_automate_cy.pyx"])],
    include_dirs=[numpy.get_include(), ],
    install_requires=[
        'matplotlib',
        'cython'
        'numpy'])
