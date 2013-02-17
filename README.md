Grow-Cut Image Segmentation
==========================

The "growcut" package implements celular automata based segmentation algorithm.

References:
-----------

    V. Vezhnevets, V. Konouchine. "Grow-Cut" - Interactive Multi-Label N-D Image Segmentation". 
    In Proceedings of the 2005 Conference, Graphicon. Pages 150 – 156.


Maintainers
-----------

   - Nathan Faggian
   - Ed Schofield

Testing
-------

[![Build Status](https://travis-ci.org/nfaggian/growcut.png?branch=master)](https://travis-ci.org/nfaggian/growcut)

Dependencies
------------

The required dependencies to build the software are:

  - python
  - numpy
  - scipy
  - py.test

Install
-------

This packages uses distutils, which is the default way of installing python modules. To install in your home directory, use:

    python setup.py install --home

To install for all users on Unix/Linux:

    python setup.py build
    sudo python setup.py install

Examples
--------

Requires Matplotlib:

    python examples/conway.py
    
    python examples/flower.py

Requires PyQt4:

    python examples/gui.py

Development
-----------

Follow: Fork + Pull Model:

    http://help.github.com/send-pull-requests/
