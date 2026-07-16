"""Kata Potter (bookshop pricing).

Price a basket of books from a five-title series so the customer pays as
little as possible. A single book costs EUR 8.00. Buying distinct titles
together earns a discount on that set: 5% for two different books, 10% for
three, 20% for four, and 25% for all five (so sets cost 8.00, 15.20, 21.60,
25.60 and 30.00). When the basket holds multiple copies, they must be split
into sets of distinct titles whose combined price is minimal — greedily
building the largest possible sets is not always best. The classic trap:
two copies each of titles 1-3 plus one each of 4 and 5 costs 51.20 as two
sets of four, beating the 51.60 from a set of five plus a set of three.

Kata catalogued at tddbuddy.com/katas/kata-potter; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from kata_potter.kata_potter import BOOK_PRICE_CENTS, BOOKS, price

__all__ = ["BOOKS", "BOOK_PRICE_CENTS", "price"]
