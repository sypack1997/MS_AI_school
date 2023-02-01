import os
import glob
import cv2
import json

categories = ["food_truck", "street_vendor" "sit_board", "garbage_bag"]
current_index = 0

for category in categories:
    category_img_path = os.path.join("./park_data/train/images/illegal", category)
    category_label_path = os.path.join("./park_data/train/label/illegal", category)
    img_paths = glob.glob(os.path.join(category_img_path, "*.jpg"))
    label_paths = glob.glob(os.path.join(category_label_path, "*.json"))

    for i in range(len(img_paths)):
        img_path = img_paths[current_index]
        label_path = label_paths[current_index]
        print(img_path)
        with open(label_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # load the image using cv2.imread
        img = cv2.imread(img_path)

        # get the height and width of the image
        height, width = img.shape[:2]

        # resize the image to a smaller size
        img = cv2.resize(img, (int(width / 2), int(height / 2)))

        for annotation in data['annotations']:
            object_class = annotation['object_class']
            x1, y1 = annotation['bbox'][0]
            x2, y2 = annotation['bbox'][1]

            # adjust the bounding box coordinates according to the image ratio
            x1, y1 = int(x1 / 2), int(y1 / 2)
            x2, y2 = int(x2 / 2), int(y2 / 2)

            cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,0),2)
            cv2.putText(img, f"{object_class}", (int(x1), int(y1)+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

        cv2.imshow("test",img)
        key = cv2.waitKey()
        if key == ord('q'):
            exit()
        elif key == ord('d'):
            current_index = max(0, current_index - 1)
        else:
            current_index = min(len(img_paths) - 1, current_index + 1)
