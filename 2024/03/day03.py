def read_input(file_name: str) -> list[str]:
    with open(file_name) as f:
        return f.readlines()

def is_valid_operand(operand: str) -> bool:
    return operand.isdecimal() and 1 <= len(operand) <= 3

def calc_mul(line: str) -> int:
    if not line.startswith('mul('):
        return 0

    close_parenthesis_index = line.find(')')
    if close_parenthesis_index == -1:
        return 0
    
    comma_index = line.find(',')
    if comma_index == -1:
        return 0
    
    first_operand = line[4:comma_index]
    if not is_valid_operand(first_operand):
        return 0

    second_operand = line[comma_index + 1:close_parenthesis_index]
    if not is_valid_operand(second_operand):
        return 0
    
    return int(first_operand) * int(second_operand)

def calc_result_of_multiplications(lines: str) -> int:
    """
    instructionをn文字とすると
    時間計算量: O(n^2)。 「すべての位置始まる文字列」に対して、findを実行するため。
    空間計算量: O(n)。「すべての位置始まる文字列」を、sliceで作成するため。
    """
    result_of_multiplications = 0
    for line in lines:
        for i in range(len(line)):
            result_of_multiplications += calc_mul(line[i:])
    return result_of_multiplications

def calc_result_of_multiplications_with_skipping(lines: str) -> int:
    """
    instructionをn文字とすると
    時間計算量: O(n^2)。 「すべての位置始まる文字列」に対して、findを実行するため。
    空間計算量: O(n)。「すべての位置始まる文字列」を、sliceで作成するため。
    """
    result_of_multiplications = 0
    is_disabled = False
    for line in lines:
        for i in range(len(line)):
            if is_disabled:
                if line[i:].startswith('do()'):
                    is_disabled = False
                continue
            if line[i:].startswith("don't()"):
                is_disabled = True
                continue
            result_of_multiplications += calc_mul(line[i:])
    return result_of_multiplications

if __name__ == '__main__':
    sample_lines = read_input('sample')
    input_lines = read_input('input')
    
    # Part1
    assert calc_result_of_multiplications(sample_lines) == 161
    print("part1:", calc_result_of_multiplications(input_lines))

    # Part2
    # Part1に加えて、"don't()"から"do()"までの間は無視する
    assert calc_result_of_multiplications_with_skipping(sample_lines) == 48
    print("part2:", calc_result_of_multiplications_with_skipping(input_lines))


