import cv2
import mediapipe as mp
import numpy as np
import keyboard
import time

# 한손만 인식
max_num_hand = 1

# 손동작 라벨 매핑
gesture = {
    0: 'ㄱ', 1: 'ㄴ', 2: 'ㄷ', 3: 'ㄹ', 4: 'ㅁ', 5: 'ㅂ', 6: 'ㅅ', 7: 'ㅇ', 8: 'ㅈ', 9: 'ㅊ',
    10: 'ㅋ', 11: 'ㅌ', 12: 'ㅍ', 13: 'ㅎ', 14: 'ㅏ', 15: 'ㅑ', 16: 'ㅓ', 17: 'ㅕ', 18: 'ㅗ',
    19: 'ㅛ', 20: 'ㅜ', 21: 'ㅠ', 22: 'ㅡ', 23: 'ㅣ', 24: 'ㅐ', 25: 'ㅒ', 26: 'ㅔ', 27: 'ㅖ',
    28: 'ㅢ', 29: 'ㅚ', 30: 'ㅟ', 31: 'spacing', 32: 'clear'
}

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
# hands = mp_hands.Hands(
#     # 한손만 인식하도록 설정
#     max_num_hands=max_num_hand,
#     # 탐지랑 트랙킹 시간(?)q
#     min_detction_confidence=0.5,
#     min_tracking_confidence=0.5)

# test파일 지정
f = open('test.txt', 'w')

file = np.genfromtxt('dataSet.txt', delimiter=',')
motionFile = file[:,:-1]
labelFile = file[:,-1]
angle = motionFile.astype(np.float32)
label = labelFile.astype(np.float32)
knn = cv2.ml.KNearest_create()
knn.train(angle, cv2.ml.ROW_SAMPLE, label)
cap = cv2.VideoCapture(0)

with mp_hands.Hands(	# 손가락인식 초기화
    max_num_hands=1,	# 인식할려는 손의 수
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
    ) as hands:

    startTime = time.time()
    prev_index = 0
    sentence = ''
    recognizeDelay = 1
    while True:
        ret, img = cap.read()
        if not ret:
            continue
        imgRGB = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        result = hands.process(imgRGB)

        if result.multi_hand_landmarks is not None:
            for res in result.multi_hand_landmarks:  # 여러개의 손을 인식 할 수 있으니까, for문 반복
                joint = np.zeros((21, 4))  # 손 관절 (joint) 넘파이 배열로 생성
                for j, lm in enumerate(res.landmark):  # media pipe의 landmark를 반복하며 joint에 대입
                    joint[j] = [lm.x, lm.y, lm.z, lm.visibility]

                # 벡터를 구하기 위해 생성하는 v1,v2 (v2에서 v2을 빼면 v백터가 된다)
                v1 = joint[[0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19], :3]
                v2 = joint[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], :3]

                v = v2 - v1
                v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]  # 정규화

                # 만들어진 벡터들 사이의 각도를 구한다
                compareV1 = v[[0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18], :]  # 각 벡터의 각도를 비교하기 위해 생성하는 compare벡터
                compareV2 = v[[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], :]

                angle = np.arccos(np.einsum('nt,nt->n', compareV1, compareV2))  # compare벡터를 사용하여 각도를 구함
                angle = np.degrees(angle)

                if keyboard.is_pressed('a'):  # a를 누를시 현재 데이터(angle)가 txt파일에 저장됨
                    for num in angle:
                        num = round(num, 6)
                        f.write(str(num))
                        f.write(',')
                    f.write("32.000000")  # 학습시키고자 하는 동작의 라벨
                    f.write("\n")
                    print("next")

                data = np.array([angle], dtype=np.float32)
                ret, result, neighbors, dist = knn.findNearest(data, 3)
                index = int(result[0][0])
                if index in gesture.keys():
                    if index != prev_index:
                        startTime = time.time()
                        prev_index = index
                    else:
                        if time.time() - startTime > recognizeDelay:
                            if index == 26:
                                sentence += ' '
                            elif index == 27:
                                sentence = ''
                            else:
                                sentence += gesture[index]
                            startTime = time.time()

                    cv2.putText(img, gesture[index], (int(res.landmark[0].x * img.shape[1] - 10), int(res.landmark[0].y * img.shape[0] + 40)),
                               cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 3)
                mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)
        cv2.putText(img, sentence, (20, 440), cv2.FONT_HERSHEY_DUPLEX, 2, (255,255,255), 3)

        cv2.imshow('HandTracking', img)
        cv2.waitKey(1)
        if keyboard.is_pressed('q'):
            break












