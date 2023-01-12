import os

file_path = "./data2/ㅎ"

file_names = os.listdir(file_path)
print(file_names)

i = 1
for name in file_names:
    src = os.path.join(file_path, name)
    dst = str(i) + 'psy.png'
    dst = os.path.join(file_path, dst)
    os.rename(src, dst)
    i +=1