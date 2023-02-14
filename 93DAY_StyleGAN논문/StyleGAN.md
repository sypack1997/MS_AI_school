## 1. 논문소개

고화질 이미지 생성에 적합한 아키텍처를 제안한다.

- **PGGAN 베이스라인** 아키텍처의 성능을 향상
- **Disentanglement**(다양한 특징들이 잘 분리되어 있는 것) **특성을 향상**

>> semantic feature들을 잘 컨트롤 

- 고해상도 얼굴 데이터셋(FFHQ) 발표

## 2. 관련논문

1. Generative Adversarial networks(GAN)
    
    생성자(generator)와 판별자(discriminator) 두개의 네트워크를 활용한 생성 모델.
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e8ae75eb-3444-4c38-b59c-ebefaee0d937/Untitled.png)
    
    G(z) : 새로운 데이터
    
    D(x) : 확률 - 실제 분포에서 나온 샘플
    
    **>>** **초기 GAN은 성능이 좋지않고, 네트워크가 수렴하는것이 불안했다.**
    
2. DCGAN
    
    Deep Convolutional Layers를 이용하여 이미지 도메인에서의 높은 성능을 보인다.
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/d73b9eda-a3d8-4636-afb8-f2396402cf77/Untitled.png)
    
    채널의 수는 줄이면서 크기와 높이를 증가시키는 upsampling 방법
    
    **DCGAN에서의 Convolutional 필터**
    
    - G : Transposed Convolution - 너비와 높이가 증가(해상도증가) - Upsampling
    - D : Strided Convolution - 너비와 높이가 감소하면서 채널 증가
    
    **DCGAN에서의 벡터 연산(Vector Arithmetic)**
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/0a6d9301-0c80-4c48-a8ed-421a485ccca1/Untitled.png)
    
    latent vectors(z)를 통해 연산을 수행하여 의도한 feature를 가지는 z를 만들 수 있다.
    
    **>>** **고성능의 생성모델을 학습할 수 있음.**
    
3. WGAN-GP
    
    WGAN은 함수가 1-Lipshichtz 조건을 만족하도록하여 안정적인 학습을 유도 → **초기 GAN의 문제였던 네트워크 수렴의 안정성을 증가시킴**.
    
    WGAN-GP에서는 gradient penalty를 이용하여 WGAN의 성능을 개선.
    
    **>> StyleGAN에서도 WGAN-GP loss가 사용됨**
    
4. Progressive Growing of GANs(PGGAN = ProGAN)
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/57fb2cca-8477-46d4-87ae-ff153088cb55/Untitled.png)
    
    **메인아이디어**
    
    - 학습과정에서 레이어를 추가 (한 layer씩 학습하여 점진적으로 이미지 해상도를 증가시킨다)
    - 안정적으로 고해상도 이미지 학습 성공
    - 학습의 속도가 빠름
    
    **한계점**
    
    - 이미지의 특징 제어가 어렵다.
    
    **Architecture**
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/b0d4e95d-2d64-407c-aaf5-f3c36161a0a3/Untitled.png)
    
    학습을 진행하는 과정에서 점진적으로 네트워크의 레이어를 붙여 나간다.
    
    **>> PGGAN을 baseline으로 하여 StyleGAN에서 문제점을 개선**
    
5. Adaptive Instance Normalization (ADaIN)
    
    AdaIN을 이용하면 **다른 원하는 데이터로부터 스타일 정보를 가져와 적용**할 수 있다.
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6c423744-37a9-4973-963c-0c2d3cd18577/Untitled.png)
    
    - 학습시킬 파라미터 필요X
    - **feed-forward 방식(네트워크에 이미지를 넣고 스타일에 대한 정보를 넣어주어서 style transfer가 수행된 결과를 얻도록 만드는 방식의 네트워크)의 style transfer 네트워크에서 사용**되어 좋은 성능을 보인다. → 해당 방식을 사용하여 StyleGAN이라는 이름으로 불리게 됬다.
    
    >> 하나의 이미지를 생성할 때, 여러개의 스타일 정보가 레이어를 거칠 때마다 입혀질 수 있도록 하는 방법 
    

