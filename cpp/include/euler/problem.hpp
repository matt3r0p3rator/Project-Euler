#pragma once

#include <chrono>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <string>

namespace euler {

template <typename Solver>
int run_problem(const std::string& problem_name, Solver solver) {
    const auto start = std::chrono::steady_clock::now();
    const auto answer = solver();
    const auto end = std::chrono::steady_clock::now();

    const std::chrono::duration<double, std::milli> elapsed = end - start;

    std::cout << problem_name << '\n';
    std::cout << "answer: " << answer << '\n';
    std::cout << "time:   " << std::fixed << std::setprecision(3) << elapsed.count() << " ms\n";

    return EXIT_SUCCESS;
}

}  // namespace euler
