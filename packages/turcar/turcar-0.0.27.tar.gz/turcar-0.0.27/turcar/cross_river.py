import itertools


def print_combinations(people):
    result = []  # 用于存储所有可能的过河方案
    left_bank = set(people)  # 左岸的初始情况
    right_bank = set()  # 右岸的初始情况
    boat = set()  # 船上的初始情况

    # 判断双人组是否安全
    def is_valid(path):
        if ('妈妈' in path and ('爸爸' in path or '路人' in path or '哥哥' in path)) or (
                '爸爸' in path and ('妹妹' in path or '妈妈' in path)) or (
                '哥哥' in path and ('妹妹' in path or '妈妈' in path or '路人' in path)) or (
                '妹妹' in path and ('爸爸' in path or '哥哥' in path)) or (
                '路人' in path and ('妈妈' in path or '哥哥' in path)):
            return False
        return True

    # 模拟每次过河的情况
    def cross(left_river, path=[]):
        print("左： ", left_river)
        print("右： ", right_bank)

        # 返回左岸,从船上下来一个人
        if boat:
            # print("回来的人： ", boat)
            left_river.update(boat)  # 船上的人回到左岸
            right_bank.difference_update(boat)  # 船上的人从右岸移除
            # print("path： ", path)
            path = path + [(list(boat)[0])]  # 过河方案拼接
            boat.clear()
            # print("path： ", path)
            # print("回来后左岸： ", left_river)

        # 遍历所有可能的过桥方式，即从左岸选取两个人
        for pair in itertools.combinations(left_river, 2):
            a, b = pair
            # 安全的双人组
            if is_valid([a, b]):
                new_river = left_river - {a, b}  # 更新左岸的情况

                right_bank.update({a, b})  # 更新右岸的情况
                # print("过河后左岸:", new_river)
                # print("过河后右岸:", right_bank)
                new_path = path + [(a, b)]  # 过河方案拼接
                print("过河组合: ", new_path)

                # 如果左岸和船上都没有人，则表示所有人都已经成功过河，将当前路径加入结果中
                if not new_river and not boat:
                    result.append(path)
                    return
                # 遍历所有可能返回方式，
                for load in itertools.combinations(right_bank, 1):
                    if len(load) == 1 and load[0] != "妹妹":
                        # 执行相关操作
                        boat.clear()
                        boat.update(load)
                        cross(new_river, new_path)

    cross(left_bank)
    print("结束")
    print(result)
    for i, step in enumerate(result):
        print(f"Step {i + 1}: {step}")


people = ['妈妈', '爸爸', '哥哥', '妹妹', '路人']
print_combinations(people)
