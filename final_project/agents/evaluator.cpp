// #include <iostream>
// #include <string>
// #include <vector>
// #include <algorithm>
// #include <map>
// #include <thread>
// #include <mutex>
// #include <unordered_map>

// std::mutex mtx;

// enum Rank {
//     TWO = 2, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE
// };

// enum Suit {
//     HEARTS, DIAMONDS, CLUBS, SPADES
// };

// struct Card {
//     Rank rank;
//     Suit suit;
// };

// struct Hand {
//     Card card1;
//     Card card2;
// };

// bool operator==(const Card& lhs, const Card& rhs) {
//     return lhs.rank == rhs.rank && lhs.suit == rhs.suit;
// }

// std::vector<Card> get_deck() {
//     std::vector<Card> deck;
//     for (int r = TWO; r <= ACE; ++r) {
//         for (int s = HEARTS; s <= SPADES; ++s) {
//             deck.push_back(Card{static_cast<Rank>(r), static_cast<Suit>(s)});
//         }
//     }
//     return deck;
// }

// std::string card_to_string(const Card& card) {
//     std::string str;
//     switch (card.rank) {
//         case TWO: str += '2'; break;
//         case THREE: str += '3'; break;
//         case FOUR: str += '4'; break;
//         case FIVE: str += '5'; break;
//         case SIX: str += '6'; break;
//         case SEVEN: str += '7'; break;
//         case EIGHT: str += '8'; break;
//         case NINE: str += '9'; break;
//         case TEN: str += 'T'; break;
//         case JACK: str += 'J'; break;
//         case QUEEN: str += 'Q'; break;
//         case KING: str += 'K'; break;
//         case ACE: str += 'A'; break;
//     }
//     switch (card.suit) {
//         case HEARTS: str += 'H'; break;
//         case DIAMONDS: str += 'D'; break;
//         case CLUBS: str += 'C'; break;
//         case SPADES: str += 'S'; break;
//     }
//     return str;
// }

// Card parse_card(const std::string& str) {
//     static std::unordered_map<char, Rank> rank_map = {
//         {'2', TWO}, {'3', THREE}, {'4', FOUR}, {'5', FIVE}, {'6', SIX},
//         {'7', SEVEN}, {'8', EIGHT}, {'9', NINE}, {'T', TEN},
//         {'J', JACK}, {'Q', QUEEN}, {'K', KING}, {'A', ACE}
//     };

//     static std::unordered_map<char, Suit> suit_map = {
//         {'H', HEARTS}, {'D', DIAMONDS}, {'C', CLUBS}, {'S', SPADES}
//     };

//     Rank rank;
//     Suit suit;

//     if (rank_map.find(str[0]) != rank_map.end()) {
//         rank = rank_map[str[0]];
//     } else if (rank_map.find(str[1]) != rank_map.end()) {
//         rank = rank_map[str[1]];
//     } else {
//         throw std::invalid_argument("Invalid rank");
//     }

//     if (suit_map.find(str[1]) != suit_map.end()) {
//         suit = suit_map[str[1]];
//     } else if (suit_map.find(str[0]) != suit_map.end()) {
//         suit = suit_map[str[0]];
//     } else {
//         throw std::invalid_argument("Invalid suit");
//     }

//     return {rank, suit};
// }

// // 生成剩余牌堆
// std::vector<Card> get_remaining_deck(const std::vector<Card>& excluded_cards) {
//     std::vector<Card> deck = get_deck();
//     for (const auto& card : excluded_cards) {
//         deck.erase(std::remove(deck.begin(), deck.end(), card), deck.end());
//     }
//     return deck;
// }

// // 生成所有可能的对手手牌组合
// void generate_opponent_hands(const std::vector<Card>& deck, std::vector<std::pair<Card, Card>>& opponent_hands) {
//     for (size_t i = 0; i < deck.size(); ++i) {
//         for (size_t j = i + 1; j < deck.size(); ++j) {
//             opponent_hands.push_back({deck[i], deck[j]});
//         }
//     }
// }

// // 评估手牌的强度
// int evaluate_hand_strength(const std::vector<Card>& hand) {
//     std::map<Rank, int> rank_count;
//     std::map<Suit, int> suit_count;
//     for (const Card& card : hand) {
//         rank_count[card.rank]++;
//         suit_count[card.suit]++;
//     }

//     bool is_flush = std::any_of(suit_count.begin(), suit_count.end(), [](const std::pair<Suit, int>& entry) { return entry.second >= 5; });
//     bool is_straight = false;

//     std::vector<int> ranks;
//     for (const auto& entry : rank_count) {
//         ranks.push_back(static_cast<int>(entry.first));
//     }
//     std::sort(ranks.begin(), ranks.end());

//     if (ranks.size() >= 5) {
//         for (size_t i = 0; i <= ranks.size() - 5; ++i) {
//             if (ranks[i + 4] - ranks[i] == 4) {
//                 is_straight = true;
//                 break;
//             }
//         }
//     }

//     if (is_flush && is_straight) return 8; // 同花顺
//     if (std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 4; })) return 7; // 四条
//     if (std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 3; }) &&
//         std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 2; })) return 6; // 葫芦
//     if (is_flush) return 5; // 同花
//     if (is_straight) return 4; // 顺子
//     if (std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 3; })) return 3; // 三条
//     if (std::count_if(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 2; }) == 2) return 2; // 两对
//     if (std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 2; })) return 1; // 一对

//     return 0; // 高牌
// }

// // 比较两手牌的强度，返回 1 表示 hand1 强，-1 表示 hand2 强，0 表示平局
// int compare_hands(const std::vector<Card>& hand1, const std::vector<Card>& hand2) {
//     int strength1 = evaluate_hand_strength(hand1);
//     int strength2 = evaluate_hand_strength(hand2);

//     if (strength1 > strength2) return 1;
//     if (strength1 < strength2) return -1;

