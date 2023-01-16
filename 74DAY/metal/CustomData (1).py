import glob
import json
import os
import cv2
from torch.utils.data import Dataset



label_dict={'waist_folding':0, 'welding_line':1, 'water_spot':2, 'crease':3, 'crescent_gap':4, 'silk_spot':5, 'rolled_pit':6, 'punching_hole':7, 'inclusion':8, 'oil_spot':9}

class customDataset(Dataset):
    def __init__(self,path,transform=None):
        self.path=glob.glob(os.path.join(path,"*", "*.jpg"))
        print(self.path)
        self.transform=transform

    def __getitem__(self, item):
        img_path=self.path[item]
        print(img_path)
        image=cv2.imread(img_path)
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        img_name=img_path.split("\\")[1]
        print(img_name)


        with open("annotation.json", "r") as file:
            data = json.load(file)
            label_temp = data[img_name]["anno"][0]
            label = label_temp["label"]
            bbox = label_temp["bbox"]
        label=label_dict[label]
        x,y,x1,y1=bbox
        image=image[y:y1,x:x1]

        if self.transform is not None:
            image=self.transform(image=image)["image"]

        return image,label


    def __len__(self):
        return len(self.path)

test=customDataset("./dataset/train/")
print(test)