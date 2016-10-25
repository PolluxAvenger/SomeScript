# coding=utf-8

# 用formkeys() 生成一个字典
invisible_char = dict.fromkeys(range(32))
invisible_char2 = dict.fromkeys(range(32), '\256')

char_string = b'abcd\012\02212345\011efg\23987'
char_string2 = 'abcd\012\02212345\011efg\23987'

# translate()，接受 byte 类型而非字符串型，第一个参数是替换，第二个参数是删除
result_string = char_string.translate(None, bytes(invisible_char))
result_string2 = char_string2.translate(invisible_char2)

print('translate()只删除不替换')
# 直接返回的不是字符串，需要用 decode() 转换成字符串型
print(result_string.decode())

print('原始字符串：')
print(char_string)
print('替换后字符串：')
print(result_string2)
result = result_string2.split('\256')
print('分割结果如下：')
print(result)
print('去掉空元素的结果：')
# filter() 返回值不再是列表，需要自己列表化
no_white_list = list(filter(None, result))
print(no_white_list)
max_string = max(no_white_list, key=len)
print('其中最长字符串为：')
print(max_string)
