#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "euler/problem.hpp"

namespace {

std::vector<std::string> read_words(const std::string& path) {
    std::ifstream input(path);
    if (!input) {
        throw std::runtime_error("failed to open words file: " + path);
    }

    std::vector<std::string> words;
    std::string token;
    while (std::getline(input, token, ',')) {
        if (token.size() >= 2 && token.front() == '"' && token.back() == '"') {
            token = token.substr(1, token.size() - 2);
        }
        if (!token.empty()) {
            words.push_back(std::move(token));
        }
    }

    return words;
}

std::string sort_letters(std::string word) {
    std::sort(word.begin(), word.end());
    return word;
}

std::vector<int> make_pattern(const std::string& value) {
    std::unordered_map<char, int> symbol_to_index;
    std::vector<int> pattern;
    pattern.reserve(value.size());

    int next_index = 0;
    for (char symbol : value) {
        const auto [iterator, inserted] = symbol_to_index.emplace(symbol, next_index);
        if (inserted) {
            ++next_index;
        }
        pattern.push_back(iterator->second);
    }

    return pattern;
}

std::unordered_map<std::size_t, std::vector<std::string>> generate_squares_by_length(std::size_t max_length) {
    std::unordered_map<std::size_t, std::vector<std::string>> squares_by_length;

    std::uint64_t square_root = 1;
    while (true) {
        const std::uint64_t square = square_root * square_root;
        const std::string square_text = std::to_string(square);
        if (square_text.size() > max_length) {
            break;
        }

        squares_by_length[square_text.size()].push_back(square_text);
        ++square_root;
    }

    return squares_by_length;
}

std::unordered_map<std::size_t, std::unordered_set<std::string>> make_square_sets(
    const std::unordered_map<std::size_t, std::vector<std::string>>& squares_by_length) {
    std::unordered_map<std::size_t, std::unordered_set<std::string>> square_sets;

    for (const auto& [length, squares] : squares_by_length) {
        auto& square_set = square_sets[length];
        square_set.reserve(squares.size());
        for (const auto& square : squares) {
            square_set.insert(square);
        }
    }

    return square_sets;
}

std::string map_word_to_digits(const std::string& source_word, const std::string& target_word,
                               const std::string& digits) {
    std::array<char, 26> letter_to_digit{};
    letter_to_digit.fill('\0');

    for (std::size_t index = 0; index < source_word.size(); ++index) {
        letter_to_digit[source_word[index] - 'A'] = digits[index];
    }

    std::string mapped_digits;
    mapped_digits.reserve(target_word.size());
    for (char letter : target_word) {
        mapped_digits.push_back(letter_to_digit[letter - 'A']);
    }

    return mapped_digits;
}

std::uint64_t solve() {
    const auto words = read_words("0098_words.txt");

    std::unordered_map<std::string, std::vector<std::string>> anagram_groups;
    std::size_t max_length = 0;
    for (const auto& word : words) {
        max_length = std::max(max_length, word.size());
        anagram_groups[sort_letters(word)].push_back(word);
    }

    const auto squares_by_length = generate_squares_by_length(max_length);
    const auto square_sets = make_square_sets(squares_by_length);

    std::uint64_t largest_square = 0;

    for (const auto& [_, group] : anagram_groups) {
        if (group.size() < 2) {
            continue;
        }

        const std::size_t length = group.front().size();
        const auto squares_it = squares_by_length.find(length);
        const auto square_set_it = square_sets.find(length);
        if (squares_it == squares_by_length.end() || square_set_it == square_sets.end()) {
            continue;
        }

        for (std::size_t left = 0; left + 1 < group.size(); ++left) {
            const auto word_pattern = make_pattern(group[left]);

            for (const auto& square : squares_it->second) {
                if (make_pattern(square) != word_pattern) {
                    continue;
                }

                for (std::size_t right = left + 1; right < group.size(); ++right) {
                    const std::string mapped_square = map_word_to_digits(group[left], group[right], square);
                    if (mapped_square.front() == '0' ||
                        square_set_it->second.find(mapped_square) == square_set_it->second.end()) {
                        continue;
                    }

                    largest_square = std::max(largest_square, static_cast<std::uint64_t>(std::stoull(square)));
                    largest_square = std::max(largest_square, static_cast<std::uint64_t>(std::stoull(mapped_square)));
                }
            }
        }
    }

    return largest_square;
}

}  // namespace

int main() {
    return euler::run_problem("Problem 0098", solve);
}
