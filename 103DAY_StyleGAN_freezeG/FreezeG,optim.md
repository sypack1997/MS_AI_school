# StyleGAN2-ada 중간 점검

1주차 (2/13 ~ 2/16)
- GAN 논문리뷰
- 예제 및 튜토리얼 실습, 학습 및 인퍼런스

2주차 (2/20 ~ 2/24)
- 학습데이터셋 전처리 방법 설정 및 수집
- 디즈니 데이터셋 수집 및 학습 & 인퍼런스

3주차 (2/27 ~ 3/1)
- 데이터수집 및 학습 + blend하여 가상인물 만들기

-------------------------------------

## StyleGAN-ada
- 데이터가 많을떈 aug가 역효과
- 강한 Aug 사용 = 오버피팅 감소 but, 학습시간이 늘어남
- ada 사용시 freezed 사용하면 성능이 더 좋아진다.
 >> 적은 데이터셋은 판별자가 오버피팅이 잘되기 떄문에 이를 방지하기 위해 동적 p 값을 가진 augmentation을 적용하여 학습

-------------------------------------

## 현재 상황
- kimg 값을 높게 주어 학습
    >> 최대 3000kmig까지 해보았지만 유의미한 결과X
- belnd주기(+ freezed)
    >> network1(FFHQ)과 network2(전이학습한 캐릭터 모델)의 순서 및 layer 범위 조정을 통해 이미지 변환값을 얻을 수 있음
    하지만 퀄리티 만족 X
    >> 전이학습 진행 시 freezed값을 주어 학습속도를 향상시키고 전이모델을 형성할 수 있음. (값을 크게 줄수록 많이 뭉개짐. 환경에 맞는 적절한 값을 찾아야함 = 2)
- freezeg 추가 및 optimizer Adam -> AdamW -> Adabeilif
 
-------------------------------------

## 소소한 파라미터 변화
- Augpipe값 변화
    'custom1': dict(xflip=1, xint=1, scale=1, xfrac=1, brightness=1, contrast=1, hue=1, saturation=1),'custom2': dict(xflip=1, xint=1, rotate90=1, scale=1, xfrac=1, brightness=1, contrast=1, hue=1, saturation=1, imgfilter=1, cutout=1)

- 스타일별 분류
    1. Coarse = w0-w2 (4x4 -8x8) 저해상도, 이미지의 큰 구조 즉 얼굴모양, 피부색, 성별, 연령 변경
    2. Middle = w3-w4(16x16-32x32) 중간해상도, Coarse스타일보다 두 잠재변수가 더 중간값으로 섞임
    3. Fine = w5-w6(64x64-1024x1024) 고해상도, 배경과 머리색만 영향을 받고 매우 미세한 변경만 있음. 

-------------------------------------

## 금일 추가된 FreezeG 및 optimizer 수정 코드 내역
- persistence는 torch_utils 안에 것으로 대체
- train -> freezeG 기능 추가 (optim = AdamW)

- 이후 adabelief 코드 추가
    사용하려면 train.py와 training 폴더안에 trainig_loop.py수정해야한다.
    (train_optim_adabelief.py 폴더 추가했습니다.)