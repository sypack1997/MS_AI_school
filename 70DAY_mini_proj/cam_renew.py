## 2022 MSAI SCHOOL 4팀 [한글 지화 이미지 분류 프로젝트: 웹캠 시현 모듈]
import os
import torch
import cv2
from PIL import ImageFont, ImageDraw, Image
import torch.nn.functional as F
import torchvision.models as models
import torch.nn as nn
from torchvision import transforms
import numpy as np
import keyboard
import torchvision
from unicode import join_jamos


labels = {
    'ㄱ': 0, 'ㄴ': 1, 'ㄷ': 2, 'ㄹ': 3, 'ㅁ': 4, 'ㅂ': 5, 'ㅅ': 6, 'ㅇ': 7, 'ㅈ': 8, 'ㅊ': 9,
    'ㅋ': 10, 'ㅌ': 11, 'ㅍ': 12, 'ㅎ': 13, 'ㅏ': 14, 'ㅑ': 15, 'ㅓ': 16, 'ㅕ': 17, 'ㅗ': 18,
    'ㅛ': 19, 'ㅜ': 20, 'ㅠ': 21, 'ㅡ': 22, 'ㅣ': 23, 'ㅐ': 24, 'ㅒ': 25, 'ㅔ': 26, 'ㅖ': 27,
    'ㅢ': 28, 'ㅚ': 29, 'ㅟ': 30
}
korean = dict(map(reversed, labels.items()))
# print(korean)
# exit()

#-----------------------------------------------------------------------------
data_transforms = transforms.Compose(
    [
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # model = models.vgg19_bn(pretrained=False)
# # model.classifier[6] = nn.Linear(in_features=4096, out_features=3)
# model = models.mobilenet_v3_large(pretrained=False)
# model.classifier[3] = nn.Linear(in_features=1280, out_features=33)

model =  torchvision.models.swin_t(weights="IMAGENET1K_V1")
model.head = torch.nn.Linear(in_features=768, out_features=31)
model.to(device)

model.load_state_dict(torch.load("swin_aug_best.pt", map_location=device))
# model = model.to(device)
model.eval()

#-----------------------------------------------------------------------------
with torch.no_grad():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    # 출력대상 리스트
    vowelsNconsonants = []
    word_list = "대기 중..."

    while True:
        ret, frame = cap.read()
        # 왜 RGB 변환을 2번 해야 되는걸까?
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(frame)
                                    # reshape() 보다 언스퀴즈 하는게 코드 수정이 덜함
        input_img = data_transforms(pil_img).unsqueeze(0).to(device)
        out = model(input_img)
        softmax_result = F.softmax(out)
        top1_prob, top1_label = torch.topk(softmax_result, 1)
        print(top1_prob, korean[top1_label.item()])
        acc = ": " + str(round(top1_prob.item()*100, 3)) + "%"

        b, g, r, a = 0, 0, 0, 0
        fontpath = "fonts/gulim.ttc"
        font = ImageFont.truetype(fontpath, 100)
        font_word = ImageFont.truetype(fontpath, 50)

        # keyboard 라이브러리를 이용한 키값 이벤트 조건
        if keyboard.is_pressed("s"):  # select
            vowelsNconsonants.append(korean[top1_label.item()])

            # print(vowelsNconsonants)
        if keyboard.is_pressed("d"):  # delete
            try:
             del vowelsNconsonants[-1]
             # out of range err 방지
            except:
                pass

        word_list = "".join(vowelsNconsonants)

        if keyboard.is_pressed("c"):  # combination
            word_list = join_jamos(word_list)
            vowelsNconsonants = word_list

        if keyboard.is_pressed("r"):  # reset
            vowelsNconsonants = []
            word_list = []

        print("현재 리스트에 포함된 자모 >>>", vowelsNconsonants)
        print(word_list)

        draw = ImageDraw.Draw(pil_img)
        draw.text((30, 40), korean[top1_label.item()], font=font, fill=(b, g, r, a))
        draw.text((90, 380), str(word_list), font=font_word, fill=(255,127,0))
        img = np.array(pil_img)

        # cv2.putText(frame, korean[top1_label.item()], (10, 100), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 255, 0), 2)
        cv2.putText(img, acc, (30, 180), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
        cv2.rectangle(img, (80, 370), (550, 450), (34, 139, 34), 3)

        cv2.imshow("TEST", cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # cv2.imshow("TEST", img)
        if cv2.waitKey(50) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()




