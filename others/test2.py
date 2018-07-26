# # -*- coding: utf-8 -*-
# import math
#
# a = float(input('请输入a: '))
# b = float(input('请输入b: '))
# c = float(input('请输入c: '))
#
#
# def quadratic(a, b, c):
#     f = b * b - 4 * a * c
#     if f < 0:
#         print('方程无解！')
#         return
#     elif f == 0:
#         x = -b / (2 * a)
#         print('方程只有一个根！')
#         return (x)
#     else:
#         x1 = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
#         x2 = (b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
#         print('方程有两个根！')
#     return (x1, x2)
#
#
# print(quadratic(a, b, c))
import requests

response = requests.get("http://192.168.10.110:8080/WebGis/main?userID=20180630100329000000000000009575")
# 打印请求页面的状态（状态码）
print(type(response.status_code), response.status_code)
# 打印请求网址的headers所有信息
print(type(response.headers), response.headers)
# 打印请求网址的cookies信息
print(type(response.cookies), response.cookies)
# 打印请求网址的地址
print(type(response.url), response.url)
# 打印请求的历史记录（以列表的形式显示）
print(type(response.history), response.history)
