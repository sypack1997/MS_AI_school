import cv2
import torch
import numpy as np

# label_dict = {0: 'Iran', 1: 'Ball', 2: 'GK', 3: 'Referee', 4: 'Korea'}
label_dict = {0: 'player', 1: 'Ball', 2: 'keeper', 3: 'Referee'}

color_dict = {
    'away': (255, 0, 0),
    'Ball': (0, 255, 0),
    'keeper': (0, 0, 0),
    'Referee': (255, 255, 0),
    'home': (0, 0, 255)
}

# device setting
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#  model call
model = torch.hub.load('ultralytics/yolov5', 'custom', path='./runs/train/exp_0208/weights/v5x_best.pt')
model.conf = 0.25  # NMS confidence threshold
model.iou = 0.45  # NMS IoU threshold
model.to(DEVICE)

videofile = './dataset/football.mp4'

cap = cv2.VideoCapture(videofile)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (int(width), int(height)))

if cap.isOpened():
    while True:
        ret, img = cap.read()
        if ret:
            # model input
            output = model(img, size=640)
            bbox_info = output.xyxy[0]

            for bbox in bbox_info:
                x1 = int(bbox[0].item())
                y1 = int(bbox[1].item())
                x2 = int(bbox[2].item())
                y2 = int(bbox[3].item())

                score = round(bbox[4].item(), 4)
                label_number = int(bbox[5].item())

                patch = img[y1:y2, x1:x2, :]

                hsv = cv2.cvtColor(patch, cv2.COLOR_BGR2HSV)

                lower_red = (0, 70, 50)
                upper_red = (10, 255, 255)

                mask = cv2.inRange(hsv, lower_red, upper_red)
                red_percent = cv2.countNonZero(mask) / (patch.shape[0] * patch.shape[1])

                # if red_percent > 0.05:
                #     label_number = 0

                label = label_dict[label_number]
                if label == 'player':
                    if red_percent > 0.055:
                        label = 'home'
                        color = color_dict[label]
                    else:
                        label = 'away'
                        color = color_dict[label]

                color = color_dict[label]

                cv2.rectangle(img, (x1, y1), (x2, y2), color, 1)
                cv2.putText(img, label, (int(x1), int(y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)


            cv2.imshow(videofile, img)
            out.write(img)

            if cv2.waitKey(33) == ord('q'):
                break
        else:
            break
else:
    print("Can't open video.")
cap.release()
cv2.destroyAllWindows()