//     // 如果手牌强度相同，进一步比较具体牌面
//     std::vector<int> ranks1, ranks2;
//     for (const Card& card : hand1) {
//         ranks1.push_back(static_cast<int>(card.rank));
//     }
//     for (const Card& card : hand2) {
//         ranks2.push_back(static_cast<int>(card.rank));
//     }

//     std::sort(ranks1.rbegin(), ranks1.rend());
//     std::sort(ranks2.rbegin(), ranks2.rend());

//     for (size_t i = 0; i < ranks1.size(); ++i) {
//         if (ranks1[i] > ranks2[i]) return 1;
//         if (ranks1[i] < ranks2[i]) return -1;
//     }

//     return 0; // 完全平局
// }

// // 穷举所有可能的对手手牌组合，并计算胜率
// void evaluate_hands(const Hand& my_hand, const std::vector<Card>& community_cards, const std::vector<Card>& deck, int start, int end, double& win_count, int& total_count) {
//     std::vector<std::pair<Card, Card>> opponent_hands;
//     generate_opponent_hands(deck, opponent_hands);

//     for (int i = start; i < end; ++i) {
//         const auto& opponent_hand = opponent_hands[i];
//         std::vector<Card> my_full_hand = { my_hand.card1, my_hand.card2 };
//         my_full_hand.insert(my_full_hand.end(), community_cards.begin(), community_cards.end());

//         std::vector<Card> opponent_full_hand = { opponent_hand.first, opponent_hand.second };
//         opponent_full_hand.insert(opponent_full_hand.end(), community_cards.begin(), community_cards.end());

//         int result = compare_hands(my_full_hand, opponent_full_hand);
//         if (result == 1) {
//             win_count += 1;
//         } else if (result == 0) {
//             win_count += 0.5; // 平局
//         }
//     }

//     std::lock_guard<std::mutex> guard(mtx);
//     total_count += (end - start);
// }

// int main(int argc, char* argv[]) {
//     if (argc != 6) {
//         std::cerr << "Usage: " << argv[0] << " hole_card1 hole_card2 community_card1 community_card2 community_card3\n";
//         return 1;
//     }

//     try {
//         Hand my_hand = { parse_card(argv[1]), parse_card(argv[2]) };
//         std::vector<Card> community_cards;
//         for (int i = 3; i < 6; ++i) {
//             community_cards.push_back(parse_card(argv[i]));
//         }

//         std::vector<Card> excluded_cards = { my_hand.card1, my_hand.card2 };
//         excluded_cards.insert(excluded_cards.end(), community_cards.begin(), community_cards.end());
//         std::vector<Card> remaining_deck = get_remaining_deck(excluded_cards);

//         std::vector<std::pair<Card, Card>> opponent_hands;
//         generate_opponent_hands(remaining_deck, opponent_hands);

//         int num_threads = std::thread::hardware_concurrency();
//         std::vector<std::thread> threads;
//         double win_count = 0.0;
//         int total_count = 0;
//         int block_size = opponent_hands.size() / num_threads;

//         for (int i = 0; i < num_threads; ++i) {
//             int start = i * block_size;
//             int end = (i == num_threads - 1) ? opponent_hands.size() : (i + 1) * block_size;
//             threads.push_back(std::thread(evaluate_hands, std::ref(my_hand), std::ref(community_cards), std::ref(remaining_deck), start, end, std::ref(win_count), std::ref(total_count)));
//         }

//         for (auto& t : threads) {
//             t.join();
//         }

//         double win_rate = (win_count / total_count) * 100;
//         std::cout << "Win rate: " << win_rate << "%" << std::endl;
//     } catch (const std::invalid_argument& e) {
//         std::cerr << "Error: " << e.what() << std::endl;
//         return 1;
//     }

//     return 0;
// }



// #include <iostream>
// #include <string>
// #include <vector>
// #include <algorithm>
// #include <map>
// #include <unordered_map>

// enum Rank {
//     TWO = 2, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE
// };

// enum Suit {
//     HEARTS, DIAMONDS, CLUBS, SPADES
// };

// struct Card {
//     Rank rank;
//     Suit suit;
// };

// struct Hand {
//     Card card1;
//     Card card2;
// };

// bool operator==(const Card& lhs, const Card& rhs) {
//     return lhs.rank == rhs.rank && lhs.suit == rhs.suit;
// }

// std::vector<Card> get_deck() {
//     std::vector<Card> deck;
//     for (int r = TWO; r <= ACE; ++r) {
//         for (int s = HEARTS; s <= SPADES; ++s) {
//             deck.push_back(Card{static_cast<Rank>(r), static_cast<Suit>(s)});
//         }
//     }
//     return deck;
// }

// std::string card_to_string(const Card& card) {
//     std::string str;
//     switch (card.rank) {
//         case TWO: str += '2'; break;
//         case THREE: str += '3'; break;
//         case FOUR: str += '4'; break;
//         case FIVE: str += '5'; break;
//         case SIX: str += '6'; break;
//         case SEVEN: str += '7'; break;
//         case EIGHT: str += '8'; break;
//         case NINE: str += '9'; break;
//         case TEN: str += 'T'; break;
//         case JACK: str += 'J'; break;
//         case QUEEN: str += 'Q'; break;
//         case KING: str += 'K'; break;
//         case ACE: str += 'A'; break;
//     }
//     switch (card.suit) {
//         case HEARTS: str += 'H'; break;
//         case DIAMONDS: str += 'D'; break;
//         case CLUBS: str += 'C'; break;
//         case SPADES: str += 'S'; break;
//     }
//     return str;
// }

// Card parse_card(const std::string& str) {
//     static std::unordered_map<char, Rank> rank_map = {
//         {'2', TWO}, {'3', THREE}, {'4', FOUR}, {'5', FIVE}, {'6', SIX},
//         {'7', SEVEN}, {'8', EIGHT}, {'9', NINE}, {'T', TEN},
//         {'J', JACK}, {'Q', QUEEN}, {'K', KING}, {'A', ACE}
//     };

