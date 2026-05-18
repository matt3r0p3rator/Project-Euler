#include <cstdint>
#include <fstream>
#include <stdexcept>
#include <string>

#include "euler/problem.hpp"
#include <vector>

namespace {

std::vector<std::uint64_t> read_file(const std::string& filename) {
    std::ifstream input(filename);
    if (!input) {
        throw std::runtime_error("failed to open number file: " + filename);
    }

    std::vector<std::uint64_t> digits;
    char ch = '\0';
    while (input.get(ch)) {
        if (ch >= '0' && ch <= '9') {
            digits.push_back(static_cast<std::uint64_t>(ch - '0'));
        }
    }

    if (digits.empty()) {
        throw std::runtime_error("number file is empty");
    }

    return digits;
}  // Read number into a vector, one digit per element.

std::uint64_t solve() {
    constexpr std::size_t window_size = 13;
    std::uint64_t max_product = 0;
    const auto number = read_file("num.txt");

    if (number.size() < window_size) {
        throw std::runtime_error("number must contain at least 13 digits");
    }

    for (std::size_t i = 0; i + window_size <= number.size(); ++i) {
        std::uint64_t product = 1;
        for (std::size_t j = 0; j < window_size; ++j) {
            product *= number[i + j];
        }
        if (product > max_product) {
            max_product = product;
        }
    }
    return max_product;
}

}  // namespace

int main() {
    return euler::run_problem("Problem 0008", solve);
}
