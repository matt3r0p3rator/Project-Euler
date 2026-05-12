from itertools import product
from fractions import Fraction
import collections

def hackenbush_value(stack):
    if not stack: return Fraction(0)
    first_color = stack[0]
    n = 0
    for coin in stack:
        if coin == first_color:
            n += 1
        else:
            break
    val = Fraction(n if first_color == 'G' else -n)
    for i in range(n, len(stack)):
        delta = Fraction(1, 2**(i - n + 1))
        if stack[i] == 'G':
            val += delta
        else:
            val -= delta
    return val

def solve_G(m):
    stacks = []
    for h in range(1, m + 1):
        for coins in product('GS', repeat=h):
            stacks.append(coins)
    
    # Precompute (value, g-s) for each stack
    data = []
    for s in stacks:
        v = hackenbush_value(s)
        gs_diff = s.count('G') - s.count('S')
        data.append((v, gs_diff))
    
    # Store by gs_diff to speed up the triplet search
    # We need (gs1 + gs2 + gs3) == 0  => gs3 = -(gs1 + gs2)
    by_gs = collections.defaultdict(list)
    for v, gs in data:
        by_gs[gs].append(v)
    
    count = 0
    gs_keys = sorted(by_gs.keys())
    for gs1 in gs_keys:
        for gs2 in gs_keys:
            gs3 = -(gs1 + gs2)
            if gs3 in by_gs:
                # Count pairs of (v1, v2) such that v1 + v2 + v3 == 0
                # v3 = -(v1 + v2)
                # Instead of looping v3, use a counter for by_gs[gs3]
                v3_counts = collections.Counter(by_gs[gs3])
                for v1 in by_gs[gs1]:
                    for v2 in by_gs[gs2]:
                        target_v3 = -(v1 + v2)
                        count += v3_counts[target_v3]
    return count

for m in [2, 3, 4]:
    print(f"G({m}) = {solve_G(m)}")
