# Readme for final_project folder

- how to create the table:
```bash
g++ -std=c++11 -I. make_table.cpp -o make_table
./make_table
```

- If wanna run the evaluator in multi-thread:
```bash
g++ -std=c++11 evaluator.cpp -o evaluator -pthread
./evaluator
```