from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

# 访问百度
driver = webdriver.Chrome()
driver.get("http://www.baidu.com")
# 搜索
driver.find_element_by_id("kw").send_keys("selenium")
driver.find_element_by_id("su").click()
time.sleep(3)
# #通过按向下键将页面滚动条拖到底部
# driver.find_element_by_xpath("//*[@id='page']/a[10]").send_keys(Keys.DOWN)
# print ('将滚动条拉到底端')
# time.sleep(2)
# driver.find_element_by_xpath("//*[@id='s_tab']/a[9]").send_keys(Keys.UP)
# print ('将滚动条拉到上端')
# time.sleep(2)
# driver.find_element_by_xpath("//*[@id='con-ar']/div[3]/a").send_keys(Keys.DOWN)
# print ('将滚动条拉到中间')
# 将页面滚动条拖到底部
js = "var q=document.body.scrollTop=100000"
driver.execute_script(js)
print('将滚动条拉到底端')
time.sleep(3)
# 将滚动条移动到页面的顶部
js = "var q=document.body.scrollTop=0"
driver.execute_script(js)
time.sleep(3)
print('将滚动条拉到上端')

# 滚动到底部
js1 = "window.scrollTo(0,document.body.scrollHeight)"
driver.execute_script(js1)
print('111将滚动条拉到底端')
time.sleep(5)

# 滚动到顶部
js2 = "window.scrollTo(0,0)"
driver.execute_script(js2)
print('2222将滚动条拉到上端')

# #这是修改后的版本，测试后基本可以用了~
# grade={'Adam':19,'Bob':23,'Cary':25,'David':27,'Emma':29,'Flora':31,'Gloria':33,'Hox':35,'Ivan':37,'Jenny':22}#dict
# print('欢迎登录BMI查询系统\n')
# a=3
# b=2
# while a>b:
#     order=input('查询，请按 1 ；\n录入，请按 2 ；\n修改，请按 3 ；\n删除，请按 4 ；\n退出，请按 5 。\n')
#     number=('1','2','3','4','5')#tuple
#     if order not in number:
#         print('数字输入有误，请输入1,2,3,4,5')
#         continue
#     else:
#         num=int(order)
#         while num==1:
#             name=input('请输入学生姓名:')
#             if name in grade:
#                 print('%s的BMI分数为%.1f.\n'%(name,grade[name]))
#                 if grade[name]>32:
#                     print('你的体重属于严重肥胖了哦~\n')
#                 elif grade[name]>27:
#                     print('你的体重已经属于肥胖了哦~\n')
#                 elif grade[name]>24:
#                     print('你的体重有些过重了哦~\n')
#                 elif grade[name]>18.5:
#                     print('恭喜！你的身材很标准！\n')
#                 else:
#                     print('你的体重有些过轻，需要补充营养哦~\n')
#                 exit=input('按Y继续查询，按N退出系统，按任意键回到主菜单~\n')
#                 if exit=='Y':
#                     continue
#                 elif exit=='N':
#                     b=4
#                     break
#                 else:
#                     break
#             else:
#                 print('姓名输入有误，请重新输入！\n')
#                 continue
#         while num==2:
#             name=input('请输入学生姓名:')
#             height=float(input('请输入学生身高(m)：'))
#             if height<1.3 or height>2.5:
#                 print('身高输入错误，请重新输入！')
#                 continue
#             else:
#                 weight=float((input('请输入学生体重(kg)：')))
#                 if weight<30 or weight>200:
#                     print('体重输入错误，请重新输入！\n')
#                     continue
#                 else:
#                     BMI=weight/(height2)
#                     grade[name]=BMI
#                     print('录入成功！\n')
#                     exit=input('按Y继续录入，按N退出系统，按任意键回到主菜单~\n')
#                     if exit=='Y':
#                         continue
#                     elif exit=='N':
#                         b=4
#                         break
#                     else:
#                         break
#         while num==3:
#             name=input('请输入学生姓名：')
#             if name in grade:
#                 height=float(input('请输入学生身高(m)：'))
#                 if height<1.3 or height>2.5:
#                     print('身高输入错误，请重新输入！\n')
#                     continue
#                 else:
#                     weight=float((input('请输入学生体重(kg)：')))
#                     if weight<30 or weight>200:
#                         print('体重输入错误，请重新输入！\n')
#                         continue
#                     else:
#                         BMI=weight/(height2)
#                         grade[name]=BMI
#                         print('修改成功！\n')
#                         exit=input('按Y继续修改，按N退出系统，按任意键回到主菜单~\n')
#                         if exit=='Y':
#                             continue
#                         elif exit=='N':
#                             b=4
#                             break
#                         else:
#                             break
#             else:
#                 print('查无此人！\n')
#                 exit=input('按Y继续修改，按N退出系统，按任意键回到主菜单~\n')
#                 if exit=='Y':
#                     continue
#                 elif exit=='N':
#                     b=4
#                     break
#                 else:
#                     break
#         while num==4:
#             name=input('请输入学生姓名：')
#             if name in grade:
#                 grade.pop(name)
#                 print('删除成功！\n')
#                 exit=input('按Y继续删除，按N退出系统，按任意键回到主菜单~\n')
#                 if exit=='Y':
#                     continue
#                 elif exit=='N':
#                     b=4
#                     break
#                 else:
#                     break
#             else:
#                 print('查无此人！\n')
#                 exit=input('按Y继续删除，按N退出系统，按任意键回到主菜单~\n')
#                 if exit=='Y':
#                     continue
#                 elif exit=='N':
#                     b=4
#                     break
#                 else:
#                     break
#         while num==5:
#             print('感谢您的使用！再见！')
#             b=4
#             break
#
