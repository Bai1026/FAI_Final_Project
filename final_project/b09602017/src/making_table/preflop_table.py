import json
import pickle

data = {
    "winning_table": [
        {"hand": "A/A/u", "win": 84.93, "lose": 14.52, "tie": 0.54, "expected_value": 70.41, "additional_chance": 0.45},
        {"hand": "K/K/u", "win": 82.12, "lose": 17.33, "tie": 0.56, "expected_value": 64.79, "additional_chance": 0.90},
        {"hand": "Q/Q/u", "win": 79.63, "lose": 19.78, "tie": 0.59, "expected_value": 59.85, "additional_chance": 1.36},
        {"hand": "J/J/u", "win": 77.15, "lose": 22.21, "tie": 0.63, "expected_value": 54.94, "additional_chance": 1.81},
        {"hand": "10/10/u", "win": 74.66, "lose": 24.64, "tie": 0.70, "expected_value": 50.02, "additional_chance": 2.26},
        {"hand": "9/9/u", "win": 71.67, "lose": 27.55, "tie": 0.78, "expected_value": 44.11, "additional_chance": 2.71},
        {"hand": "8/8/u", "win": 68.72, "lose": 30.39, "tie": 0.89, "expected_value": 38.33, "additional_chance": 3.17},
        {"hand": "K/A/s", "win": 66.22, "lose": 32.13, "tie": 1.65, "expected_value": 34.09, "additional_chance": 3.47},
        {"hand": "7/7/u", "win": 65.73, "lose": 33.25, "tie": 1.02, "expected_value": 32.47, "additional_chance": 3.92},
        {"hand": "Q/A/s", "win": 65.31, "lose": 32.90, "tie": 1.79, "expected_value": 32.42, "additional_chance": 4.22},
        {"hand": "J/A/s", "win": 64.40, "lose": 33.61, "tie": 1.99, "expected_value": 30.79, "additional_chance": 4.52},
        {"hand": "K/A/u", "win": 64.47, "lose": 33.83, "tie": 1.70, "expected_value": 30.64, "additional_chance": 5.43},
        {"hand": "10/A/s", "win": 63.49, "lose": 34.28, "tie": 2.23, "expected_value": 29.20, "additional_chance": 5.73},
        {"hand": "Q/A/u", "win": 63.51, "lose": 34.65, "tie": 1.85, "expected_value": 28.86, "additional_chance": 6.64},
        {"hand": "J/A/u", "win": 62.54, "lose": 35.41, "tie": 2.06, "expected_value": 27.13, "additional_chance": 7.54},
        {"hand": "Q/K/s", "win": 62.41, "lose": 35.61, "tie": 1.98, "expected_value": 26.80, "additional_chance": 7.84},
        {"hand": "6/6/u", "win": 62.70, "lose": 36.13, "tie": 1.17, "expected_value": 26.57, "additional_chance": 8.30},
        {"hand": "9/A/s", "win": 61.51, "lose": 35.95, "tie": 2.54, "expected_value": 25.56, "additional_chance": 8.60},
        {"hand": "10/A/u", "win": 61.57, "lose": 36.12, "tie": 2.31, "expected_value": 25.44, "additional_chance": 9.50},
        {"hand": "J/K/s", "win": 61.48, "lose": 36.34, "tie": 2.18, "expected_value": 25.13, "additional_chance": 9.80},
        {"hand": "8/A/s", "win": 60.51, "lose": 36.62, "tie": 2.87, "expected_value": 23.89, "additional_chance": 10.11},
        {"hand": "10/K/s", "win": 60.59, "lose": 37.01, "tie": 2.40, "expected_value": 23.58, "additional_chance": 10.41},
        {"hand": "Q/K/u", "win": 60.43, "lose": 37.52, "tie": 2.05, "expected_value": 22.91, "additional_chance": 11.31},
        {"hand": "7/A/s", "win": 59.39, "lose": 37.42, "tie": 3.19, "expected_value": 21.97, "additional_chance": 11.61},
        {"hand": "9/A/u", "win": 59.45, "lose": 37.90, "tie": 2.65, "expected_value": 21.55, "additional_chance": 12.52},
        {"hand": "J/K/u", "win": 59.44, "lose": 38.30, "tie": 2.25, "expected_value": 21.14, "additional_chance": 13.42},
        {"hand": "5/5/u", "win": 59.64, "lose": 38.99, "tie": 1.37, "expected_value": 20.65, "additional_chance": 13.88},
        {"hand": "J/Q/s", "win": 59.07, "lose": 38.55, "tie": 2.38, "expected_value": 20.52, "additional_chance": 14.18},
        {"hand": "9/K/s", "win": 58.64, "lose": 38.66, "tie": 2.70, "expected_value": 19.98, "additional_chance": 14.48},
        {"hand": "5/A/s", "win": 58.06, "lose": 38.22, "tie": 3.72, "expected_value": 19.85, "additional_chance": 14.78},
        {"hand": "6/A/s", "win": 58.18, "lose": 38.37, "tie": 3.45, "expected_value": 19.81, "additional_chance": 15.08},
        {"hand": "8/A/u", "win": 58.37, "lose": 38.63, "tie": 3.00, "expected_value": 19.75, "additional_chance": 15.99},
        {"hand": "10/K/u", "win": 58.49, "lose": 39.02, "tie": 2.49, "expected_value": 19.48, "additional_chance": 16.89},
        {"hand": "10/Q/s", "win": 58.17, "lose": 39.24, "tie": 2.59, "expected_value": 18.94, "additional_chance": 17.19},
        {"hand": "4/A/s", "win": 57.14, "lose": 39.07, "tie": 3.79, "expected_value": 18.07, "additional_chance": 17.50},
        {"hand": "7/A/u", "win": 57.17, "lose": 39.49, "tie": 3.34, "expected_value": 17.68, "additional_chance": 18.40},
        {"hand": "8/K/s", "win": 56.79, "lose": 40.17, "tie": 3.04, "expected_value": 16.62, "additional_chance": 18.70},
        {"hand": "3/A/s", "win": 56.34, "lose": 39.89, "tie": 3.77, "expected_value": 16.44, "additional_chance": 19.00},
        {"hand": "J/Q/u", "win": 56.91, "lose": 40.64, "tie": 2.46, "expected_value": 16.27, "additional_chance": 19.91},
        {"hand": "9/K/u", "win": 56.41, "lose": 40.78, "tie": 2.81, "expected_value": 15.62, "additional_chance": 20.81},
        {"hand": "5/A/u", "win": 55.74, "lose": 40.35, "tie": 3.91, "expected_value": 15.39, "additional_chance": 21.72},
        {"hand": "6/A/u", "win": 55.87, "lose": 40.51, "tie": 3.62, "expected_value": 15.36, "additional_chance": 22.62},
        {"hand": "9/Q/s", "win": 56.22, "lose": 40.89, "tie": 2.88, "expected_value": 15.33, "additional_chance": 22.93},
        {"hand": "7/K/s", "win": 55.85, "lose": 40.77, "tie": 3.38, "expected_value": 15.08, "additional_chance": 23.23},
        {"hand": "10/J/s", "win": 56.15, "lose": 41.10, "tie": 2.75, "expected_value": 15.06, "additional_chance": 23.53},
        {"hand": "2/A/s", "win": 55.51, "lose": 40.75, "tie": 3.75, "expected_value": 14.76, "additional_chance": 23.83},
        {"hand": "10/Q/u", "win": 55.95, "lose": 41.37, "tie": 2.69, "expected_value": 14.58, "additional_chance": 24.74},
        {"hand": "4/4/u", "win": 56.26, "lose": 42.21, "tie": 1.53, "expected_value": 14.05, "additional_chance": 25.19},
        {"hand": "4/A/u", "win": 54.73, "lose": 41.27, "tie": 3.99, "expected_value": 13.46, "additional_chance": 26.09},
        {"hand": "6/K/s", "win": 54.80, "lose": 41.52, "tie": 3.67, "expected_value": 13.28, "additional_chance": 26.40},
        {"hand": "8/K/u", "win": 54.43, "lose": 42.39, "tie": 3.18, "expected_value": 12.04, "additional_chance": 27.30},
        {"hand": "8/Q/s", "win": 54.42, "lose": 42.38, "tie": 3.20, "expected_value": 12.04, "additional_chance": 27.60},
        {"hand": "3/A/u", "win": 53.86, "lose": 42.17, "tie": 3.98, "expected_value": 11.69, "additional_chance": 28.51},
        {"hand": "5/K/s", "win": 53.83, "lose": 42.25, "tie": 3.92, "expected_value": 11.59, "additional_chance": 28.81},
        {"hand": "9/J/s", "win": 54.11, "lose": 42.79, "tie": 3.10, "expected_value": 11.32, "additional_chance": 29.11},
        {"hand": "9/Q/u", "win": 53.86, "lose": 43.14, "tie": 3.00, "expected_value": 10.72, "additional_chance": 30.02},
        {"hand": "10/J/u", "win": 53.83, "lose": 43.33, "tie": 2.84, "expected_value": 10.50, "additional_chance": 30.92},
        {"hand": "7/K/u", "win": 53.42, "lose": 43.04, "tie": 3.54, "expected_value": 10.37, "additional_chance": 31.83},
        {"hand": "2/A/u", "win": 52.95, "lose": 43.09, "tie": 3.96, "expected_value": 9.86, "additional_chance": 32.73},
        {"hand": "4/K/s", "win": 52.89, "lose": 43.12, "tie": 3.99, "expected_value": 9.77, "additional_chance": 33.03},
        {"hand": "7/Q/s", "win": 52.52, "lose": 43.92, "tie": 3.56, "expected_value": 8.60, "additional_chance": 33.33},
        {"hand": "6/K/u", "win": 52.30, "lose": 43.85, "tie": 3.85, "expected_value": 8.45, "additional_chance": 34.24},
        {"hand": "3/K/s", "win": 52.07, "lose": 43.96, "tie": 3.97, "expected_value": 8.11, "additional_chance": 34.54},
        {"hand": "9/10/s", "win": 52.38, "lose": 44.32, "tie": 3.30, "expected_value": 8.06, "additional_chance": 34.84},
        {"hand": "8/J/s", "win": 52.31, "lose": 44.28, "tie": 3.41, "expected_value": 8.03, "additional_chance": 35.14},
        {"hand": "3/3/u", "win": 52.84, "lose": 45.45, "tie": 1.71, "expected_value": 7.39, "additional_chance": 35.60},
        {"hand": "6/Q/s", "win": 51.68, "lose": 44.45, "tie": 3.87, "expected_value": 7.23, "additional_chance": 35.90},
        {"hand": "8/Q/u", "win": 51.93, "lose": 44.73, "tie": 3.34, "expected_value": 7.20, "additional_chance": 36.80},
        {"hand": "5/K/u", "win": 51.25, "lose": 44.63, "tie": 4.12, "expected_value": 6.63, "additional_chance": 37.71},
        {"hand": "9/J/u", "win": 51.64, "lose": 45.14, "tie": 3.22, "expected_value": 6.50, "additional_chance": 38.61},
        {"hand": "2/K/s", "win": 51.24, "lose": 44.82, "tie": 3.94, "expected_value": 6.42, "additional_chance": 38.91},
        {"hand": "5/Q/s", "win": 50.71, "lose": 45.17, "tie": 4.11, "expected_value": 5.54, "additional_chance": 39.22},
        {"hand": "8/10/s", "win": 50.51, "lose": 45.84, "tie": 3.65, "expected_value": 4.67, "additional_chance": 39.52},
        {"hand": "4/K/u", "win": 50.23, "lose": 45.57, "tie": 4.20, "expected_value": 4.65, "additional_chance": 40.42},
        {"hand": "7/J/s", "win": 50.45, "lose": 45.80, "tie": 3.74, "expected_value": 4.65, "additional_chance": 40.72},
        {"hand": "4/Q/s", "win": 49.76, "lose": 46.05, "tie": 4.18, "expected_value": 3.71, "additional_chance": 41.03},
        {"hand": "7/Q/u", "win": 49.90, "lose": 46.37, "tie": 3.72, "expected_value": 3.53, "additional_chance": 41.93},
        {"hand": "9/10/u", "win": 49.82, "lose": 46.75, "tie": 3.43, "expected_value": 3.06, "additional_chance": 42.84},
        {"hand": "8/J/u", "win": 49.71, "lose": 46.73, "tie": 3.55, "expected_value": 2.98, "additional_chance": 43.74},
        {"hand": "3/K/u", "win": 49.33, "lose": 46.48, "tie": 4.19, "expected_value": 2.85, "additional_chance": 44.65},
        {"hand": "6/Q/u", "win": 49.00, "lose": 46.95, "tie": 4.06, "expected_value": 2.05, "additional_chance": 45.55},
        {"hand": "3/Q/s", "win": 48.94, "lose": 46.90, "tie": 4.16, "expected_value": 2.04, "additional_chance": 45.85},
        {"hand": "8/9/s", "win": 48.86, "lose": 47.25, "tie": 3.89, "expected_value": 1.60, "additional_chance": 46.15},
        {"hand": "7/10/s", "win": 48.65, "lose": 47.37, "tie": 3.98, "expected_value": 1.28, "additional_chance": 46.46},
        {"hand": "6/J/s", "win": 48.57, "lose": 47.36, "tie": 4.06, "expected_value": 1.21, "additional_chance": 46.76},
        {"hand": "2/K/u", "win": 48.42, "lose": 47.41, "tie": 4.17, "expected_value": 1.02, "additional_chance": 47.66},
        {"hand": "2/2/u", "win": 49.39, "lose": 48.72, "tie": 1.90, "expected_value": 0.67, "additional_chance": 48.11},
        {"hand": "2/Q/s", "win": 48.10, "lose": 47.76, "tie": 4.13, "expected_value": 0.34, "additional_chance": 48.42},
        {"hand": "5/Q/u", "win": 47.96, "lose": 47.72, "tie": 4.32, "expected_value": 0.24, "additional_chance": 49.32},
        {"hand": "5/J/s", "win": 47.82, "lose": 47.85, "tie": 4.33, "expected_value": -0.03, "additional_chance": 49.62},
        {"hand": "8/10/u", "win": 47.82, "lose": 48.38, "tie": 3.81, "expected_value": -0.56, "additional_chance": 50.53},
        {"hand": "7/J/u", "win": 47.73, "lose": 48.36, "tie": 3.91, "expected_value": -0.64, "additional_chance": 51.43},
        {"hand": "4/Q/u", "win": 46.92, "lose": 48.67, "tie": 4.41, "expected_value": -1.74, "additional_chance": 52.34},
        {"hand": "7/9/s", "win": 46.99, "lose": 48.75, "tie": 4.25, "expected_value": -1.76, "additional_chance": 52.64},
        {"hand": "4/J/s", "win": 46.87, "lose": 48.73, "tie": 4.40, "expected_value": -1.86, "additional_chance": 52.94},
        {"hand": "6/10/s", "win": 46.80, "lose": 48.92, "tie": 4.28, "expected_value": -2.12, "additional_chance": 53.24},
        {"hand": "3/J/s", "win": 46.04, "lose": 49.58, "tie": 4.38, "expected_value": -3.54, "additional_chance": 53.54},
        {"hand": "3/Q/u", "win": 46.02, "lose": 49.59, "tie": 4.39, "expected_value": -3.56, "additional_chance": 54.45},
        {"hand": "8/9/u", "win": 46.07, "lose": 49.87, "tie": 4.06, "expected_value": -3.81, "additional_chance": 55.35},
        {"hand": "7/8/s", "win": 45.68, "lose": 49.81, "tie": 4.50, "expected_value": -4.13, "additional_chance": 55.66},
        {"hand": "7/10/u", "win": 45.83, "lose": 50.01, "tie": 4.16, "expected_value": -4.18, "additional_chance": 56.56},
        {"hand": "6/J/u", "win": 45.71, "lose": 50.02, "tie": 4.26, "expected_value": -4.31, "additional_chance": 57.47},
        {"hand": "6/9/s", "win": 45.15, "lose": 50.29, "tie": 4.55, "expected_value": -5.14, "additional_chance": 57.77},
        {"hand": "2/J/s", "win": 45.20, "lose": 50.45, "tie": 4.35, "expected_value": -5.24, "additional_chance": 58.07},
        {"hand": "2/Q/u", "win": 45.11, "lose": 50.52, "tie": 4.37, "expected_value": -5.41, "additional_chance": 58.97},
        {"hand": "5/10/s", "win": 44.94, "lose": 50.51, "tie": 4.55, "expected_value": -5.57, "additional_chance": 59.28},
        {"hand": "5/J/u", "win": 44.90, "lose": 50.54, "tie": 4.55, "expected_value": -5.64, "additional_chance": 60.18},
        {"hand": "4/10/s", "win": 44.20, "lose": 51.14, "tie": 4.65, "expected_value": -6.94, "additional_chance": 60.48},
        {"hand": "7/9/u", "win": 44.07, "lose": 51.48, "tie": 4.45, "expected_value": -7.40, "additional_chance": 61.39},
        {"hand": "6/8/s", "win": 43.82, "lose": 51.33, "tie": 4.85, "expected_value": -7.51, "additional_chance": 61.69},
        {"hand": "4/J/u", "win": 43.87, "lose": 51.50, "tie": 4.64, "expected_value": -7.63, "additional_chance": 62.59},
        {"hand": "6/10/u", "win": 43.85, "lose": 51.66, "tie": 4.49, "expected_value": -7.82, "additional_chance": 63.50},
        {"hand": "5/9/s", "win": 43.31, "lose": 51.87, "tie": 4.82, "expected_value": -8.56, "additional_chance": 63.80},
        {"hand": "3/10/s", "win": 43.38, "lose": 51.99, "tie": 4.63, "expected_value": -8.61, "additional_chance": 64.10},
        {"hand": "6/7/s", "win": 42.83, "lose": 52.09, "tie": 5.08, "expected_value": -9.26, "additional_chance": 64.40},
        {"hand": "3/J/u", "win": 42.97, "lose": 52.42, "tie": 4.62, "expected_value": -9.45, "additional_chance": 65.31},
        {"hand": "7/8/u", "win": 42.69, "lose": 52.59, "tie": 4.72, "expected_value": -9.90, "additional_chance": 66.21},
        {"hand": "2/10/s", "win": 42.54, "lose": 52.86, "tie": 4.60, "expected_value": -10.32, "additional_chance": 66.52},
        {"hand": "5/8/s", "win": 41.99, "lose": 52.90, "tie": 5.11, "expected_value": -10.91, "additional_chance": 66.82},
        {"hand": "6/9/u", "win": 42.10, "lose": 53.12, "tie": 4.78, "expected_value": -11.02, "additional_chance": 67.72},
        {"hand": "2/J/u", "win": 42.05, "lose": 53.35, "tie": 4.60, "expected_value": -11.30, "additional_chance": 68.63},
        {"hand": "5/10/u", "win": 41.86, "lose": 53.36, "tie": 4.79, "expected_value": -11.50, "additional_chance": 69.53},
        {"hand": "4/9/s", "win": 41.41, "lose": 53.68, "tie": 4.91, "expected_value": -12.28, "additional_chance": 69.83},
        {"hand": "5/7/s", "win": 40.98, "lose": 53.63, "tie": 5.39, "expected_value": -12.65, "additional_chance": 70.14},
        {"hand": "4/10/u", "win": 41.06, "lose": 54.05, "tie": 4.90, "expected_value": -12.99, "additional_chance": 71.04},
        {"hand": "3/9/s", "win": 40.81, "lose": 54.28, "tie": 4.91, "expected_value": -13.47, "additional_chance": 71.34},
        {"hand": "6/8/u", "win": 40.70, "lose": 54.21, "tie": 5.09, "expected_value": -13.52, "additional_chance": 72.25},
        {"hand": "5/6/s", "win": 40.35, "lose": 54.08, "tie": 5.57, "expected_value": -13.73, "additional_chance": 72.55},
        {"hand": "4/8/s", "win": 40.10, "lose": 54.70, "tie": 5.20, "expected_value": -14.60, "additional_chance": 72.85},
        {"hand": "5/9/u", "win": 40.14, "lose": 54.80, "tie": 5.06, "expected_value": -14.66, "additional_chance": 73.76},
        {"hand": "3/10/u", "win": 40.16, "lose": 54.97, "tie": 4.88, "expected_value": -14.81, "additional_chance": 74.66},
        {"hand": "2/9/s", "win": 39.97, "lose": 55.14, "tie": 4.88, "expected_value": -15.17, "additional_chance": 74.96},
        {"hand": "6/7/u", "win": 39.65, "lose": 55.01, "tie": 5.34, "expected_value": -15.35, "additional_chance": 75.87},
        {"hand": "4/7/s", "win": 39.11, "lose": 55.41, "tie": 5.48, "expected_value": -16.30, "additional_chance": 76.17},
        {"hand": "2/10/u", "win": 39.24, "lose": 55.90, "tie": 4.86, "expected_value": -16.66, "additional_chance": 77.07},
        {"hand": "4/5/s", "win": 38.53, "lose": 55.63, "tie": 5.84, "expected_value": -17.09, "additional_chance": 77.38},
        {"hand": "5/8/u", "win": 38.74, "lose": 55.89, "tie": 5.37, "expected_value": -17.14, "additional_chance": 78.28},
        {"hand": "4/6/s", "win": 38.48, "lose": 55.81, "tie": 5.70, "expected_value": -17.33, "additional_chance": 78.58},
        {"hand": "3/8/s", "win": 38.28, "lose": 56.54, "tie": 5.18, "expected_value": -18.25, "additional_chance": 78.88},
        {"hand": "4/9/u", "win": 38.09, "lose": 56.74, "tie": 5.17, "expected_value": -18.66, "additional_chance": 79.79},
        {"hand": "5/7/u", "win": 37.67, "lose": 56.65, "tie": 5.67, "expected_value": -18.98, "additional_chance": 80.69},
        {"hand": "2/8/s", "win": 37.68, "lose": 57.14, "tie": 5.18, "expected_value": -19.46, "additional_chance": 81.00},
        {"hand": "3/7/s", "win": 37.30, "lose": 57.23, "tie": 5.46, "expected_value": -19.93, "additional_chance": 81.30},
        {"hand": "3/9/u", "win": 37.43, "lose": 57.39, "tie": 5.18, "expected_value": -19.96, "additional_chance": 82.20},
        {"hand": "5/6/u", "win": 37.01, "lose": 57.12, "tie": 5.86, "expected_value": -20.11, "additional_chance": 83.11},
        {"hand": "3/5/s", "win": 36.76, "lose": 57.37, "tie": 5.87, "expected_value": -20.61, "additional_chance": 83.41},
        {"hand": "3/6/s", "win": 36.69, "lose": 57.62, "tie": 5.70, "expected_value": -20.93, "additional_chance": 83.71},
        {"hand": "4/8/u", "win": 36.71, "lose": 57.82, "tie": 5.48, "expected_value": -21.11, "additional_chance": 84.62},
        {"hand": "2/9/u", "win": 36.52, "lose": 58.32, "tie": 5.16, "expected_value": -21.80, "additional_chance": 85.52},
        {"hand": "3/4/s", "win": 35.73, "lose": 58.44, "tie": 5.83, "expected_value": -22.72, "additional_chance": 85.82},
        {"hand": "4/7/u", "win": 35.66, "lose": 58.56, "tie": 5.78, "expected_value": -22.90, "additional_chance": 86.73},
        {"hand": "2/7/s", "win": 35.44, "lose": 59.13, "tie": 5.43, "expected_value": -23.69, "additional_chance": 87.03},
        {"hand": "4/5/u", "win": 35.07, "lose": 58.76, "tie": 6.16, "expected_value": -23.69, "additional_chance": 87.93},
        {"hand": "4/6/u", "win": 35.00, "lose": 58.98, "tie": 6.01, "expected_value": -23.98, "additional_chance": 88.84},
        {"hand": "2/5/s", "win": 34.93, "lose": 59.23, "tie": 5.84, "expected_value": -24.30, "additional_chance": 89.14},
        {"hand": "2/6/s", "win": 34.84, "lose": 59.50, "tie": 5.66, "expected_value": -24.66, "additional_chance": 89.44},
        {"hand": "3/8/u", "win": 34.75, "lose": 59.78, "tie": 5.47, "expected_value": -25.03, "additional_chance": 90.35},
        {"hand": "2/4/s", "win": 33.92, "lose": 60.26, "tie": 5.82, "expected_value": -26.34, "additional_chance": 90.65},
        {"hand": "2/8/u", "win": 34.09, "lose": 60.43, "tie": 5.48, "expected_value": -26.34, "additional_chance": 91.55},
        {"hand": "3/7/u", "win": 33.72, "lose": 60.51, "tie": 5.77, "expected_value": -26.80, "additional_chance": 92.46},
        {"hand": "3/5/u", "win": 33.16, "lose": 60.64, "tie": 6.20, "expected_value": -27.47, "additional_chance": 93.36},
        {"hand": "3/6/u", "win": 33.07, "lose": 60.91, "tie": 6.02, "expected_value": -27.84, "additional_chance": 94.27},
        {"hand": "2/3/s", "win": 33.09, "lose": 61.12, "tie": 5.78, "expected_value": -28.03, "additional_chance": 94.57},
        {"hand": "3/4/u", "win": 32.07, "lose": 61.77, "tie": 6.16, "expected_value": -29.71, "additional_chance": 95.48},
        {"hand": "2/7/u", "win": 31.71, "lose": 62.54, "tie": 5.75, "expected_value": -30.83, "additional_chance": 96.38},
        {"hand": "2/5/u", "win": 31.19, "lose": 62.62, "tie": 6.18, "expected_value": -31.43, "additional_chance": 97.29},
        {"hand": "2/6/u", "win": 31.08, "lose": 62.93, "tie": 5.99, "expected_value": -31.85, "additional_chance": 98.19},
        {"hand": "2/4/u", "win": 30.12, "lose": 63.72, "tie": 6.16, "expected_value": -33.60, "additional_chance": 99.10},
        {"hand": "2/3/u", "win": 29.24, "lose": 64.63, "tie": 6.13, "expected_value": -35.39, "additional_chance": 100.00}
    ]
}

# 以下的列表顯⽰在兩位玩家的賭局當中、最初牌⾯的輸贏與補牌機率。期 望值是贏注的機率減去輸牌的機率。機率是得到特定牌⾯的機率、附加機 率是得到特定牌⾯或者列表當中任何其他較⾼牌⾯的機率。
'''
The tables below show the initial win/lose/tie probabilities and the additional chance of drawing a higher hand in a two-player poker game. 
Expected value is the probability of winning minus the probability of losing. 
Probability is the chance of getting a specific hand.
Additional chance is the chance of getting a specific hand or any higher hand in the list.
''' 

# Save to JSON
with open("./poker_odds.json", "w") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

# /Save to pickle
with open("./poker_odds.pkl", "wb") as pickle_file:
    pickle.dump(data, pickle_file)