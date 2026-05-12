#include <cstdint>

#include "euler/problem.hpp"

namespace {
    std::uint64_t fibonacci(std::uint64_t n) {
        if (n == 0) {
            return 0;
        } else if (n == 1) {
            return 1;
        } else {
            return fibonacci(n - 1) + fibonacci(n - 2);
        }
    }
    

std::uint64_t solve() {
    std::uint64_t sum = 0;
    std::uint64_t n = 0;
    constexpr std::uint64_t nMax = 4000000;
    while (true) {
        const auto fib = fibonacci(n);
        if (fib > nMax) {
            break;
        } else if (fib % 2 == 0) {
            sum += fib;
        }
        ++n;
    }
    return sum;
}

}  // namespace

int main() {
    return euler::run_problem("Problem 0002", solve);
}
