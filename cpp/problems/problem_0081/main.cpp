#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

#include "euler/problem.hpp"

namespace {

std::vector<std::vector<std::uint64_t>> read_matrix(const std::string& path) {
    std::ifstream input(path);
    if (!input) {
        throw std::runtime_error("failed to open matrix file: " + path);
    }

    std::vector<std::vector<std::uint64_t>> matrix;
    std::string line;
    while (std::getline(input, line)) {
        std::stringstream line_stream(line);
        std::vector<std::uint64_t> row;
        std::string cell;

        while (std::getline(line_stream, cell, ',')) {
            row.push_back(std::stoull(cell));
        }

        if (!row.empty()) {
            matrix.push_back(std::move(row));
        }
    }

    if (matrix.empty()) {
        throw std::runtime_error("matrix file is empty");
    }

    const std::size_t expected_columns = matrix.front().size();
    for (const auto& row : matrix) {
        if (row.size() != expected_columns) {
            throw std::runtime_error("matrix rows must all have the same width");
        }
    }

    return matrix;
}

std::uint64_t solve() {
    const auto matrix = read_matrix("0081_matrix.txt");
    const std::size_t rows = matrix.size();
    const std::size_t columns = matrix.front().size();

    std::vector<std::uint64_t> min_path_sums(columns, 0);
    min_path_sums.front() = matrix.front().front();

    for (std::size_t column = 1; column < columns; ++column) {
        min_path_sums[column] = min_path_sums[column - 1] + matrix.front()[column];
    }

    for (std::size_t row = 1; row < rows; ++row) {
        min_path_sums.front() += matrix[row].front();

        for (std::size_t column = 1; column < columns; ++column) {
            min_path_sums[column] = std::min(min_path_sums[column], min_path_sums[column - 1]) + matrix[row][column];
        }
    }

    return min_path_sums.back();
}

}  // namespace

int main() {
    return euler::run_problem("Problem 0081", solve);
}
