#include <cstdint>

#include "euler/problem.hpp"

namespace {

std::uint64_t solve() {
    std::uint64_t sum = 0;
    for (std::uint64_t i = 0; i < 1000; ++i) {
        if (i % 3 == 0 || i % 5 == 0) {
            sum += i;
        }
    }
    return sum;
}

}  // namespace

int main() {
    return euler::run_problem("Problem 0001", solve);
}
