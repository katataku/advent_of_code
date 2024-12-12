def read_input(file_name: str) -> list[str]:
    with open(file_name) as f:
        return f.readlines()

def is_word(map_: list[str], word: str, row: int, column: int, row_diff: int, column_diff: int) -> bool:
    if row < 0 or len(map_) <= row:
        return False
    if column < 0 or len(map_[row]) <= column:
        return False
    if len(word) == 0:
        return False
    if map_[row][column] != word[0]:
        return False
    if len(word) == 1:
        return True
    next_row = row + row_diff
    next_column = column + column_diff
    return is_word(map_, word[1:], next_row, next_column, row_diff, column_diff)

def count_xmas(map_: list[str]) -> int:
    """
    mapをn * mとすると、
    時間計算量: O(nm)。 「すべての位置」に対して、O(1)のXMASを探索する操作を9回行うため。
    空間計算量: O(1)。
    """
    xmas_count = 0
    for row in range(len(map_)):
        for column in range(len(map_[row])):
            for row_diff in [-1, 0, 1]:
                for column_diff in [-1, 0, 1]:
                    if is_word(map_, 'XMAS', row, column, row_diff, column_diff):
                        xmas_count += 1
    return xmas_count

def is_center_of_x_mas(map_: list[str], row: int, column: int) -> bool:
    x_max_count = 0
    for row_diff, column_diff in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        start_row = row - row_diff
        start_column = column - column_diff
        if is_word(map_, 'MAS', start_row, start_column, row_diff, column_diff):
            x_max_count += 1
    return x_max_count == 2

def count_x_mas(map_: list[str]) -> int:
    """
    mapをn * mとすると、
    時間計算量: O(nm)。 「すべての位置」に対して、O(1)のMASを探索する操作を4回行うため。
    空間計算量: O(1)。
    """
    x_mas_count = 0
    for row in range(len(map_)):
        for column in range(len(map_[row])):
            if is_center_of_x_mas(map_, row, column):
                x_mas_count += 1
    return x_mas_count

if __name__ == '__main__':
    sample_lines = read_input('sample')
    input_lines = read_input('input')
    
    # Part1
    sample_result = count_xmas(sample_lines)
    assert sample_result == 18, sample_result
    print("part1:", count_xmas(input_lines))

    # Part2
    # "XMAS"ではなく、X型の"MAS"を数える
    sample_result = count_x_mas(sample_lines)
    assert sample_result == 9, sample_result
    print("part1:", count_x_mas(input_lines))
