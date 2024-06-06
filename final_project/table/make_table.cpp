#include <iostream>
#include <fstream>
#include "json.hpp"  // 使用JSON for Modern C++

using json = nlohmann::json;

json evaluate_preflop_hand(const std::string& hand) {
    // 模拟评估逻辑，这里返回一个示例结果
    json result;
    result["strength"] = rand() % 100;  // 随机数作为示例
    return result;
}

void generate_preflop_table() {
    json preflopTable;
    for (int i = 0; i < 13; ++i) {
        for (int j = 0; j < 13; ++j) {
            std::string hand = "Hand_" + std::to_string(i) + "_" + std::to_string(j);  // 示例手牌
            preflopTable[i][j] = evaluate_preflop_hand(hand);
        }
    }

    std::ofstream file("preflop_table.json");
    file << preflopTable.dump(4);  // 格式化输出，缩进4个空格
    file.close();
}

int main() {
    generate_preflop_table();
    return 0;
}
