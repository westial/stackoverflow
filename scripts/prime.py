#!/usr/bin/env python
# See https://iluxonchik.github.io/regular-expression-check-if-number-is-prime/
from re import match

NO_PRIME_PATTERN = "^.?$|^(..+?)\\1+$"


def to_unary(in_number):
    number = int(in_number)
    unary = ""
    while number:
        unary += "1"
        number -= 1
    return unary


def is_prime(unary):
    return not match(NO_PRIME_PATTERN, unary)


def ask_prime():
    in_number = input("Write number: ")
    unary = to_unary(in_number)
    if is_prime(unary):
        print("{!s} is prime".format(in_number))
    else:
        print("{!s} is NOT prime".format(in_number))


while True:
    ask_prime()
