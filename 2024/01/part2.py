from collections import Counter

#FILE_NAME = 'sample'
FILE_NAME = 'input'

def main():
    """
    入力されるlocationの長さをnとして、
    時間計算量: O(n)
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

    right_counter = Counter(right_locations)
    similarity_score = 0
    for left in left_locations:
        similarity_score += left * right_counter[left]
    print(similarity_score)
    
if __name__ == '__main__':
    main()
