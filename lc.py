from urllib.request import Request, urlopen
import json
import datetime


def open_url(username, limit):
    base = 'https://leetcode.com/graphql?query=query%20recentAcSubmissions{{recentAcSubmissionList(username:%22{username}%22,%20limit:{limit})%20{{id%20title%20titleSlug%20timestamp}}}}'
    url = base.format(username=username, limit=limit)
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    req = Request(url, headers=head)
    response = urlopen(req)
    html = response.read()
    html_str = html.decode('utf-8')
    return html_str


def get_prev_week_date():
    today = datetime.date.today() + datetime.timedelta(days=2)
    prev_monday = today - datetime.timedelta(days=today.weekday(), weeks=1)
    prev_sunday = prev_monday + datetime.timedelta(days=6)
    return (prev_monday, prev_sunday)


def is_submited_in_prev_week(ts):
    dates = get_prev_week_date()
    ts_date = datetime.datetime.fromtimestamp(int(ts)).date()
    return dates[0] <= ts_date <= dates[1]


def gen_submission_list(html_str):
    obj = json.loads(html_str)
    if 'data' not in obj:
        return []
    if 'recentAcSubmissionList' not in obj['data']:
        return []
    sub_lst = obj['data']['recentAcSubmissionList']
    if not sub_lst:
        return [-1]
    prev_ac_problems = []
    for item in sub_lst:
        if is_submited_in_prev_week(item['timestamp']):
            prev_ac_problems.append(item['title'])
    return prev_ac_problems


def print_result(username, ac_problems):
    prev_ac_count = len(ac_problems)
    if prev_ac_count == 1 and ac_problems[0] == -1:
        res = username + '\tInvalid'
        print(res)
        return
    ac_limit = 5
    unit_price = 10
    usd2rmb = 7
    res = username + '\tTotal AC: ' + str(prev_ac_count)
    if prev_ac_count < ac_limit:
        rmb = unit_price * (ac_limit - prev_ac_count)
        res += '  \tPenalty: ¥' + \
            str(rmb) + '($' + '{:.2f}'.format(rmb / usd2rmb) + ')'
    print(res)


name_dict = {'QiaoZhennn': 'Zhen',
             #'xtdong1001': 'Xingt',
             #'pinisthn': 'Nicole',
             #'haomiaovast': 'Emma',
             'SeSmC06': 'Peng',
             'RachelLiu66': 'Rachel',
             'ychen01': 'Yian',
             'wchoi32': 'John'}
limit = 20

if __name__ == '__main__':
    dates = get_prev_week_date()
    print(str(dates[0]) + ' to ' + str(dates[1]))
    for id, name in name_dict.items():
        html_str = open_url(id, limit)
        ac_problems = gen_submission_list(html_str)
        print_result(name, ac_problems)