## 3. StyleGAN의 핵심 아이디어

1. 매핑 네트워크(Mapping Network)
    - 512차원의 z 도메인에서 w 도메인으로 매핑을 수행한다.
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/1bf87742-1ab6-4531-8995-bb6a43a6e002/Untitled.png)
    
    (a) 실제 학습데이터가 가지는 분포
    
    (b) 가우시안 분포에서 샘플링한 z 벡터 → 특징들이 바뀌는 현상을 확인
    
    (c) Linear space에서 특징들이 분리되는 형태로 학습될 수 있음
    
    **>> StyleGAN의 생성자는 더욱 linear하며 덜 entangled되어 있다.**
    
2. Style Modules (AdaIN)
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c93ba2e1-61c1-4523-b2a8-ff1917fb09c8/Untitled.png)
    
     Latent w를 뽑은다음에 style형태(AdaIn에 들어가는 스타일 정보가 될 수 있도록 변환 후.)로서 생성 네트워크에 적용된다. 
    
    **>> 스타일 정보가 반영되도록 만듦으로써 하나의 고해상도 이미지가 만들어지는 과정에서 다양한 스타일들이 반영되도록 하여 합성된 하나의 결과 이미지를 볼 수 있다.**
    
3. Removing Traditional Input
    
    PGGAN에서는 하나의 latent벡터를 만든 후 생성 네트워크에 넣어 하나의 새로운 이미지가 만들어는 반면, **StyleGAN의 경우 스타일 정보가 layer를 거치는 과정에서 적용될 수 있도록 함으로서 이미지의 다양성이 보장됨.** 
    
    **>> 초기 입력을 상수로 대체하여 성능향상**
    
4. Stochastic Variation
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/292e9e6e-4ef8-4a48-92f3-a5e4616426b3/Untitled.png)
    
    **다양한 확률적인 측면을 컨트롤할 수 있다.**
    
    별도의 **noise input을 넣어서 각각의 layer마다 noise 정보를 넣다.**
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e6d2a502-6abe-41b7-a7aa-0eb20f044a7e/Untitled.png)
    
    (a) 모든 레이어에 노이즈 적용
    
    (b) 노이즈 적용 X
    
    (c) Fine layer
    
    (d) Coarse layer
    
    **노이즈(주근깨, 피부 모공 등)**
    
    - Coarse noise : 큰 크기의 머리 곱슬거림, 배경 등
    - Fine noise : 세밀한 머리 곱슬거림, 배경 등
    
    **스타일(얼굴형, 포즈 등)**
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/a8c0d531-35f6-4a06-8e5d-0f50f3266adf/Untitled.png)
    
5. Style Mixing (Mixing Regularization)
    
    인접한 레이어간의 스타일 상관관계를 줄인다. (크로스오버 포인트 설정 → w1, w2)
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e86f1c4e-cc89-4fa9-98a1-e1052f8f0aa8/Untitled.png)
    
    **>> 다양한 스타일들이 서로 잘 분리될 수있도록 적용** 
    

## 4. Evaluation

1. FID 값 비교

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/592f4a62-e6ee-43de-a71e-9fa1e4cd1e2a/Untitled.png)

1. Disentanglement 관련 두 가지 성능 측정 지표 제안

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/b491fdc2-901a-4e12-beb2-930a56d34c65/Untitled.png)

- Path Length : 두 벡터를 보간(interpolation)할 때 **얼마나 급격하게** 이미지 특징이 바뀌는지
- Separability : latent space에서 attributes가 **얼마나 선형적으로 분류**될 수 있는지 평가

**>> 다양한 feature들이 잘 분리되어 컨트롤 하기 용이하다.**