from collections import defaultdict

with open("05", "r") as f:
    rules = defaultdict(list)
    for line in f:
        line = line.strip()
        if line == "":
            break

        before, after = line.split("|")
        before, after = int(before), int(after)
        rules[before].append(after)
    
    pages_list = []
    for line in f:
        pages_list.append([int(i) for i in line.strip().split(",")])

def is_correctly_ordered(pages: list[int], rules: dict[int, list[int]]) -> bool:
    for i, page in enumerate(pages):
        for other in rules[page]:
            if other in pages and pages.index(other) < i:
                return False
    return True

def sort(pages: list[int], rules: dict[int, list[int]]) -> list[int]:
    out = []
    for page in pages:
        for i, inserted_page in enumerate(out):
            if page not in rules[inserted_page]:
                out.insert(i, page)
                break
        else:
            out.append(page)
    return out
    return sorted(pages, key = lambda i: item(i))

middle_sum = 0
sorted_middle_sum = 0
for pages in pages_list:
    if is_correctly_ordered(pages, rules):
        middle_sum += pages[len(pages) // 2]
    else:
        sorted_pages = sort(pages, rules)
        sorted_middle_sum += sorted_pages[len(pages) // 2]

print(middle_sum)
print(sorted_middle_sum)
    