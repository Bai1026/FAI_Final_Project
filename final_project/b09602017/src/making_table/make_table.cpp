// #include <iostream>
// #include <fstream>
// #include "json.hpp"  // 使用JSON for Modern C++

// using json = nlohmann::json;

// json evaluate_preflop_hand(const std::string& hand) {
//     // 模拟评估逻辑，这里返回一个示例结果
//     json result;
//     result["strength"] = rand() % 100;  // 随机数作为示例
//     return result;
// }

// void generate_preflop_table() {
//     json preflopTable;
//     for (int i = 0; i < 13; ++i) {
//         for (int j = 0; j < 13; ++j) {
//             std::string hand = "Hand_" + std::to_string(i) + "_" + std::to_string(j);  // 示例手牌
//             preflopTable[i][j] = evaluate_preflop_hand(hand);
//         }
//     }

//     std::ofstream file("preflop_table.json");
//     file << preflopTable.dump(4);  // 格式化输出，缩进4个空格
//     file.close();
// }

// int main() {
//     generate_preflop_table();
//     return 0;
// }


// #include <iostream>
// #include <fstream>
// #include <string>
// #include <vector>
// #include <map>
// #include "json.hpp"  // 使用JSON for Modern C++

// using json = nlohmann::json;

// // 假设你有一个函数evaluate_hand_strength来计算手牌的强度
// int evaluate_hand_strength(const std::string& hand) {
//     // 简单的示例算法，实际应用中会更复杂
//     // 这里使用手牌中的字符计算强度
//     int strength = 0;
//     for (char ch : hand) {
//         if (isdigit(ch)) {
//             strength += (ch - '0');
//         } else if (ch == 'T') {
//             strength += 10;
//         } else if (ch == 'J') {
//             strength += 11;
//         } else if (ch == 'Q') {
//             strength += 12;
//         } else if (ch == 'K') {
//             strength += 13;
//         } else if (ch == 'A') {
//             strength += 14;
//         }
//     }
//     return strength;
// }

// json evaluate_preflop_hand(const std::string& hand) {
//     json result;
//     result["hand"] = hand;
//     result["strength"] = evaluate_hand_strength(hand);  // 使用评估函数计算强度
//     return result;
// }

// void generate_preflop_table() {
//     json preflopTable;
//     std::vector<std::string> ranks = {"2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"};
//     std::vector<std::string> suits = {"s", "h", "d", "c"};

//     for (const auto& rank1 : ranks) {
//         for (const auto& rank2 : ranks) {
//             std::string hand_offsuit = rank1 + "o" + rank2;
//             std::string hand_suited = rank1 + "s" + rank2;
//             preflopTable[rank1][rank2]["offsuit"] = evaluate_preflop_hand(hand_offsuit);
//             preflopTable[rank1][rank2]["suited"] = evaluate_preflop_hand(hand_suited);
//         }
//     }

//     std::ofstream file("preflop_table.json");
//     file << preflopTable.dump(4);  // 格式化输出，缩进4个空格
//     file.close();
// }

// int main() {
//     generate_preflop_table();
//     return 0;
// }


// #include <iostream>
// #include <fstream>
// #include <vector>
// #include <thread>
// #include <json.hpp>  // 使用JSON for Modern C++

// using json = nlohmann::json;

// // 手牌强度评估函数（示例：简单的随机数生成）
// int evaluate_hand_strength(const std::string& hand) {
//     return rand() % 100;
// }

// // 生成preflop表
// void generate_preflop_table() {
//     json preflopTable;
//     std::vector<std::string> ranks = {"2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"};

//     for (const auto& rank1 : ranks) {
//         for (const auto& rank2 : ranks) {
//             if (rank1 != rank2) {
//                 std::string hand_offsuit = rank1 + rank2 + "o";
//                 std::string hand_suited = rank1 + rank2 + "s";
//                 preflopTable[rank1][rank2]["offsuit"] = evaluate_hand_strength(hand_offsuit);
//                 preflopTable[rank1][rank2]["suited"] = evaluate_hand_strength(hand_suited);
//             }
//         }
//     }

//     std::ofstream file("preflop_table.json");
//     file << preflopTable.dump(4);  // 格式化输出，缩进4个空格
//     file.close();
// }

// int main() {
//     generate_preflop_table();
//     return 0;
// }



// #include <iostream>
// #include <fstream>
// #include <vector>
// #include <string>
// #include <algorithm>
// #include <random>
// #include <json.hpp>