//     static std::unordered_map<char, Suit> suit_map = {
//         {'H', HEARTS}, {'D', DIAMONDS}, {'C', CLUBS}, {'S', SPADES}
//     };

//     Rank rank;
//     Suit suit;

//     if (rank_map.find(str[0]) != rank_map.end()) {
//         rank = rank_map[str[0]];
//     } else if (rank_map.find(str[1]) != rank_map.end()) {
//         rank = rank_map[str[1]];
//     } else {
//         throw std::invalid_argument("Invalid rank");
//     }

//     if (suit_map.find(str[1]) != suit_map.end()) {
//         suit = suit_map[str[1]];
//     } else if (suit_map.find(str[0]) != suit_map.end()) {
//         suit = suit_map[str[0]];
//     } else {
//         throw std::invalid_argument("Invalid suit");
//     }

//     return {rank, suit};
// }

// // 生成剩余牌堆
// std::vector<Card> get_remaining_deck(const std::vector<Card>& excluded_cards) {
//     std::vector<Card> deck = get_deck();
//     for (const auto& card : excluded_cards) {
//         deck.erase(std::remove(deck.begin(), deck.end(), card), deck.end());
//     }
//     return deck;
// }

// // 生成所有可能的对手手牌组合
// std::vector<std::pair<Card, Card>> generate_opponent_hands(const std::vector<Card>& deck) {
//     std::vector<std::pair<Card, Card>> opponent_hands;
//     for (size_t i = 0; i < deck.size(); ++i) {
//         for (size_t j = i + 1; j < deck.size(); ++j) {
//             opponent_hands.push_back({deck[i], deck[j]});
//         }
//     }
//     return opponent_hands;
// }

// // 评估手牌的强度
// int evaluate_hand_strength(const std::vector<Card>& hand) {
//     std::map<Rank, int> rank_count;
//     std::map<Suit, int> suit_count;
//     for (const Card& card : hand) {
//         rank_count[card.rank]++;
//         suit_count[card.suit]++;
//     }

//     bool is_flush = std::any_of(suit_count.begin(), suit_count.end(), [](const std::pair<Suit, int>& entry) { return entry.second >= 5; });
//     bool is_straight = false;

//     std::vector<int> ranks;
//     for (const auto& entry : rank_count) {
//         ranks.push_back(static_cast<int>(entry.first));
//     }
//     std::sort(ranks.begin(), ranks.end());

//     if (ranks.size() >= 5) {
//         for (size_t i = 0; i <= ranks.size() - 5; ++i) {
//             if (ranks[i + 4] - ranks[i] == 4) {
//                 is_straight = true;
//                 break;
//             }
//         }
//     }

//     if (is_flush && is_straight) return 8; // 同花顺
//     if (std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 4; })) return 7; // 四条
//     if (std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 3; }) &&
//         std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 2; })) return 6; // 葫芦
//     if (is_flush) return 5; // 同花
//     if (is_straight) return 4; // 顺子
//     if (std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 3; })) return 3; // 三条
//     if (std::count_if(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 2; }) == 2) return 2; // 两对
//     if (std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 2; })) return 1; // 一对

//     return 0; // 高牌
// }

// // 比较两手牌的强度，返回 1 表示 hand1 强，-1 表示 hand2 强，0 表示平局
// int compare_hands(const std::vector<Card>& hand1, const std::vector<Card>& hand2) {
//     int strength1 = evaluate_hand_strength(hand1);
//     int strength2 = evaluate_hand_strength(hand2);

//     if (strength1 > strength2) return 1;
//     if (strength1 < strength2) return -1;

//     // 如果手牌强度相同，进一步比较具体牌面
//     std::vector<int> ranks1, ranks2;
//     for (const Card& card : hand1) {
//         ranks1.push_back(static_cast<int>(card.rank));
//     }
//     for (const Card& card : hand2) {
//         ranks2.push_back(static_cast<int>(card.rank));
//     }

//     std::sort(ranks1.rbegin(), ranks1.rend());
//     std::sort(ranks2.rbegin(), ranks2.rend());

//     for (size_t i = 0; i < ranks1.size(); ++i) {
//         if (ranks1[i] > ranks2[i]) return 1;
//         if (ranks1[i] < ranks2[i]) return -1;
//     }

//     return 0; // 完全平局
// }

// // 计算胜率
// double calculate_win_rate(const Hand& my_hand, const std::vector<Card>& community_cards, const std::vector<Card>& deck) {
//     std::vector<std::pair<Card, Card>> opponent_hands = generate_opponent_hands(deck);
//     double win_count = 0.0;
//     int total_count = opponent_hands.size();

//     for (const auto& opponent_hand : opponent_hands) {
//         std::vector<Card> my_full_hand = { my_hand.card1, my_hand.card2 };
//         my_full_hand.insert(my_full_hand.end(), community_cards.begin(), community_cards.end());

//         std::vector<Card> opponent_full_hand = { opponent_hand.first, opponent_hand.second };
//         opponent_full_hand.insert(opponent_full_hand.end(), community_cards.begin(), community_cards.end());

//         int result = compare_hands(my_full_hand, opponent_full_hand);
//         if (result == 1) {
//             win_count += 1;
//         } else if (result == 0) {
//             win_count += 0.5; // 平局
//         }
//     }

//     return (win_count / total_count) * 100;
// }

// int main(int argc, char* argv[]) {
//     if (argc != 6) {
//         std::cerr << "Usage: " << argv[0] << " hole_card1 hole_card2 community_card1 community_card2 community_card3\n";
//         return 1;
//     }

//     try {
//         Hand my_hand = { parse_card(argv[1]), parse_card(argv[2]) };
//         std::vector<Card> community_cards;
//         for (int i = 3; i < 6; ++i) {
//             community_cards.push_back(parse_card(argv[i]));
//         }

