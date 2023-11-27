# def fibonacci(n):
#     # if n <= 0:
#     #     return []
#     # elif n == 1:
#     #     return [0]
#     # elif n == 2:
#     #     return [0, 1]
#     if n <= 2:
#         return [1, 1]
#     else:
#         fib_sequence = fibonacci(n - 1)
#         fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
#         return fib_sequence
#
# # 测试
# n = 10
# sequence = fibonacci(n)
# print(sequence)

def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [1]
    elif n == 2:
        return [1, 1]
    else:
        fib_sequence = [1, 1] + [0] * (n - 2)  # 初始化斐波那契数列数组
        for i in range(2, n):
            fib_sequence[i] = fib_sequence[i - 1] + fib_sequence[i - 2]
        return fib_sequence

# 测试
n = 10
sequence = fibonacci(n)
print(sequence)

