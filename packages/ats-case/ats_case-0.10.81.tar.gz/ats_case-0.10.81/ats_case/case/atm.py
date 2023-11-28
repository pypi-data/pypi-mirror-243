from ats_base.common import func


def sys_time():
    return func.sys_current_time()


def extract_letters(s):
    letters = []
    for char in s:
        if char.isalpha():
            letters.append(char)

    return ''.join(letters)