//         std::vector<Card> excluded_cards = { my_hand.card1, my_hand.card2 };
//         excluded_cards.insert(excluded_cards.end(), community_cards.begin(), community_cards.end());
//         std::vector<Card> remaining_deck = get_remaining_deck(excluded_cards);

//         double win_rate = calculate_win_rate(my_hand, community_cards, remaining_deck);
//         std::cout << "Win rate: " << win_rate << "%" << std::endl;
//     } catch (const std::invalid_argument& e) {
//         std::cerr << "Error: " << e.what() << std::endl;
//         return 1;
//     }

//     return 0;
// }



// #include <iostream>
// #include <string>
// #include <vector>
// #include <algorithm>
// #include <map>
// #include <unordered_map>
// #include <set>

// enum Rank {
//     TWO = 2, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE
// };

// enum Suit {
//     HEARTS, DIAMONDS, CLUBS, SPADES
// };

// struct Card {
//     Rank rank;
//     Suit suit;
// };

// struct Hand {
//     Card card1;
//     Card card2;
// };

// bool operator==(const Card& lhs, const Card& rhs) {
//     return lhs.rank == rhs.rank && lhs.suit == rhs.suit;
// }

// std::vector<Card> get_deck() {
//     std::vector<Card> deck;
//     for (int r = TWO; r <= ACE; ++r) {
//         for (int s = HEARTS; s <= SPADES; ++s) {
//             deck.push_back(Card{static_cast<Rank>(r), static_cast<Suit>(s)});
//         }
//     }
//     return deck;
// }

// std::string card_to_string(const Card& card) {
//     std::string str;
//     switch (card.rank) {
//         case TWO: str += '2'; break;
//         case THREE: str += '3'; break;
//         case FOUR: str += '4'; break;
//         case FIVE: str += '5'; break;
//         case SIX: str += '6'; break;
//         case SEVEN: str += '7'; break;
//         case EIGHT: str += '8'; break;
//         case NINE: str += '9'; break;
//         case TEN: str += 'T'; break;
//         case JACK: str += 'J'; break;
//         case QUEEN: str += 'Q'; break;
//         case KING: str += 'K'; break;
//         case ACE: str += 'A'; break;
//     }
//     switch (card.suit) {
//         case HEARTS: str += 'H'; break;
//         case DIAMONDS: str += 'D'; break;
//         case CLUBS: str += 'C'; break;
//         case SPADES: str += 'S'; break;
//     }
//     return str;
// }

// Card parse_card(const std::string& str) {
//     static std::unordered_map<char, Rank> rank_map = {
//         {'2', TWO}, {'3', THREE}, {'4', FOUR}, {'5', FIVE}, {'6', SIX},
//         {'7', SEVEN}, {'8', EIGHT}, {'9', NINE}, {'T', TEN},
//         {'J', JACK}, {'Q', QUEEN}, {'K', KING}, {'A', ACE}
//     };

//     static std::unordered_map<char, Suit> suit_map = {
//         {'H', HEARTS}, {'D', DIAMONDS}, {'C', CLUBS}, {'S', SPADES}
//     };

//     Rank rank;
//     Suit suit;

//     if (rank_map.find(str[0]) != rank_map.end()) {
//         rank = rank_map[str[0]];
//     } else if (rank_map.find(str[1]) != rank_map.end()) {
//         rank = rank_map[str[1]];
//     } else {
//         throw std::invalid_argument("Invalid rank");
//     }

//     if (suit_map.find(str[1]) != suit_map.end()) {
//         suit = suit_map[str[1]];
//     } else if (suit_map.find(str[0]) != suit_map.end()) {
//         suit = suit_map[str[0]];
//     } else {
//         throw std::invalid_argument("Invalid suit");
//     }

//     return {rank, suit};
// }

// // 生成剩余牌堆
// std::vector<Card> get_remaining_deck(const std::vector<Card>& excluded_cards) {
//     std::vector<Card> deck = get_deck();
//     for (const auto& card : excluded_cards) {
//         deck.erase(std::remove(deck.begin(), deck.end(), card), deck.end());
//     }
//     return deck;
// }

// // 生成所有可能的对手手牌组合
// std::vector<std::pair<Card, Card>> generate_opponent_hands(const std::vector<Card>& deck) {
//     std::vector<std::pair<Card, Card>> opponent_hands;
//     for (size_t i = 0; i < deck.size(); ++i) {
//         for (size_t j = i + 1; j < deck.size(); ++j) {
//             opponent_hands.push_back({deck[i], deck[j]});
//         }
//     }
//     return opponent_hands;
// }

// bool is_straight(const std::set<int>& ranks) {
//     if (ranks.size() < 5) return false;
//     auto it = ranks.begin();
//     auto next = std::next(it);
//     int count = 1;
//     while (next != ranks.end()) {
//         if (*next - *it == 1) {
//             count++;
//             if (count == 5) return true;
//         } else {
//             count = 1;
//         }
//         it++;
//         next++;
//     }
//     return false;
// }

// // 评估手牌的强度
// int evaluate_hand_strength(const std::vector<Card>& hand) {
//     std::map<Rank, int> rank_count;
//     std::map<Suit, int> suit_count;
//     for (const Card& card : hand) {
//         rank_count[card.rank]++;
//         suit_count[card.suit]++;
//     }

//     bool is_flush = std::any_of(suit_count.begin(), suit_count.end(), [](const std::pair<Suit, int>& entry) { return entry.second >= 5; });
//     std::set<int> ranks;
//     for (const auto& entry : rank_count) {
//         ranks.insert(static_cast<int>(entry.first));
//     }
//     bool is_straight_hand = is_straight(ranks);

