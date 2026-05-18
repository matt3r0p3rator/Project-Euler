#include <cstdint>

#include "euler/problem.hpp"
#include <vector>

namespace {
    // find different way to make n using primes
    int count_partitions(int n, const std::vector<int>& primes) {
        std::vector<int> partitions(n + 1, 0);
        partitions[0] = 1;  // Base case: there's one way to partition 0

        for (const int prime : primes) {
            for (int i = prime; i <= n; ++i) {
                partitions[i] += partitions[i - prime];
            }
        }

        return partitions[n];
    }

std::uint64_t solve() {
    const int target = 100;
    std::vector<int> primes;

    // Generate prime numbers up to target
    for (int num = 2; num <= target; ++num) {
        bool is_prime = true;
        for (int div = 2; div * div <= num; ++div) {
            if (num % div == 0) {
                is_prime = false;
                break;
            }
        }
        if (is_prime) {
            primes.push_back(num);
        }
    }

    return count_partitions(target, primes);
}

}  // namespace

int main() {
    return euler::run_problem("Problem 0077", solve);
}
