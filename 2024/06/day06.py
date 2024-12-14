from enum import IntEnum
import copy

# いわゆるキャラクターというより、c言語の文字型charという意味で、あえて_CHARという名前にした。
OBJECT_CHAR='#'
START_CHAR='^'
VISITED_CHAR='X'

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def read_input(file_name: str) -> list[str]:
    with open(file_name) as f:
        return f.readlines()

class Position():
    """
    # immutableなクラス。更新は、新しいPositionインスタンスを生成して返す。
    # comment: 更新も考えたけど、使いまわせるので、結果この方が効率的と考えた。
    """
    def __init__(self, row: int, column: int, direction: int = UP):
        self.row = row
        self.column = column
        self.direction = direction
    
    def is_inside_field(self, field: list[list[str]]) -> bool:
        return 0 <= self.row < len(field) and 0 <= self.column < len(field[self.row])
    
    def move_forward(self) -> 'Position':
        direction_to_diff = {
            UP: (-1, 0),
            RIGHT: (0, 1),
            DOWN: (1, 0),
            LEFT: (0, -1),
        }
        row_diff, column_diff = direction_to_diff[self.direction]
        return Position(self.row + row_diff, self.column + column_diff, self.direction)
    
    def turn_right(self) -> 'Position':
        return Position(self.row, self.column, (self.direction + 1) % 4)

    def is_on_same_row_and_column(self, row: int, column: int) -> bool:
        return self.row == row and self.column == column

    def is_on_same_position(self, other: 'Position') -> bool:
        return self.is_on_same_row_and_column(other.row, other.column)
    
    def is_on_field_object(self, field: list[list[str]]) -> bool:
        return field[self.row][self.column] == OBJECT_CHAR
    
    # setで使うために、__eq__と__hash__を実装する。
    # row, column, directionのすべてが同じなら、同じPositionとして扱う。
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Position):
            return self.row == other.row and self.column == other.column and self.direction == other.direction
        return False

    def __hash__(self) -> int:
        return hash((self.row, self.column, self.direction))

def find_start_position(field: list[list[str]]) -> Position:
    for row in range(len(field)):
        for column in range(len(field[row])):
            if field[row][column] == START_CHAR:
                return Position(row, column, UP)
    raise ValueError("Start position not found")

def plot_and_count_visited_char(field: list[list[str]]) -> tuple[list[list[str]], int]:
    field_with_visited = copy.deepcopy(field)
    current_position = find_start_position(field_with_visited)
    num_visited = 0
    while True:
        if field_with_visited[current_position.row][current_position.column] != VISITED_CHAR:
            field_with_visited[current_position.row][current_position.column] = VISITED_CHAR
            num_visited += 1
        next_position = current_position.move_forward()

        if not next_position.is_inside_field(field_with_visited):
            return field_with_visited, num_visited
        
        if next_position.is_on_field_object(field_with_visited):
            current_position = current_position.turn_right()
            continue
        current_position = next_position

def make_field(lines: list[str]) -> list[list[str]]:
    field = []
    for line in lines:
        field.append(list(line))
    return field

def count_visited_position(lines: list[str]) -> int:
    """
    マップの高さをn、幅をmとすると、
    時間計算量: O(nm)。
    空間計算量: O(nm)。
    """
    field = make_field(lines)
        
    _, num_visited = plot_and_count_visited_char(field)
    return num_visited


def is_loop(field: list[list[str]], current_position: Position, obstacle_position: Position) -> bool:
    visited_potitions: set[Position] = set()

    while True:
        next_position = current_position.move_forward()

        if not next_position.is_inside_field(field):
            return False

        if next_position.is_on_field_object(field) or next_position.is_on_same_position(obstacle_position):
            current_position = current_position.turn_right()
            continue
        
        if current_position in visited_potitions:
            return True
        visited_potitions.add(current_position)
        current_position = next_position

def count_loop_obstacle(lines: list[str]) -> int:
    """
    マップの高さをn、幅をm、障害物の数をlとすると、
    時間計算量: O((nm) ^ 2)。マップの各マスについて、障害物を置いてループができるかどうかを確認する。
    空間計算量: O((nm) ^ 2)。
    """
    field = make_field(lines)

    field_with_visited, _ = plot_and_count_visited_char(field)
    start_position = find_start_position(field)

    num_loop_obstacle = 0
    for row in range(len(field)):
        for column in range(len(field[row])):
            if field[row][column] == OBJECT_CHAR or field_with_visited[row][column] != VISITED_CHAR:
                continue
            if start_position.is_on_same_row_and_column(row, column):
                continue
            if is_loop(field, start_position, Position(row, column)):
                num_loop_obstacle += 1
    return num_loop_obstacle

if __name__ == '__main__':
    sample_lines = read_input('sample')
    input_lines = read_input('input')
    
    # Part1
    sample_result = count_visited_position(sample_lines)
    assert sample_result == 41, sample_result
    print("part1:", count_visited_position(input_lines))

    # Part2
    # 任意の場所に障害物を置いて、ループができるかどうかを確認する。
    # ループできる個数をカウントする。
    sample_result = count_loop_obstacle(sample_lines)
    assert sample_result == 6, sample_result
    print("sampel: OK")
    print("part2:", count_loop_obstacle(input_lines))


