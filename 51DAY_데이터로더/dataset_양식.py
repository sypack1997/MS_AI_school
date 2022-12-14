from torch.utils.data.dataset import Dataset
from torchvision import transforms
import cv2

label_dic = {"cat" : 0, "dog" : 1}

class MyCustomDataset(Dataset):
    def __init__(self, path, transforms = None): ## cvs읽기, 뱐환할당, 데이터 필터링 등과 같은 초기 논리가 발생하는 곳
        # data path
        self.all_data_path = "./image/*.jpg"
        self.transforms = transforms


    def __getitem__(self, index): ## 데이터와 레이블을 반환 dataloader에서 호출된다.
        image_path = self.all_data_path[index]
        # 'image01.png, image02.png, image03.png, ...'
        label_temp = image_path.split("\\")
        # [. , image , cat.jpg]
        label_temp = label_temp[2]
        # cat.jpg
        label_temp = label_temp.replace(".jpg", "")
        # cat
        label = label_dic[label_temp]
        # 0
        
        # image read
        image = cv2.imread(image_path)

        if self.transforms is not None:
            image = self.transforms(image)

        return image, label
        # return filename, bbox # 과제 양식

    def __len__(self): ## 보유한 샘플 수 를 반환
        return len(self.all_data_path)

temp = MyCustomDataset("./dataset")

for i in temp:
    print(i)
    # image01 xywh