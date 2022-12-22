from torch.utils.data import Dataset
from xml.etree.ElementTree import parse

def box_xyxy(image_metas):
    list_box = []


class CustomDataset(Dataset):
    def __init__(self, dataset_path, xml_path, transform = None):
        self.dataset_path = dataset_path
        self.xml_path = xml_path
        

    def __getitem__(self, index):
        image_path = self.dataset_path[index]
        xml_path = self.xml_path[index]
        tree = parse(xml_path)
        root = tree.getroot()
        image_metas = root.findall("image")

        box = box_xyxy(image_metas)
        print(box)

        return image, box

    def __len__(self):
        return len(self.dataset_path)


image_path = ["./01.jpg"]
xml_path = ["./annotations.xml"]
test = CustomDataset(image_path, xml_path, transform=None)

## 디버깅
for i in test:
    print(i)