//     if (is_flush && is_straight_hand) return 8; // 同花顺
//     if (std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 4; })) return 7; // 四条
//     if (std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 3; }) &&
//         std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 2; })) return 6; // 葫芦
//     if (is_flush) return 5; // 同花
//     if (is_straight_hand) return 4; // 顺子
//     if (std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 3; })) return 3; // 三条
//     if (std::count_if(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 2; }) == 2) return 2; // 两对
//     if (std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 2; })) return 1; // 一对

//     return 0; // 高牌
// }

// // 比较两手牌的强度，返回 1 表示 hand1 强，-1 表示 hand2 强，0 表示平局
// int compare_hands(const std::vector<Card>& hand1, const std::vector<Card>& hand2) {
//     int strength1 = evaluate_hand_strength(hand1);
//     int strength2 = evaluate_hand_strength(hand2);

//     if (strength1 > strength2) return 1;
//     if (strength1 < strength2) return -1;

//     // 如果手牌强度相同，进一步比较具体牌面
//     std::vector<int> ranks1, ranks2;
//     for (const Card& card : hand1) {
//         ranks1.push_back(static_cast<int>(card.rank));
//     }
//     for (const Card& card : hand2) {
//         ranks2.push_back(static_cast<int>(card.rank));
//     }

//     std::sort(ranks1.rbegin(), ranks1.rend());
//     std::sort(ranks2.rbegin(), ranks2.rend());

//     for (size_t i = 0; i < ranks1.size(); ++i) {
//         if (ranks1[i] > ranks2[i]) return 1;
//         if (ranks1[i] < ranks2[i]) return -1;
//     }

//     return 0; // 完全平局
// }

// // 计算胜率
// double calculate_win_rate(const Hand& my_hand, const std::vector<Card>& community_cards, const std::vector<Card>& deck) {
//     std::vector<std::pair<Card, Card>> opponent_hands = generate_opponent_hands(deck);
//     double win_count = 0.0;
//     int total_count = opponent_hands.size();

//     for (const auto& opponent_hand : opponent_hands) {
//         std::vector<Card> my_full_hand = { my_hand.card1, my_hand.card2 };
//         my_full_hand.insert(my_full_hand.end(), community_cards.begin(), community_cards.end());

//         std::vector<Card> opponent_full_hand = { opponent_hand.first, opponent_hand.second };
//         opponent_full_hand.insert(opponent_full_hand.end(), community_cards.begin(), community_cards.end());

//         int result = compare_hands(my_full_hand, opponent_full_hand);
//         if (result == 1) {
//             win_count += 1;
//         } else if (result == 0) {
//             win_count += 0.5; // 平局
//         }
//     }

//     return (win_count / total_count) * 100;
// }

// int main(int argc, char* argv[]) {
//     if (argc != 6) {
//         std::cerr << "Usage: " << argv[0] << " hole_card1 hole_card2 community_card1 community_card2 community_card3\n";
//         return 1;
//     }

//     try {
//         Hand my_hand = { parse_card(argv[1]), parse_card(argv[2]) };
//         std::vector<Card> community_cards;
//         for (int i = 3; i < 6; ++i) {
//             community_cards.push_back(parse_card(argv[i]));
//         }

//         std::vector<Card> excluded_cards = { my_hand.card1, my_hand.card2 };
//         excluded_cards.insert(excluded_cards.end(), community_cards.begin(), community_cards.end());
//         std::vector<Card> remaining_deck = get_remaining_deck(excluded_cards);

//         double win_rate = calculate_win_rate(my_hand, community_cards, remaining_deck);
//         std::cout << "Win rate: " << win_rate << "%" << std::endl;
//     } catch (const std::invalid_argument& e) {
//         std::cerr << "Error: " << e.what() << std::endl;
//         return 1;
//     }

//     return 0;
// }


// single thread for all the combinations --> run about 30s
// #include <iostream>
// #include <string>
// #include <vector>
// #include <algorithm>
// #include <map>
// #include <unordered_map>
// #include <set>

// enum Rank {
//     TWO = 2, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE
// };

// enum Suit {
//     HEARTS, DIAMONDS, CLUBS, SPADES
// };

// struct Card {
//     Rank rank;
//     Suit suit;
// };

// struct Hand {
//     Card card1;
//     Card card2;
// };

// bool operator==(const Card& lhs, const Card& rhs) {
//     return lhs.rank == rhs.rank && lhs.suit == rhs.suit;
// }

// std::vector<Card> get_deck() {
//     std::vector<Card> deck;
//     for (int r = TWO; r <= ACE; ++r) {
//         for (int s = HEARTS; s <= SPADES; ++s) {
//             deck.push_back(Card{static_cast<Rank>(r), static_cast<Suit>(s)});
//         }
//     }
//     return deck;
// }

// std::string card_to_string(const Card& card) {
//     std::string str;
//     switch (card.rank) {
//         case TWO: str += '2'; break;
//         case THREE: str += '3'; break;
//         case FOUR: str += '4'; break;
//         case FIVE: str += '5'; break;
//         case SIX: str += '6'; break;
//         case SEVEN: str += '7'; break;
//         case EIGHT: str += '8'; break;
//         case NINE: str += '9'; break;
//         case TEN: str += 'T'; break;
//         case JACK: str += 'J'; break;
//         case QUEEN: str += 'Q'; break;
//         case KING: str += 'K'; break;
//         case ACE: str += 'A'; break;
//     }
//     switch (card.suit) {
//         case HEARTS: str += 'H'; break;
//         case DIAMONDS: str += 'D'; break;
//         case CLUBS: str += 'C'; break;
//         case SPADES: str += 'S'; break;
//     }
//     return str;
// }

// Card parse_card(const std::string& str) {
//     static std::unordered_map<char, Rank> rank_map = {
//         {'2', TWO}, {'3', THREE}, {'4', FOUR}, {'5', FIVE}, {'6', SIX},
//         {'7', SEVEN}, {'8', EIGHT}, {'9', NINE}, {'T', TEN},
//         {'J', JACK}, {'Q', QUEEN}, {'K', KING}, {'A', ACE}
//     };

