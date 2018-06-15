# -*- coding: utf-8 -*-
import math

a = float(input('请输入a: '))
b = float(input('请输入b: '))
c = float(input('请输入c: '))


def quadratic(a, b, c):
    f = b * b - 4 * a * c
    if f < 0:
        print('方程无解！')
        return
    elif f == 0:
        x = -b / (2 * a)
        print('方程只有一个根！')
        return (x)
    else:
        x1 = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
        x2 = (b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
        print('方程有两个根！')
    return (x1, x2)


print(quadratic(a, b, c))
