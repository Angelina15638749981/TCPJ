nums = [2, 3, 4, 5, 6, 7]
target = 10
def get_index():
    for num1 in nums:
        for num2 in nums:
            if target-num1 == num2:
                print(nums.index[num1], nums.index[num2])
            return nums.index[num1], nums.index[num2]