//     static std::unordered_map<char, Suit> suit_map = {
//         {'H', HEARTS}, {'D', DIAMONDS}, {'C', CLUBS}, {'S', SPADES}
//     };

//     Rank rank;
//     Suit suit;

//     if (rank_map.find(str[0]) != rank_map.end()) {
//         rank = rank_map[str[0]];
//     } else if (rank_map.find(str[1]) != rank_map.end()) {
//         rank = rank_map[str[1]];
//     } else {
//         throw std::invalid_argument("Invalid rank");
//     }

//     if (suit_map.find(str[1]) != suit_map.end()) {
//         suit = suit_map[str[1]];
//     } else if (suit_map.find(str[0]) != suit_map.end()) {
//         suit = suit_map[str[0]];
//     } else {
//         throw std::invalid_argument("Invalid suit");
//     }

//     return {rank, suit};
// }

// // 生成剩余牌堆
// std::vector<Card> get_remaining_deck(const std::vector<Card>& excluded_cards) {
//     std::vector<Card> deck = get_deck();
//     for (const auto& card : excluded_cards) {
//         deck.erase(std::remove(deck.begin(), deck.end(), card), deck.end());
//     }
//     return deck;
// }

// // 生成所有可能的对手手牌组合
// std::vector<std::pair<Card, Card>> generate_opponent_hands(const std::vector<Card>& deck) {
//     std::vector<std::pair<Card, Card>> opponent_hands;
//     for (size_t i = 0; i < deck.size(); ++i) {
//         for (size_t j = i + 1; j < deck.size(); ++j) {
//             opponent_hands.push_back({deck[i], deck[j]});
//         }
//     }
//     return opponent_hands;
// }

// bool is_straight(const std::set<int>& ranks) {
//     if (ranks.size() < 5) return false;
//     auto it = ranks.begin();
//     auto next = std::next(it);
//     int count = 1;
//     while (next != ranks.end()) {
//         if (*next - *it == 1) {
//             count++;
//             if (count == 5) return true;
//         } else {
//             count = 1;
//         }
//         it++;
//         next++;
//     }
//     return false;
// }

// // 评估手牌的强度
// int evaluate_hand_strength(const std::vector<Card>& hand) {
//     std::map<Rank, int> rank_count;
//     std::map<Suit, int> suit_count;
//     for (const Card& card : hand) {
//         rank_count[card.rank]++;
//         suit_count[card.suit]++;
//     }

//     bool is_flush = std::any_of(suit_count.begin(), suit_count.end(), [](const std::pair<Suit, int>& entry) { return entry.second >= 5; });
//     std::set<int> ranks;
//     for (const auto& entry : rank_count) {
//         ranks.insert(static_cast<int>(entry.first));
//     }
//     bool is_straight_hand = is_straight(ranks);

//     if (is_flush && is_straight_hand) return 8; // 同花顺
//     if (std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 4; })) return 7; // 四条
//     if (std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 3; }) &&
//         std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 2; })) return 6; // 葫芦
//     if (is_flush) return 5; // 同花
//     if (is_straight_hand) return 4; // 顺子
//     if (std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 3; })) return 3; // 三条
//     if (std::count_if(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 2; }) == 2) return 2; // 两对
//     if (std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 2; })) return 1; // 一对

//     return 0; // 高牌
// }

// // 比较两手牌的强度，返回 1 表示 hand1 强，-1 表示 hand2 强，0 表示平局
// int compare_hands(const std::vector<Card>& hand1, const std::vector<Card>& hand2) {
//     int strength1 = evaluate_hand_strength(hand1);
//     int strength2 = evaluate_hand_strength(hand2);

//     if (strength1 > strength2) return 1;
//     if (strength1 < strength2) return -1;

//     // 如果手牌强度相同，进一步比较具体牌面
//     std::vector<int> ranks1, ranks2;
//     for (const Card& card : hand1) {
//         ranks1.push_back(static_cast<int>(card.rank));
//     }
//     for (const Card& card : hand2) {
//         ranks2.push_back(static_cast<int>(card.rank));
//     }

//     std::sort(ranks1.rbegin(), ranks1.rend());
//     std::sort(ranks2.rbegin(), ranks2.rend());

//     for (size_t i = 0; i < ranks1.size(); ++i) {
//         if (ranks1[i] > ranks2[i]) return 1;
//         if (ranks1[i] < ranks2[i]) return -1;
//     }

//     return 0; // 完全平局
// }

// // 计算胜率
// double calculate_win_rate(const Hand& my_hand, const std::vector<Card>& community_cards, const std::vector<Card>& deck) {
//     std::vector<std::pair<Card, Card>> opponent_hands = generate_opponent_hands(deck);
//     double win_count = 0.0;
//     int total_count = 0;

//     for (const auto& opponent_hand : opponent_hands) {
//         for (size_t i = 0; i < deck.size(); ++i) {
//             for (size_t j = i + 1; j < deck.size(); ++j) {
//                 std::vector<Card> remaining_cards = deck;
//                 remaining_cards.erase(std::remove(remaining_cards.begin(), remaining_cards.end(), opponent_hand.first), remaining_cards.end());
//                 remaining_cards.erase(std::remove(remaining_cards.begin(), remaining_cards.end(), opponent_hand.second), remaining_cards.end());
//                 remaining_cards.erase(std::remove(remaining_cards.begin(), remaining_cards.end(), deck[i]), remaining_cards.end());
//                 remaining_cards.erase(std::remove(remaining_cards.begin(), remaining_cards.end(), deck[j]), remaining_cards.end());

//                 std::vector<Card> my_full_hand = { my_hand.card1, my_hand.card2 };
//                 my_full_hand.insert(my_full_hand.end(), community_cards.begin(), community_cards.end());
//                 my_full_hand.push_back(deck[i]);
//                 my_full_hand.push_back(deck[j]);

