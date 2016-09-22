# coding=utf-8

import string
import random


def password(length = 10):
    letter = string.ascii_letters
    little_letter = string.ascii_lowercase
    big_letter = string.ascii_uppercase
    digit = string.digits
    mask = string.punctuation

    password_string = letter + digit + mask
    password_letter = [random.choice(password_string) for _ in range(length)]
    password_result = ''.join(password_letter)
    print('生成的密码是：' + password_result)


if __name__ == '__main__':

    password()
