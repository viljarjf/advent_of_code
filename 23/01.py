import numpy as np

with open("01", "r", encoding="utf-8") as inp:

    codes = ("".join(c for c in line if c.isnumeric()) for line in inp)
    codes = (code[0] + code[-1] for code in codes)
    codes = (int(code) for code in codes)

    print(f"{sum(codes) = }")

def find_first_number(code: str) -> str:
    numbers = [
        ("one",    "1"),
        ("two",    "2"),
        ("three",  "3"),
        ("four",   "4"),
        ("five",   "5"),
        ("six",    "6"),
        ("seven",  "7"),
        ("eight",  "8"),
        ("nine",   "9"),
    ]
    for i in range(len(code)):
        if code[i].isnumeric():
            return code[i]
        c = code[:i+1]
        for num, digit in numbers:
            if num in c:
                return digit

def find_last_number(code: str) -> str:
    code = code[::-1]
    numbers = [
        ("one",    "1"),
        ("two",    "2"),
        ("three",  "3"),
        ("four",   "4"),
        ("five",   "5"),
        ("six",    "6"),
        ("seven",  "7"),
        ("eight",  "8"),
        ("nine",   "9"),
    ]
    for i in range(len(code)):
        if code[i].isnumeric():
            return code[i]
        c = code[:i+1]
        for num, digit in numbers:
            num = num[::-1]
            if num in c:
                return digit

with open("01", "r", encoding="utf-8)") as inp:
    codes = (find_first_number(code) + find_last_number(code) for code in inp)
    codes = (int(code) for code in codes)

    # print(list(codes))
    print(f"{sum(codes) = }")
