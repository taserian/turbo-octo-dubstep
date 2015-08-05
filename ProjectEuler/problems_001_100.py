from project_euler_tools import *
import sys
import inspect


def is_mod_function(mod, func):
    return inspect.isfunction(func) and inspect.getmodule(func) == mod


def list_functions(mod):
    return [func.__name__ for func in mod.__dict__.itervalues()
            if is_mod_function(mod, func)]


def problem001():
    """
    Solve problem 001
    """
    L, a, b = 999, 3, 5
    som = sumn(L, a) + sumn(L, b) - sumn(L, a*b)
    print som, "sum of multiples of", a, "or", b, "below", L+1


def problem002():
    L = 4000000
    x, y, s = 1, 1, 0

    while s < L:
        s += (x + y)
        x, y = x + 2*y, 2*x + 3*y

    print s, "even Fibonacci numbers <", L


def problem003():
    N = n = 600851475143
    p = 2

    while p*p <= n:
        if n % p == 0:
            n //= p
        else:
            p += 2 if p>2 else 1   # after 2, consider only odd p

    print n, "is the largest prime factor of", N


def problem004():
    def is_palindromic(n): n=str(n); return n==n[::-1]

    pmax = 0
    for i in range(999, 100, -2):
        for j in range(i, 900, -2):
            p = i*j
            if p < pmax: break
            if is_palindromic(p): x, y, pmax = i, j, p

    print "Project Euler  4 Solution = %3d x %3d = %6d" % (x, y, pmax)


def problem005():
    def lcm(a, b):
        return a // gcd(a, b) * b
    L = 20
    print "Project Euler 5 Solution:", reduce(lcm, range(L//2+1, L+1))


def problem006():
    n = 100
    sq_of_sum = (n * (n + 1) // 2) ** 2
    sum_of_sq = n * (n + 1) * (2*n + 1) // 6
    print "Project Euler 6 Solution =", sq_of_sum - sum_of_sq


def problem007():
    n = 10001
    p, f = 5, 1

    while n > 3:
        p += 3-f
        f = -f
        if is_prime(p):
            n -= 1

    print "Project Euler 7 Solution =", p


def problem008():
    s = ('73167176531330624919225119674426574742355349194934'
     '96983520312774506326239578318016984801869478851843'
     '85861560789112949495459501737958331952853208805511'
     '12540698747158523863050715693290963295227443043557'
     '66896648950445244523161731856403098711121722383113'
     '62229893423380308135336276614282806444486645238749'
     '30358907296290491560440772390713810515859307960866'
     '70172427121883998797908792274921901699720888093776'
     '65727333001053367881220235421809751254540594752243'
     '52584907711670556013604839586446706324415722155397'
     '53697817977846174064955149290862569321978468622482'
     '83972241375657056057490261407972968652414535100474'
     '82166370484403199890008895243450658541227588666881'
     '16427171479924442928230863465674813919123162824586'
     '17866458359124566529476545682848912883142607690042'
     '24219022671055626321111109370544217506941658960408'
     '07198403850962455444362981230987879927244284909188'
     '84580156166097919133875499200524063689912560717606'
     '05886116467109405077541002256983155200055935729725'
     '71636269561882670428252483600823257530420752963450')

s = map(int, s) # Convert string to a list of single digit integers (0-9)
s_max = -1
s_len = 13

for i in range(len(s) - s_len+1):
    p = 1
    for j in s[i:i+s_len]:
        p *= j
    s_max = max(s_max, p)

print 'Greatest product of', s_len, 'consecutive \ndigits =', s_max

def main():
    """
    :param args:
    """
    possibles = globals().copy()
    possibles.update(locals())
    problem_functions = sorted( filter(lambda x: x.startswith("problem"), list_functions(sys.modules[__name__])))
    for p in problem_functions:
        function = possibles.get(p)
        print p
        function()



if __name__ == "__main__":
    main()