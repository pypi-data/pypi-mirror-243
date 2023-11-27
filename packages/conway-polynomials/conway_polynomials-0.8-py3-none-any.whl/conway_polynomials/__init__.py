r"""
Python interface to Frank Lübeck's Conway polynomial database

First, call ``database()`` to load the database into a python
dictionary, and then look up the coefficients of your polynomial using
two keys ``p`` (your prime) and ``n`` (your degree). The following
results for ``p=2`` can be found at,

  https://www.math.rwth-aachen.de/~Frank.Luebeck/data/ConwayPol/CP2.html

::

>>> import conway_polynomials
>>> cpdb = conway_polynomials.database()

>>> p = 2; n = 5
>>> cpdb[p][n]
(1, 0, 1, 0, 0, 1)

>>> p = 2; n = 17
>>> cpdb[p][n]
(1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)

>>> p = 23; n = 19
>>> cpdb[p][n]
(18, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)

>>> p = 307; n = 1
>>> cpdb[p][n]
(302, 1)

>>> p = 40013; n = 2
>>> cpdb[p][n]
(2, 40009, 1)

If ``n`` is the degree of our polynomial, there should be ``n+1``
coefficients, the last of which is unity by definition::

>>> from random import choice
>>> p = choice(list(cpdb.keys()))
>>> n = choice(list(cpdb[p].keys()))
>>> len(cpdb[p][n]) == n + 1
True
>>> cpdb[p][n][n] == 1
True

"""


def _parse_line(l: str) -> tuple[int, int, tuple[int,...]]:
    r"""
    Parse a single line (not the first or the last) from Frank
    Lübeck's data file.

    According to Frank's webpage, each line has the form,

      [p, n, [a0, a1, ..., 1]],

    and corresponds to a single Conway polynomial with prime p and
    degree n. In reality, there are no spaces in the data.

    Parameters
    ----------

    l : str
        A line from the data file.

    Returns
    -------

    tuple[int, int, tuple[int,...]]
      A triplet ``(p, n, coeffs)``, where ``p`` and ``n`` are python
      integers representing the prime and degree of this polynomial,
      respectively, and ``coeffs`` is a tuple of its coefficients.

    """
    # Remove all of the brackets, the trailing comma, and the trailing
    # newline to obtain "p, n, a0, a1, ..., 1".
    l = l.replace("[","")[:-4]

    # Now we know that p and n are the first two (CSV) fields, and
    # that the coefficients are whatever's left.
    fields = l.split(",")

    # Convert everything to integers before returning.
    p = int(fields[0])
    n = int(fields[1])
    coeffs = tuple( int(c) for c in fields[2:] )

    return (p, n, coeffs)


from typing import Optional
_conway_dict: Optional[ dict[int,dict[int,tuple[int,...]]] ]
_conway_dict = None    # cached result of database()
def database() -> dict[int,dict[int,tuple[int,...]]]:
    r"""
    Load (if necessary) and return a dict of pre-computed Conway
    polynomial coefficients.

    The result is cached.

    Returns
    -------

    dict
      A dictionary of the form ``{p: {n: coefficients}}``, where ``p``
      is a prime, ``n`` is a degree, and ``coefficients`` is a tuple
      of coefficients. The coefficients are listed in "ascending"
      order; that is, they are indexed by the degree of the monomial
      they sit in front of.

    """
    global _conway_dict

    if _conway_dict is not None:
        return _conway_dict

    _conway_dict = {}
    from importlib.resources import files
    dbpath = files('conway_polynomials').joinpath('CPimport.txt')
    with dbpath.open("r") as f:
        # The first line of the file is "allConwayPolynomials := ["
        f.readline()

        for line in f:
            if line[0] == "0":
                # This is the last line in the file; otherwise it would
                # start with a square bracket.
                break

            (p, n, coeffs) = _parse_line(line)
            if p not in _conway_dict:
                _conway_dict[p] = {}

            _conway_dict[p][n] = coeffs

    return _conway_dict


if __name__ == "__main__":
    import doctest
    doctest.testmod()
