# coding=utf-8

import re

all_result = []
final_result = []

regular = re.compile('(\d+)\.(\d+)\.(\d+)\.(\d+)')

with open('access.log', 'r+') as f:
    for line in f:
        content = re.search(regular, line).group()
        all_result.append(content)

print(all_result)
print(len(all_result))
final_result = list(set(all_result))
        # t.write(content + ' - - [25/May/2016:05:14:41 +0000] "GET /media/system/js/caption.js HTTP/1.1" 200 491 "http://198.58.105.152/" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"\n')
#for item in all_result:
#    for item in final_result#:
#        final_result.append(item)
with open('result.log', 'w+') as t:
    for item in final_result:
        t.write(item + ' - - [13/Apr/2016:04:28:26 +0000] "GET / HTTP/1.1" 502 583 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"' + '\n')

print(final_result)
print(len(final_result))
#last_list = [x for x in  if x not in delete_list]
