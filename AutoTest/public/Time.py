# coding=utf-8
import datetime
from datetime import timedelta


class Time():
    now = datetime.datetime.now()

    # 今天
    today = (now).strftime('%Y/%m/%d %H:%M:%S')
    t_date = (now).strftime('%Y/%m/%d')
    # 时间格式%Y-%m-%d 今天和往前推7天
    t_date1 = (now).strftime('%Y-%m-%d')
    t_date2 = (now - timedelta(days=7)).strftime('%Y-%m-%d')


    # 昨天
    yestoday = (now - timedelta(days=1)).strftime('%Y/%m/%d')

    # 明天
    tomorrow = now + timedelta(days=1)  # 当前季度
    now_quarter = now.month / 3 if now.month % 3 == 0 else now.month / 3 + 1
    # 本周第一天和最后一天
    this_week_start = now - timedelta(days=now.weekday())
    this_week_end = now + timedelta(days=6 - now.weekday())

    # 上周第一天和最后一天
    last_week_start = (now - timedelta(days=now.weekday() + 7)).strftime('%Y/%m/%d')
    last_week_end = (now - timedelta(days=now.weekday() + 1)).strftime('%Y/%m/%d')

    # 本月第一天和最后一天
    this_month_start = datetime.datetime(now.year, now.month, 1)
    this_month_end = datetime.datetime(now.year, now.month + 1, 1) - timedelta(days=1)

    # 上月第一天和最后一天
    last_month_end1 = this_month_start - timedelta(days=1)
    last_month_end = last_month_end1.strftime('%Y/%m/%d')
    last_month_start = (datetime.datetime(last_month_end1.year, last_month_end1.month, 1)).strftime('%Y/%m/%d')

    # 本季第一天和最后一天
    month = (now.month - 1) - (now.month - 1) % 3 + 1
    this_quarter_start = datetime.datetime(now.year, month, 1)
    this_quarter_end = datetime.datetime(now.year, month + 3, 1) - timedelta(days=1)

    # 上季第一天和最后一天
    last_quarter_end = this_quarter_start - timedelta(days=1)
    last_quarter_start = datetime.datetime(last_quarter_end.year, last_quarter_end.month - 2, 1)

    # 本年第一天和最后一天
    this_year_start = datetime.datetime(now.year, 1, 1)
    this_year_end = datetime.datetime(now.year + 1, 1, 1) - timedelta(days=1)

    # 去年第一天和最后一天
    last_year_end = this_year_start - timedelta(days=1)
    last_year_start = datetime.datetime(last_year_end.year, 1, 1)


# 测试
if __name__ == '__main__':
    time = Time()
    print("今天：", time.today)
    print("今天日期：", time.t_date2, time.t_date1)
    print("昨天：", time.yestoday)
    print("上周开始:", time.last_week_start)
    print("上周结束:", time.last_week_end)
    print(time.last_month_start)
    print(time.last_month_end)
