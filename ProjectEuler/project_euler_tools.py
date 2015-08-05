from math import sqrt


def sumn(n, d):  # sum numbers <= n that are divisible by d
    n //= d
    return d * n * (n + 1) // 2


def gcd(a, b):
    """
    Compute the greatest common divisor of a and b. Examples:

    >>> gcd(14, 15)    #co-prime
    1
    >>> gcd(5*5, 3*5)
    5
    """
    if a < 0:
        a = -a
    if b < 0:
        b = -b
    if a == 0:
        return b
    while b != 0:
        a, b = b, a % b
    return a


def is_prime(n):
    n = int(n)
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    if n < 9:
        return True
    if n % 3 == 0:
        return False
    r = int(sqrt(n))
    f = 5
    while f <= r:
        if n % f == 0:
            return False
        if n % (f + 2) == 0:
            return False
        f += 6
    return True