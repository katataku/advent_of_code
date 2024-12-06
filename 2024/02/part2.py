

def read_input(file_name: str) -> list[str]:
    with open(file_name) as f:
        return f.readlines()
    
def is_safe(nums: list[int]) -> bool:
    is_increasing = True if nums[0] < nums[1] else False
    previous = nums[0]
    for num in nums[1:]:
        if is_increasing and previous >= num:
            return False
        if not is_increasing and previous <= num:
            return False
        if not (1 <= abs(num - previous) <= 3):
            return False
        previous = num
    return True

def main(file_name: str) -> None:
    """
    reportをn行、各行にあるlevelをm個として、
    時間計算量: O(n * (m**2))
        - `nums[:i]+nums[i+1:]`でリストを再作成しているため、同じ計算量でも時間がかかる処理になってそう
    空間計算量: O(m)。ただし、入力を受け取るためにO(nm)必要。
        - `nums[:i]+nums[i+1:]`でリストを再作成しているため、O(m)必要
    """
    lines = read_input(file_name)
    sum_safe = 0
    for line in lines:
        nums = list(map(int, line.split()))
        for i in range(len(nums)):
            if is_safe(nums[:i]+nums[i+1:]):
                sum_safe += 1
                break

    print(sum_safe)
    
if __name__ == '__main__':
    main('sample')
    main('input')
