#include <cstdint>

#include "euler/problem.hpp"

namespace {
std::uint64_t solve() {
    std::uint64_t max_palindrome = 0;
    for (std::uint64_t i = 100; i <= 999; ++i) {
        for (std::uint64_t j = i; j <= 999; ++j) {
            std::uint64_t product = i * j;
            std::string str_product = std::to_string(product);
            std::string reversed_str_product(str_product.rbegin(), str_product.rend());
            if (str_product == reversed_str_product && product > max_palindrome) {
                max_palindrome = product;
            }
        }
    }
    return max_palindrome;
}}  // namespace

int main() {
    return euler::run_problem("Problem 0004", solve);
}
