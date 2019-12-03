def pgcd (a, b):
    "Plus grand commun diviseur de deux entiers naturels"
    assert type(a) is int and a >= 0
    assert type(b) is int and b >= 0
    if a < b:
        (a, b) = (b, a)
    while b > 0:
        (a, b) = (b, a % b)
    return a

# test unitaire
assert pgcd(8 * 3 * 5 * 13, 4 * 5 * 7 * 17) == 4 * 5
