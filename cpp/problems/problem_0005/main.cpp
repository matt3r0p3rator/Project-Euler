#include <cstdint>

#include "euler/problem.hpp"
#include <algorithm>
#include <numeric>

namespace {

std::uint64_t solve() {
    std::uint64_t lcm = 1;
    for (std::uint64_t n = 2; n <= 20; ++n) {
        std::uint64_t gcd = std::gcd(lcm, n);
        lcm = lcm / gcd * n;
    }
    return lcm;
}

}  // namespace

int main() {
    return euler::run_problem("Problem 0005", solve);
}
