# coding=utf-8

import random
import string

mac_address = ""

digit_result = string.digits
upper_result = string.ascii_uppercase

result = digit_result + upper_result[0:6]

tiaochu = 0
count = 0

while 1:
    if count % 2 == 0 and count != 0:
        mac_address += '-'

    mac_address += result[random.randint(0, 15)]

    count += 1
    if count == 12:
        break

print(mac_address)
