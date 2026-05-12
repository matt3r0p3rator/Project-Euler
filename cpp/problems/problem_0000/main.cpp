#include <cstdint>

#include "euler/problem.hpp"

namespace {

std::uint64_t solve() {
    // add sum of first 557,000 odd square numbers
    std::uint64_t sum = 0;
    std::uint64_t square = 0;
    for (std::uint64_t i = 1; i <= 557000; i += 1) {
        square = i * i;
        if (square % 2 == 1) {
            sum += square;
        }
    }
    return sum;
}

}  // namespace

int main() {
    return euler::run_problem("Problem 0000", solve);
}
