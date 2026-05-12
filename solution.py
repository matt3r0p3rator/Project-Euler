from itertools import product
from fractions import Fraction

def hackenbush_value_v2(stack):
    \"\"\"
    Compute the partizan Hackenbush string value of a stack.
    From Winning Ways: a sequence of moves G (Left) and S (Right).
    \"\"\"
    if not stack:
        return Fraction(0)
    
    lo = None  
    hi = None  
    current = Fraction(0)
    
    for coin in stack:
        if coin == 'G':  
            lo = current
            if hi is None:
                current = current + 1
            else:
                current = (current + hi) / 2
        else:  
            hi = current
            if lo is None:
                current = current - 1
            else:
                current = (lo + current) / 2
    
    return current

def count_G(m):
    stacks = []
    for h in range(1, m+1):
        for coins in product('GS', repeat=h):
            stacks.append(coins)
    
    count = 0
    # The problem asks for stacks (s1, s2, s3)
    # 1. Total number of G and S are equal
    # 2. Game is fair (second player wins), which means value = 0 in Hackenbush
    for s1 in stacks:
        for s2 in stacks:
            for s3 in stacks:
                combined = s1 + s2 + s3
                g = combined.count('G')
                s = combined.count('S')
                if g != s:
                    continue
                v1 = hackenbush_value_v2(s1)
                v2 = hackenbush_value_v2(s2)
                v3 = hackenbush_value_v2(s3)
                if v1 + v2 + v3 == 0:
                    count += 1
    return count

print(\"0\")
print(\"G =\", hackenbush_value_v2(('G',)))
print(\"S =\", hackenbush_value_v2(('S',)))
print(\"GG =\", hackenbush_value_v2(('G','G')))
print(\"GS =\", hackenbush_value_v2(('G','S')))
print(\"SG =\", hackenbush_value_v2(('S','G')))
print(\"SS =\", hackenbush_value_v2(('S','S')))
print(\"GGS =\", hackenbush_value_v2(('G','G','S')))
print(\"GSG =\", hackenbush_value_v2(('G','S','G')))
print(\"GSS =\", hackenbush_value_v2(('G','S','S')))

print(\"\\nG(2) =\", count_G(2))
print(\"G(3) =\", count_G(3))
print(\"G(4) =\", count_G(4))
print(\"G(5) =\", count_G(5))
