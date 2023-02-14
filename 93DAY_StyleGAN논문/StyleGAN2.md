# Analyzing and Improving the Image Quality of StyleGAN(GANv2)

## 1. 논문소개

다양한 고해상도 이미지 생성을 위한 방법

- 기존의 StyleGAN보더 **더 높은 품질의 이미지 생성 및 부드럽게 변경가능**
- truncation trick : 값이 작을수록 평균(자연스러운)에 가까워지고 클수록 다양한 이미지가 만들어진다.

문제점

- AdaIN style transfer → **blob-like artifact** 발생
- Progressive growing → 얼굴의 특정부분이 fixed position을 갖는 문제 발생 (**phase artifact**)
    
    → 생성된 이미지가 인공적인 느낌을 가진다.
    

성능개선 방안

- 이미지를 latent vector로 **inversion(=mapping, 한 장의 이미지를 갖고 있을 때 그 이미지를 만들 수 있는 latent vector를 찾는 과정)**하는 새로운 알고리즘 제안
- Path length regularization(**w space에서 고정된 만큼 latent vector를 이동**시키면, 이미지 space에서도 고정된 만큼의 변화를 일으킴.)
    
    → latent interpolation에 따라서 이미지가 부드러운 변화를 보인다.
    

## 2. StyleGAN의 문제상황

1. Blob-like (Droplet) Artifacts
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/b9e1ed54-f7ec-4576-bc76-f16f27cb3804/Untitled.png)
    
    물방울 형태의 인공물이 있음.
    
    - **Adaptive instance normalization이 원인**으로 추정
    - 생성자의 activation에서 더욱 확실히 나타남
    
    >> Feature map 상에서 ****Droplet artifact가 있는경우 대부분의 이미지가 정상이지만, artifact가 없는 경우 오히려 Corrupted된 이미지가 생성될 수 있다(약 0.1% 확률)
    
    >> Latent manipulation과정에서 이미지 붕괴를 쉽게 발견할 수 있다.
    
2. Phase Artifact
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/92d870ca-6490-4241-b0bc-e366aa71574d/Untitled.png)
    
    Latent manipulation 과정에서 특정요소(teeth 등)가 고정
    
    - **Progressive growing이 원인**
    
    >> low resolution에서 높은 frequency detail 생성에 의해 형태가 고정되어버려(변경되기 어려워짐) high resolution에서 특정요소가 고정되어버림.
    

## 3. 해결방안

1. Removing Normalization artifacts
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/66f84f53-47e1-4f03-a1e0-edabd4646d03/Untitled.png)
    
    (b) AdaIN은 각 feature map의 **mean/std를 개별적으로 정규화해 서로 연관된 feature들의 정보가 소실될 수 있다**.(스타일 정보를 바꾸기 위해서 각각의 채널마다 서로 다른 방식으로 Normalization을 진행하게 되면 서로연관된 정보들이 소실된다.)
    
    (c) **standard deviation만 변경하면서**, 최대한 style block의 외부에서 feature map들의 값을 변경하고자 한다. (하지만 이 방식도 연관된 feature들의 정보를 손실될 수 있다.)
    
    (d) convolution 연산을 거친 feature map에 대해여 바로 modulation을 적용하지 않고, **weight 값만에 대하여 modulation (scaling)을 진행한다.** (서로 연결되어있는 feature들의 연관성을 덜 해친다.) → **weight demodulation**
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/92b2a24b-8e7e-4703-8e86-bab2522125df/Untitled.png)
    
    >> 직접적으로 정규화 하지않고 feature map의 statistics를 예측하여 정규화를 적용
    
    **>> 결과적으로 normalization을 demodulation으로 대체**하여 blob-like artifact가 제거된 것을 확인할 수 있다. → **Full controllability**
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/5bde8440-6bbb-4356-9e16-bdf264e8f7d8/Untitled.png)
    
2. Image Quality and Generator Smoothness
    
    PPL(Perceptual Path Length)에 따라서 image quality가 달라질 수 있다.
    
    - PPL이 낮을수록 object를 잘 생성한다.
    
    >> 좋은 이미지를 만들 수 있는 latent space의 region을 효과적으로 stretch할 수 있다. **(smaller PPL)**
    
    >> 단순히 PPL을 줄이기 어려우므로, **path length regularizer 사용**
    
    1. Lazy Regularization
        
        일반적으로 neural network를 학습할  Loss를 적용할때마다 Regularization 텀을 함께 계산해서 적용 중 → 컴퓨팅 리소스 大
        
        >> **16번의 mini-batch마다** 한번씩 regularization 적용
        
    2. Path Length Regularization
        
        방향과 상관없이 w가 일정하게 움직이는 만큼 G(w)도 일정하게(특정한 length만큼) 움직이게 된다.
        
        >> 이렇게 생성된 smoother generator가 더욱 inversion 잘된다. 
        
3. Progressive Growing Revisited
    
    치아나 눈이 부드럽게 이동하지 않는 경우 발생
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/9cbee1cd-3f14-46af-adc2-ce278cdedc2e/Untitled.png)
    
    >> **단순한 feedforward 네트워크**를 사용하는 방식 이용
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f83698ca-2528-40aa-bc86-8eea48e26048/Untitled.png)
    
    - higher-resolution 레이어에 의해서 크게 영향을 받지 않는 low resolution 이미지를 생성.
    - 처음부터 완전한 형태의 아키텍처를 구성한 상태에서 end to end로 feedforward네트워크를 활용해 학습을 진행
    
    (a) multiple skip connection을 사용해 G와 D의 해상도를 매칭.
    
    일반적인 U-net 구조(c)는 G 혹은 D 안에서만 skip connection이 사용되었지만 (a)의 경우 **G와 D 사이에서 skip connection이 사용**된다.
    
    (b) (a)구조에서 sampling을 통해 resolution을 키우는 layer
    
    **>> G는 output skips, D는 resudual net을 쓸 때 좋은 결과가 나타난다.**
    
4. Resolution Usage
    
    각 tRGB(실제 결과 이미지) 레이어가 만드는 output pixel value들의 standard deviation을 비교
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/bd293556-374f-4ac1-ba88-c49d8c9b35c9/Untitled.png)
    
    stadard deviation 값이 높다는 것은 실질적으로 결과이미지에 미치는 contribution이 크다 → 보다 다양한 pixel값들을 생성할 수 있음.
    
    (a) capcity가 부족한것을 원인으로 판단.
    
    (b) **큰 네트워크(highest-resolution layer의 feature map 개수 2배)를 사용해 성능 향상**. → Highest-resolution layer의 contribution이 증가한다.
    
5. Projection of images to latent space