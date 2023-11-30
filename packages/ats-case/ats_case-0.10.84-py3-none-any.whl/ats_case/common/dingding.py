from dingtalkchatbot.chatbot import DingtalkChatbot

from ats_base.service import db

from ats_case.common.enum import Payload

TXT = '### **{}**\n\n' \
      '# {}\n\n' \
      '---\n\n' \
      '>**测试序号:**  {}\n\n' \
      '>**开始时间:**  {}\n\n' \
      '>**结束时间:**  {}\n\n' \
      '>**测试结果:**  {} @{} {}\n\n'


def send(payload: Payload, project: str, test_sn: str, start_time, end_time, msg='', subhead=''):
    try:
        url, secret, sign = _link(test_sn)
        dc = DingtalkChatbot(url, secret)
        dc.send_markdown(title=f'{sign}', text=_data(payload, project, test_sn, start_time, end_time, msg, subhead),
                         is_at_all=True)
    except Exception as e:
        print(str(e))


def _link(test_sn):
    username = extract_letters(test_sn)

    user = db.query('sys:user', name=username)
    gid = user.get('msg_group_id')
    group = db.query('sys:msg:group', id=gid)

    url = group.get('url')
    secret = group.get('secret')
    sign = group.get('sign')

    return url, secret, sign


def _data(payload, project, test_sn, start_time, end_time, msg='', subhead=''):
    sn = test_sn.split(':')[0]
    username = extract_letters(test_sn).lower()

    start_time = start_time.strftime('%Y.%m.%d %H:%M:%S')
    end_time = end_time.strftime('%Y.%m.%d %H:%M:%S')

    completed_msg = _none()
    if payload == Payload.NORMAL:
        completed_msg = _normal()
    if payload == Payload.WARN:
        completed_msg = _warn()
    if payload == Payload.ERROR:
        completed_msg = _error()

    return TXT.format(project, subhead, sn, start_time, end_time, completed_msg, username, msg)


def _none():
    return '<font color="#8F8100">[未知]</font>'


def _normal():
    return '<font color="#00EE00">[完成]</font>'


def _warn():
    return '<font color="#FFD700">[警告]</font>'


def _error():
    return '<font color="#DC143C">[出错]</font>'


def extract_letters(s):
    letters = []
    for char in s:
        if char.isalpha():
            letters.append(char)

    return ''.join(letters)
