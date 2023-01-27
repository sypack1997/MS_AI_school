import os
import shutil
import splitfolders

# splitfolder 라이브러리를 사용하기 위해 요구되는 directory 구조를 형성해야한다.
# data folder - class folder(images, labels)
os.makedirs("./data/images", exist_ok=True)
os.makedirs("./data/labels", exist_ok=True)

# 현재 디렉토리에서 이미지 파일과 xml 파일경로를 찾는다.
img_files = [f for f in os.listdir() if f.endswith('.jpg')]
xml_files = [f for f in os.listdir() if f.endswith('.xml')]
# print(img_files[0])

# data folder - class folder(images, labels) - *.jpg
# for i in range(len(img_files)):
#     shutil.move(img_files[i], "./input/images")
#     shutil.move(xml_files[i], "./input/labels")

# 데이터 스플릿 8:1:1
# splitfolders.ratio("input", output="dataset", seed=7777, ratio=(.8, .1, .1))