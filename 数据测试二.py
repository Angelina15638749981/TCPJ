import re
#
fileName = r"C:\Users\admin\Desktop\TCPJW\certify_code\要处理的文档.txt"
with open(fileName,) as f:
  every_line_content = f.readline()
  # print(every_line_content)
  nums=re.findall(r'\d+', every_line_content)
  words=re.compile(r"\b[a-zA-Z]+\b",re.I).findall(every_line_content)


# file1_words = open("words.txt",)
# file2_nums = open(("nums.txt",)
#
for word in words:
  print(word)
  # 复制到words.txt里面
  # file1_words.write(word)
for num in nums:
  print(num)
  # 复制到nums.txt里面
  # file1_words.write()

