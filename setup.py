""" growcut package configuration """

from setuptools import setup

setup(
    name='growcut',
    version='0.1',
    description='GrowCut - A cellular automata image segmentation.',
    author='Nathan Faggian',
    author_email='nathan.faggian@gmail.com',
    packages=['growcut'],
    install_requires=[
       'matplotlib',
       'numpy',
       ]
    )
