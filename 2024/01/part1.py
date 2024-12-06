#FILE_NAME = 'sample'
FILE_NAME = 'input'

def main():
    """
    入力されるlocationの長さをnとして、
    時間計算量: O(nlogn)
    空間計算量: O(n)
    """
    left_locations = []
    right_locations = []
    with open(FILE_NAME) as f:
        lines = f.readlines()
        for line in lines:
            left, right = map(int, line.split())
            left_locations.append(left)
            right_locations.append(right)
    
    left_locations.sort()
    right_locations.sort()
    sum_distance = 0
    for left, right in zip(left_locations, right_locations):
        sum_distance += abs(left - right)

    print(sum_distance)
    
if __name__ == '__main__':
    main()
