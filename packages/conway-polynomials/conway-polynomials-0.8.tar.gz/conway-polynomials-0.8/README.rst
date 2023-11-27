Python interface to Frank Lübeck's Conway polynomial database

Introduction
============

Frank Lübeck maintains a list of pre-computed Conway polynomial
coefficients at,

  https://www.math.rwth-aachen.de/~Frank.Luebeck/data/ConwayPol/index.html

These are used in several computer algebra systems such as GAP and
SageMath to provide quick access to those Conway polynomials. The aim
of this package is to make them available through a generic python
interface. The package consists of a single module containing a single
function that returns a dict of dicts, ``conway_polynomials.database()``.
The dictionary's format is ``{p: {n: coefficients}}``, where ``p``
represents your prime and ``n`` your degree. The tuple of coefficients
is returned in ascending order; that is, the first coefficient (at
index zero) is for the constant (degree zero) term.

This package is an evolution of the SageMath *conway_polynomials*
package hosted at,

  http://files.sagemath.org/spkg/upstream/conway_polynomials/

and is maintained by the same team of developers. We have kept the
versioning scheme consistent to reflect that.


Examples
========

Retrieve the coefficients of the Conway polynomial for prime p=2 and
degree n=5::

  >>> import conway_polynomials
  >>> cpdb = conway_polynomials.database()
  >>> cpdb[2][5]
  (1, 0, 1, 0, 0, 1)

The result is cached, so subsequent computations should be fast even
if you call the function again::

  >>> conway_polynomials.database() is conway_polynomials.database()
  True

However, the result is also mutable, so if you need to modify it for
some reason then you should create a copy; otherwise your changes will
affect future calls::

  >>> cpdb = conway_polynomials.database()
  >>> cpdb[5][5]
  (3, 4, 0, 0, 0, 1)
  >>> cpdb[5][5] = (8, 6, 7, 5, 3, 0, 9)
  >>> conway_polynomials.database()[5][5]
  (8, 6, 7, 5, 3, 0, 9)


Testing
=======

A few doctests within the module (and this README) ensure that
everything is working. You can run them from the repository or from a
release tarball using::

  PYTHONPATH=src python -m doctest \
    README.rst \
    src/conway_polynomials/__init__.py
