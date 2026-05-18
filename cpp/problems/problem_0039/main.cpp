#include <cstdint>

#include "euler/problem.hpp"

namespace {

std::uint64_t solve() {
    std::uint64_t maxPerimeter = 1000;
    std::uint64_t maxSolutions = 0;
    std::uint64_t maxP = 0;

    for (std::uint64_t p = 2; p <= maxPerimeter; p += 2) {
        std::uint64_t solutions = 0;
        for (std::uint64_t a = 1; a < p / 2; ++a) {
            for (std::uint64_t b = a; b < p / 2; ++b) {
                std::uint64_t c = p - a - b;
                if (a * a + b * b == c * c) {
                    ++solutions;
                }
            }
        }
        if (solutions > maxSolutions) {
            maxSolutions = solutions;
            maxP = p;
        }
    }

    return maxP;
}

}  // namespace

int main() {
    return euler::run_problem("Problem 0039", solve);
}