// using json = nlohmann::json;

// // 函数：计算模拟胜率（这里只是一个示例，实际需要更复杂的逻辑）
// double simulate_win_rate(const std::string& hand1, const std::string& hand2) {
//     // 模拟大量游戏局以计算胜率
//     // 示例：简单地随机生成一个胜率
//     std::random_device rd;
//     std::mt19937 gen(rd());
//     std::uniform_real_distribution<> dis(0.0, 1.0);
//     return dis(gen);
// }

// // 函数：生成13x13的胜率表
// void generate_preflop_table(json& preflop_table) {
//     std::string ranks = "AKQJT98765432";
//     int n = ranks.size();

//     for (int i = 0; i < n; ++i) {
//         for (int j = 0; j < n; ++j) {
//             std::string hand1, hand2;
//             if (i < j) {
//                 hand1 = ranks[i] + "s";  // 同花
//                 hand2 = ranks[j] + "s";
//             } else {
//                 hand1 = ranks[i] + "o";  // 不同花
//                 hand2 = ranks[j] + "o";
//             }

//             double win_rate = simulate_win_rate(hand1, hand2);
//             preflop_table[ranks[i] + (i < j ? "s" : "o")][ranks[j] + (i < j ? "s" : "o")] = win_rate;
//         }
//     }
// }

// // 函数：将胜率表保存为JSON文件
// void save_to_json(const json& preflop_table, const std::string& filename) {
//     std::ofstream file(filename);
//     file << preflop_table.dump(4);  // 格式化输出，缩进4空格
//     file.close();
// }

// int main() {
//     json preflop_table;

//     generate_preflop_table(preflop_table);
//     save_to_json(preflop_table, "preflop_win_rates.json");

//     std::cout << "Preflop win rates table saved to preflop_win_rates.json" << std::endl;

//     return 0;
// }


// #include <iostream>
// #include <fstream>
// #include <vector>
// #include <string>
// #include <algorithm>
// #include <random>
// #include <json.hpp>

// using json = nlohmann::json;

// // 函数：计算模拟胜率（这里只是一个示例，实际需要更复杂的逻辑）
// double simulate_win_rate(const std::string& hand1, const std::string& hand2) {
//     // 模拟大量游戏局以计算胜率
//     // 示例：简单地随机生成一个胜率
//     std::random_device rd;
//     std::mt19937 gen(rd());
//     std::uniform_real_distribution<> dis(0.0, 1.0);
//     return dis(gen);
// }

// // 函数：生成13x13的胜率表
// void generate_preflop_table(json& preflop_table) {
//     std::string ranks = "AKQJT98765432";
//     int n = ranks.size();

//     for (int i = 0; i < n; ++i) {
//         for (int j = 0; j < n; ++j) {
//             std::string hand1, hand2;
//             if (i < j) {
//                 hand1 = std::string(1, ranks[i]) + std::string(1, ranks[j]) + "s";  // 同花
//                 hand2 = std::string(1, ranks[j]) + std::string(1, ranks[i]) + "s";
//             } else if (i > j) {
//                 hand1 = std::string(1, ranks[i]) + std::string(1, ranks[j]) + "o";  // 不同花
//                 hand2 = std::string(1, ranks[j]) + std::string(1, ranks[i]) + "o";
//             } else {
//                 hand1 = std::string(1, ranks[i]) + std::string(1, ranks[j]);
//                 hand2 = hand1;
//             }

//             double win_rate = simulate_win_rate(hand1, hand2);
//             preflop_table[hand1] = win_rate;
//         }
//     }
// }

// // 函数：将胜率表保存为JSON文件
// void save_to_json(const json& preflop_table, const std::string& filename) {
//     std::ofstream file(filename);
//     file << preflop_table.dump(4);  // 格式化输出，缩进4空格
//     file.close();
// }

// int main() {
//     json preflop_table;

//     generate_preflop_table(preflop_table);
//     save_to_json(preflop_table, "preflop_win_rates.json");

//     std::cout << "Preflop win rates table saved to preflop_win_rates.json" << std::endl;

//     return 0;
// }


// #include <iostream>
// #include <fstream>
// #include <vector>
// #include <string>
// #include <algorithm>
// #include <random>
// #include <json.hpp>

// using json = nlohmann::json;

