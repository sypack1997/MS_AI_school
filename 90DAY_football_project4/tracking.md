# YOLO tracking
yolov5 -> detect_track.py 에서 실행
(argument에서 관련 값 입력하면 됨)

가끔 오류가 발생하는 경우가 있는데 이는 yolo모델 업그레이되면서 기존에 있던 models - yolo.py파일이 호환이 안되서 그런 것
-> yolov5 github에 들어가서 최신화된 yolo.py다운받은 후 적용해주면 됨.


# Hardcoding
inf.py로 만들었음.
color threshold에 따른 player 구분을 위해 따로 작성.
player의 색깔 threshold에 따라 'home'팀과 'away'팀으로 나타나도록 변경



# 차이점
영상 확인결과 yolo를 이용한 detect와 달리 inf파일에서 detection이 잘못되는 경우가 발생
ex> yolo에서는 keeper가 꾸준히 keeper로 인식되지만, inf에서는 keeper와 referee로 혼동 인식되는 경우가 있다.

>> yolo detect 시 따로 후보정해주는 값이 있는지 확인해볼 것.



# 문제점
1. 공이 player와 근접해있을때 인식이 안됨. >> 볼 점유율 계산 불가
2. color threshold detection 시 home 팀과 away팀이 혼동되는 경우 발생
3. inf.py에서의 detection과 yolov5 tracking에서의 차이