//                 std::vector<Card> opponent_full_hand = { opponent_hand.first, opponent_hand.second };
//                 opponent_full_hand.insert(opponent_full_hand.end(), community_cards.begin(), community_cards.end());
//                 opponent_full_hand.push_back(deck[i]);
//                 opponent_full_hand.push_back(deck[j]);

//                 int result = compare_hands(my_full_hand, opponent_full_hand);
//                 if (result == 1) {
//                     win_count += 1;
//                 } else if (result == 0) {
//                     win_count += 0.5; // 平局
//                 }
//                 total_count += 1;
//             }
//         }
//     }

//     return (win_count / total_count) * 100;
// }

// int main(int argc, char* argv[]) {
//     if (argc != 6) {
//         std::cerr << "Usage: " << argv[0] << " hole_card1 hole_card2 community_card1 community_card2 community_card3\n";
//         return 1;
//     }

//     try {
//         Hand my_hand = { parse_card(argv[1]), parse_card(argv[2]) };
//         std::vector<Card> community_cards;
//         for (int i = 3; i < 6; ++i) {
//             community_cards.push_back(parse_card(argv[i]));
//         }

//         std::vector<Card> excluded_cards = { my_hand.card1, my_hand.card2 };
//         excluded_cards.insert(excluded_cards.end(), community_cards.begin(), community_cards.end());
//         std::vector<Card> remaining_deck = get_remaining_deck(excluded_cards);

//         double win_rate = calculate_win_rate(my_hand, community_cards, remaining_deck);
//         std::cout << "Win rate: " << win_rate << "%" << std::endl;
//     } catch (const std::invalid_argument& e) {
//         std::cerr << "Error: " << e.what() << std::endl;
//         return 1;
//     }

//     return 0;
// }


#include <iostream>
#include <vector>
#include <thread>
#include <mutex>
#include <algorithm>
#include <map>
#include <unordered_map>
#include <set>

enum Rank {
    TWO = 2, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE
};

enum Suit {
    HEARTS, DIAMONDS, CLUBS, SPADES
};

struct Card {
    Rank rank;
    Suit suit;
};

struct Hand {
    Card card1;
    Card card2;
};

bool operator==(const Card& lhs, const Card& rhs) {
    return lhs.rank == rhs.rank && lhs.suit == rhs.suit;
}

std::vector<Card> get_deck() {
    std::vector<Card> deck;
    for (int r = TWO; r <= ACE; ++r) {
        for (int s = HEARTS; s <= SPADES; ++s) {
            deck.push_back(Card{static_cast<Rank>(r), static_cast<Suit>(s)});
        }
    }
    return deck;
}

Card parse_card(const std::string& str) {
    static std::unordered_map<char, Rank> rank_map = {
        {'2', TWO}, {'3', THREE}, {'4', FOUR}, {'5', FIVE}, {'6', SIX},
        {'7', SEVEN}, {'8', EIGHT}, {'9', NINE}, {'T', TEN},
        {'J', JACK}, {'Q', QUEEN}, {'K', KING}, {'A', ACE}
    };

    static std::unordered_map<char, Suit> suit_map = {
        {'H', HEARTS}, {'D', DIAMONDS}, {'C', CLUBS}, {'S', SPADES}
    };

    Rank rank;
    Suit suit;

    if (rank_map.find(str[0]) != rank_map.end()) {
        rank = rank_map[str[0]];
    } else if (rank_map.find(str[1]) != rank_map.end()) {
        rank = rank_map[str[1]];
    } else {
        throw std::invalid_argument("Invalid rank");
    }

    if (suit_map.find(str[1]) != suit_map.end()) {
        suit = suit_map[str[1]];
    } else if (suit_map.find(str[0]) != suit_map.end()) {
        suit = suit_map[str[0]];
    } else {
        throw std::invalid_argument("Invalid suit");
    }

    return {rank, suit};
}

// 生成剩余牌堆
std::vector<Card> get_remaining_deck(const std::vector<Card>& excluded_cards) {
    std::vector<Card> deck = get_deck();
    for (const auto& card : excluded_cards) {
        deck.erase(std::remove(deck.begin(), deck.end(), card), deck.end());
    }
    return deck;
}

// 生成所有可能的对手手牌组合
std::vector<std::pair<Card, Card>> generate_opponent_hands(const std::vector<Card>& deck) {
    std::vector<std::pair<Card, Card>> opponent_hands;
    for (size_t i = 0; i < deck.size(); ++i) {
        for (size_t j = i + 1; j < deck.size(); ++j) {
            opponent_hands.push_back({deck[i], deck[j]});
        }
    }
    return opponent_hands;
}

bool is_straight(const std::set<int>& ranks) {
    if (ranks.size() < 5) return false;
    auto it = ranks.begin();
    auto next = std::next(it);
    int count = 1;
    while (next != ranks.end()) {
        if (*next - *it == 1) {
            count++;
            if (count == 5) return true;
        } else {
            count = 1;
        }
        it++;
        next++;
    }
    return false;
}

// 评估手牌的强度
int evaluate_hand_strength(const std::vector<Card>& hand) {
    std::map<Rank, int> rank_count;
    std::map<Suit, int> suit_count;
    for (const Card& card : hand) {
        rank_count[card.rank]++;
        suit_count[card.suit]++;
    }

    bool is_flush = std::any_of(suit_count.begin(), suit_count.end(), [](const std::pair<Suit, int>& entry) { return entry.second >= 5; });
    std::set<int> ranks;
    for (const auto& entry : rank_count) {
        ranks.insert(static_cast<int>(entry.first));
    }
    bool is_straight_hand = is_straight(ranks);

    if (is_flush && is_straight_hand) return 8; // 同花顺
    if (std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 4; })) return 7; // 四条
    if (std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 3; }) &&
        std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 2; })) return 6; // 葫芦
    if (is_flush) return 5; // 同花
    if (is_straight_hand) return 4; // 顺子
    if (std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 3; })) return 3; // 三条
    if (std::count_if(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 2; }) == 2) return 2; // 两对
    if (std::any_of(rank_count.begin(), rank_count.end(), [](const std::pair<Rank, int>& entry) { return entry.second == 2; })) return 1; // 一对

    return 0; // 高牌
}