// // 函数：计算模拟胜率（这里只是一个示例，实际需要更复杂的逻辑）
// double simulate_win_rate(const std::string& hand1, const std::string& hand2) {
//     // 模拟大量游戏局以计算胜率
//     // 示例：简单地随机生成一个胜率
//     std::random_device rd;
//     std::mt19937 gen(rd());
//     std::uniform_real_distribution<> dis(0.0, 1.0);
//     return dis(gen);
// }

// // 函数：生成13x13的胜率表
// void generate_preflop_table(json& preflop_table) {
//     std::string ranks = "AKQJT98765432";
//     int n = ranks.size();

//     for (int i = 0; i < n; ++i) {
//         for (int j = 0; j < n; ++j) {
//             if (i == j) continue; // 排除同一张牌

//             std::string hand1, hand2;
//             if (i < j) {
//                 hand1 = std::string(1, ranks[i]) + std::string(1, ranks[j]) + "s";  // 同花
//                 hand2 = std::string(1, ranks[j]) + std::string(1, ranks[i]) + "s";
//             } else {
//                 hand1 = std::string(1, ranks[i]) + std::string(1, ranks[j]) + "o";  // 不同花
//                 hand2 = std::string(1, ranks[j]) + std::string(1, ranks[i]) + "o";
//             }

//             double win_rate = simulate_win_rate(hand1, hand2);
//             preflop_table[hand1] = win_rate;
//         }
//     }
// }

// // 函数：将胜率表保存为JSON文件
// void save_to_json(const json& preflop_table, const std::string& filename) {
//     std::ofstream file(filename);
//     file << preflop_table.dump(4);  // 格式化输出，缩进4空格
//     file.close();
// }

// int main() {
//     json preflop_table;

//     generate_preflop_table(preflop_table);
//     save_to_json(preflop_table, "preflop_win_rates2.json");

//     std::cout << "Preflop win rates table saved to preflop_win_rates.json" << std::endl;

//     return 0;
// }


#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <random>
#include <json.hpp>

using json = nlohmann::json;

// 函数：模拟一次德州扑克对局
bool simulate_hand(const std::vector<int>& hand1, const std::vector<int>& hand2, std::mt19937& gen) {
    // 生成一个52张牌的牌堆
    std::vector<int> deck(52);
    std::iota(deck.begin(), deck.end(), 0);
    std::shuffle(deck.begin(), deck.end(), gen);

    // 手牌已经在deck中移除

    // 模拟公共牌（Flop, Turn, River）
    // 示例代码不包含具体的评估逻辑，假设手牌1总是赢，手牌2总是输
    // 需要实现实际的牌力计算逻辑
    return true; // 示例：假设手牌1总是赢
}

// 函数：计算手牌的胜率
void calculate_win_rate(const std::vector<int>& hand1, int num_simulations, double& win, double& lose, double& tie) {
    win = lose = tie = 0;
    std::random_device rd;
    std::mt19937 gen(rd());

    for (int i = 0; i < num_simulations; ++i) {
        std::vector<int> opponent_hand = { rand() % 52, rand() % 52 };
        if (simulate_hand(hand1, opponent_hand, gen)) {
            win++;
        } else {
            lose++;
        }
    }

    win /= num_simulations;
    lose /= num_simulations;
    tie = 1.0 - win - lose;
}

void generate_preflop_table(json& preflop_table, int num_simulations) {
    std::string ranks = "AKQJT98765432";
    int n = ranks.size();

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (i == j) continue; // for same card

            std::vector<int> hand1 = { i, j };
            double win, lose, tie;
            calculate_win_rate(hand1, num_simulations, win, lose, tie);

            std::string hand_key;
            if (i < j) {
                hand_key = std::string(1, ranks[i]) + std::string(1, ranks[j]) + "s";  // 同花
            } else {
                hand_key = std::string(1, ranks[i]) + std::string(1, ranks[j]) + "o";  // 不同花
            }

            preflop_table[hand_key] = {
                {"win", win},
                {"lose", lose},
                {"tie", tie}
            };
        }
    }
}

// 函数：将胜率表保存为JSON文件
void save_to_json(const json& preflop_table, const std::string& filename) {
    std::ofstream file(filename);
    file << preflop_table.dump(4);  // 格式化输出，缩进4空格
    file.close();
}

int main() {
    json preflop_table;
    int num_simulations = 100000;  // 模拟次数

    generate_preflop_table(preflop_table, num_simulations);
    save_to_json(preflop_table, "preflop_win_rates3.json");

    std::cout << "Preflop win rates table saved to preflop_win_rates.json" << std::endl;

    return 0;
}
