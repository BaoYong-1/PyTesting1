def calc(*numbers):
    m = len(numbers)
    if len(numbers) == 0:
        raise TypeError
    m = 1
    for n in numbers:
        m = m * n
    return m


print(calc(1, 2, 3,4))