// 比较两手牌的强度，返回 1 表示 hand1 强，-1 表示 hand2 强，0 表示平局
int compare_hands(const std::vector<Card>& hand1, const std::vector<Card>& hand2) {
    int strength1 = evaluate_hand_strength(hand1);
    int strength2 = evaluate_hand_strength(hand2);

    if (strength1 > strength2) return 1;
    if (strength1 < strength2) return -1;

    // 如果手牌强度相同，进一步比较具体牌面
    std::vector<int> ranks1, ranks2;
    for (const Card& card : hand1) {
        ranks1.push_back(static_cast<int>(card.rank));
    }
    for (const Card& card : hand2) {
        ranks2.push_back(static_cast<int>(card.rank));
    }

    std::sort(ranks1.rbegin(), ranks1.rend());
    std::sort(ranks2.rbegin(), ranks2.rend());

    for (size_t i = 0; i < ranks1.size(); ++i) {
        if (ranks1[i] > ranks2[i]) return 1;
        if (ranks1[i] < ranks2[i]) return -1;
    }

    return 0; // 完全平局
}

void evaluate_hands(const Hand& my_hand, const std::vector<Card>& community_cards, const std::vector<Card>& remaining_deck,
                    int start, int end, double& win_count, int& total_count, std::mutex& mtx) {
    std::vector<std::pair<Card, Card>> opponent_hands = generate_opponent_hands(remaining_deck);
    for (int i = start; i < end; ++i) {
        const auto& opponent_hand = opponent_hands[i];
        for (size_t j = 0; j < remaining_deck.size(); ++j) {
            for (size_t k = j + 1; k < remaining_deck.size(); ++k) {
                std::vector<Card> deck = remaining_deck;
                deck.erase(std::remove(deck.begin(), deck.end(), opponent_hand.first), deck.end());
                deck.erase(std::remove(deck.begin(), deck.end(), opponent_hand.second), deck.end());
                deck.erase(std::remove(deck.begin(), deck.end(), remaining_deck[j]), deck.end());
                deck.erase(std::remove(deck.begin(), deck.end(), remaining_deck[k]), deck.end());

                std::vector<Card> my_full_hand = { my_hand.card1, my_hand.card2 };
                my_full_hand.insert(my_full_hand.end(), community_cards.begin(), community_cards.end());
                my_full_hand.push_back(remaining_deck[j]);
                my_full_hand.push_back(remaining_deck[k]);

                std::vector<Card> opponent_full_hand = { opponent_hand.first, opponent_hand.second };
                opponent_full_hand.insert(opponent_full_hand.end(), community_cards.begin(), community_cards.end());
                opponent_full_hand.push_back(remaining_deck[j]);
                opponent_full_hand.push_back(remaining_deck[k]);

                int result = compare_hands(my_full_hand, opponent_full_hand);
                std::lock_guard<std::mutex> lock(mtx);
                if (result == 1) {
                    win_count += 1;
                } else if (result == 0) {
                    win_count += 0.5; // 平局
                }
                total_count += 1;
            }
        }
    }
}

double calculate_win_rate(const Hand& my_hand, const std::vector<Card>& community_cards, const std::vector<Card>& remaining_deck) {
    int num_threads = std::thread::hardware_concurrency();
    int num_opponent_hands = generate_opponent_hands(remaining_deck).size();
    int block_size = num_opponent_hands / num_threads;

    // std::cout << "Number of threads: " << num_threads << std::endl;
    // std::cout << "Number of opponent hands: " << num_opponent_hands << std::endl;
    // std::cout << "Block size: " << block_size << std::endl;
    std::cout << std::endl;

    std::vector<std::thread> threads;
    std::vector<double> win_counts(num_threads, 0);
    std::vector<int> total_counts(num_threads, 0);
    std::mutex mtx;

    for (int i = 0; i < num_threads; ++i) {
        int start = i * block_size;
        int end = (i == num_threads - 1) ? num_opponent_hands : start + block_size;
        threads.emplace_back(evaluate_hands, std::ref(my_hand), std::ref(community_cards), std::ref(remaining_deck),
                             start, end, std::ref(win_counts[i]), std::ref(total_counts[i]), std::ref(mtx));
    }

    for (auto& thread : threads) {
        thread.join();
    }

    double total_win_count = 0;
    int total_count = 0;
    for (int i = 0; i < num_threads; ++i) {
        total_win_count += win_counts[i];
        total_count += total_counts[i];
    }

    return (total_win_count / total_count) * 100;
}

int main(int argc, char* argv[]) {
    if (argc != 6) {
        std::cerr << "Usage: " << argv[0] << " hole_card1 hole_card2 community_card1 community_card2 community_card3\n";
        return 1;
    }

    try {
        Hand my_hand = { parse_card(argv[1]), parse_card(argv[2]) };
        std::vector<Card> community_cards;
        for (int i = 3; i < 6; ++i) {
            community_cards.push_back(parse_card(argv[i]));
        }

        std::vector<Card> excluded_cards = { my_hand.card1, my_hand.card2 };
        excluded_cards.insert(excluded_cards.end(), community_cards.begin(), community_cards.end());
        std::vector<Card> remaining_deck = get_remaining_deck(excluded_cards);

        double win_rate = calculate_win_rate(my_hand, community_cards, remaining_deck);
        std::cout << "Win rate: " << win_rate << "%" << std::endl;
    } catch (const std::invalid_argument& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
