#include <cstdint>

#include "euler/problem.hpp"

namespace {

    bool isPrime(std::uint64_t n) {
        if (n <= 1) {
            return false;
        }
        for (std::uint64_t i = 2; i * i <= n; ++i) {
            if (n % i == 0) {
                return false;
            }
        }
        return true;
    }

    std::uint64_t largestPrimeFactor(std::uint64_t n) {
        std::uint64_t largest = 0;
        for (std::uint64_t i = 2; i * i <= n; ++i) {
            while (n % i == 0) {
                largest = i;
                n /= i;
            }
        }
        if (n > 1) {
            largest = n;
        }
        return largest;
    }

std::uint64_t solve() {
    return largestPrimeFactor(600851475143);
}

}  // namespace

int main() {
    return euler::run_problem("Problem 0003", solve);
}
