from torch.utils.data.dataset import Dataset
from torchvision import transforms
import cv2
import os
import pandas as pd


class MyCustomDataset(Dataset):
    def __init__(self, path, transforms = None): ## cvs읽기, 뱐환할당, 데이터 필터링 등과 같은 초기 논리가 발생하는 곳
        # data path
        self.all_data_path = pd.read_csv(os.path.join(path))


    def __getitem__(self, index): ## 데이터와 레이블을 반환 dataloader에서 호출된다.
        file_name = self.all_data_path.iloc[index, 1]
        x1 = self.all_data_path.iloc[index, 2]
        y1 = self.all_data_path.iloc[index, 3]
        w = self.all_data_path.iloc[index, 4]
        h = self.all_data_path.iloc[index, 5]

        return file_name, x1, y1, w, h
        # return filename, bbox # 과제 양식

    def __len__(self): ## 보유한 샘플 수 를 반환
        return len(self.all_data_path)

temp = MyCustomDataset("./coco_box_points.csv")

for i in temp:
    print(i)