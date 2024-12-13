import heapq
from collections import defaultdict 

def read_input(file_name: str) -> list[str]:
    with open(file_name) as f:
        return f.readlines()

def read_lines(lines: list[str]) -> tuple[dict[int, list[int]], list[list[int]]]:
    page_to_prerequired_pages: dict[int, list[int]] = defaultdict(list)
    i = 0
    while True:
        if lines[i] == '\n':
            break
        left, right = map(int, lines[i].split('|'))
        page_to_prerequired_pages[right].append(left)
        i += 1
    updates = []
    for line in lines[i + 1:]:
        updates.append([int(x) for x in line.split(',')])
    return page_to_prerequired_pages, updates

def is_valid_update(update: list[int], page_to_prerequired_pages: dict[int, list[int]]) -> bool:
    prerequired_pages = set()
    for page in update:
        if page in prerequired_pages:
            return False
        for prerequire in page_to_prerequired_pages.get(page, []):
            prerequired_pages.add(prerequire)
    return True

def calc_sum_of_correct_middle_page(lines: list[str]) -> int:
    """
    order ruleの数をn, updateの個数をm, updateの最大長をlとして、計算量は以下の通り。
    時間計算量: O(nml)。
    空間計算量: O(nl)。
    """
    page_to_prerequired_pages, updates = read_lines(lines)
    sum_of_correct_middle_page = 0
    for update in updates:
        if is_valid_update(update, page_to_prerequired_pages):
            middle_page = update[len(update) // 2]
            sum_of_correct_middle_page += middle_page
    return sum_of_correct_middle_page

def count_prerequires(page: int, page_to_prerequired_pages: dict[int, list[int]], unused_pages: set[int]) -> int:
    total_prerequires = set(page_to_prerequired_pages.get(page, []))
    return len(unused_pages & total_prerequires)

def order_update(update: list[int], page_to_prerequired_pages: dict[int, list[int]]) -> list[int]:
    unused_pages = set(update)
    num_prerequire_and_page: list[tuple[int, int]] = []
    for page in update:
        num_prerequires = count_prerequires(page, page_to_prerequired_pages, unused_pages)
        heapq.heappush(num_prerequire_and_page, (num_prerequires, page))

    ordered_update = []
    next_num_prerequire_and_page: list[tuple[int, int]] = []
    while num_prerequire_and_page or next_num_prerequire_and_page:
        if not num_prerequire_and_page:
            num_prerequire_and_page = next_num_prerequire_and_page
            next_num_prerequire_and_page = []
            
        _, page = heapq.heappop(num_prerequire_and_page)
        num_prerequires = count_prerequires(page, page_to_prerequired_pages, unused_pages)
        if num_prerequires > 0:
            heapq.heappush(next_num_prerequire_and_page, (num_prerequires, page))
            continue
        ordered_update.append(page)
        unused_pages.remove(page)
    return ordered_update

def calc_sum_of_ordered_middle_page(lines: list[str]) -> int:
    """
    order ruleの数をn, updateの個数をm, updateの最大長をlとして、計算量は以下の通り。
    時間計算量: O(nml)。
    空間計算量: O(nl)。
    """
    page_to_prerequired_pages, updates = read_lines(lines)
    sum_of_ordered_middle_page = 0
    for update in updates:
        if is_valid_update(update, page_to_prerequired_pages):
            continue
        ordered_update = order_update(update, page_to_prerequired_pages)
        middle_page = ordered_update[len(update) // 2]
        sum_of_ordered_middle_page += middle_page
    return sum_of_ordered_middle_page

if __name__ == '__main__':
    sample_lines = read_input('./sample')
    input_lines = read_input('./input')
    
    # Part1
    # 正しいupdateについて、中央値を合計する。
    sample_result = calc_sum_of_correct_middle_page(sample_lines)
    assert sample_result == 143, sample_result
    print("part1:", calc_sum_of_correct_middle_page(input_lines))

    # Part2
    # 不正なupdateについて、updateを並び替えた上で中央値を合計する。
    sample_result = calc_sum_of_ordered_middle_page(sample_lines)
    assert sample_result == 123, sample_result
    print("part2:", calc_sum_of_ordered_middle_page(input_lines))
