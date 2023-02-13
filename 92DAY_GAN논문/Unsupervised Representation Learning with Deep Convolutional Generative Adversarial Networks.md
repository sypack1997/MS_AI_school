## Abstract

CNN이 비지도학습에서 빛을 보지 못하고 있을때, DCGANs라는 CNN기반의 GANs 네트워크를 제시하며 비자도학습에서도 사용될 수 있다고 주장했다. Object의 part에서 scene으로 표현 방법들의 계층을 G(generator)와 D(discriminator) 모두 학습하며, 학습된 특징을 특성 tasks에 사용할 수 있다고 한다.

## 1. Introduction

기존의 GAN은 학습하기 불안정했고, 떄때로 이상한 결과를 만드는 G가 발생했습니다. 

본 논문은 다음과 같이 contributions한다.

- 안정적인 training이 가능한 Deep Convolutional GANs(DCGAN)을 제안
- 이미지 분류를 위한 학습된 D를  사용하여, 다른 비지도 알고리즘들보다 경쟁적인 성능을 보여준다.
- GAN의 filter를 시각화하여, filter가 어떤 특정 objects를 그리는지 보여준다.
- 쉽고 다양한 segmentic 단위의 조작이 가능

## 2. Approach and Model Architecture

CNN 아키텍쳐의 변화된 부분은 아래 3가지이다.

1. **먼저 Pooling layer가 없고, 대신에 strided convolution을 사용하여 신경망이 spatial downsampling을 학습하도록 한다. 이러한 방법을 G, D에 적용하여 스스로 spatial upsampling을 학습하도록 한다.**
2. convolutional features 위에 Fully connected hidden layers 를 두지 않는 방식이다.
3. **G와 D 모두 batch normalization을 사용한다.** 이는 깊은 모델의 gradient flow를 도와주며, GAN에서 흔히 관측되는 모든 샘플들이 하나의 point를 생성하는 것을 방지해준다. 하지만 모든 layer에 batchnorm을 사용하는 것은 불안정성을 도래할 수 있다. 이에, **G의 output layer와 D의 input에는 사용하지 않는다.**

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/2236af6b-3601-4463-9937-1a418abd7ae9/Untitled.png)

## 5. Details if Adversarial Training

G는 latent space vector(z)fmf data-space에 mapping하는 역할

>> z를 data-space로 매핑하는 것은 훈련 이미지들과 동일한 사이즈를 가지는 RGB이미지들을 만든다. 이는 연속된 strided convolution을 거치며, 각각은 아래 그림처럼 2d batch-norm과 relu activation이 이어진다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/65f71854-8e42-418c-b023-4e3adb180b01/Untitled.png)

G의 output은 tanh 활성화 함수를 통과하여 [-1,1]사이의 출력값을 받게 된다. 특히 conv layer이후에 오는 batchNorm layer는 논문에서 언급했듯 중요한데, **훈련시 gradient-flow에 도움을 주어 학습이 잘되도록 한다.** Input section인 (nz, ngf, nc)는 G 구조에 영향을 끼치는데, **nz는 z input vector의 길이(dim), ngf는 G에서 propagation이 일어나는 feature map의 크기, nc는 ouput image의 채널 수 를 의미한다.**

D는 input 이미지에 대해 real, fake로 판단하는 확률을 출력하는 binary classifier다.

D는 3x64x64의 입력 이미지를 받고, **Conv2d, BatchNorm2d, LeakyRelu 계층**을 거쳐 최종적으로 sigmoid를 통과하여 출력값을 반환한다.

>> **pooling 대신 strided Conv를 사용하는 이유는 신경망이 스스로 pooling을 학습하기 때문이다. BatchNorm과 Relu는 gradient flow에 도움을 주어 G와 D가 잘 학습하도록 도와준다.**

G의 학습과정을 추적하기 위해 고정된 가우시안 분포로부터 생성된 latent vector의 배치를 만든다. 훈련과정에서 fixed_noise 배치를 G에 넣어주고, 수많은 반복 이후 노이즈로부터 생성된 이미지들으 살필 수 있다.

## 3. **Emprical Validation of DCGANs Capabilities**

지도학습의 이미지 분류에서도 좋은 성능을 보여준다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c9685060-37a0-4d4f-ab45-2c7b98044280/Untitled.png)

## 4. **Investigating and Visualizing the Internals of the networks**

먼저 latent space(잠재적 공간) 접근에 대한 실험을 진행했다. latent space에서의 접근이 이미지 생성에 있어서 semantic change을 줄 수 있는지 실험해보았고, 모델이 relevant하고 interesting한 representations을 학습한다는 것을 추론할 수 있었다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/a9260d5a-44c8-4006-8481-8c793468c41c/Untitled.png)

위의 그림처럼 Z의 random points들을 interpolinate(선형보간)한 결과 위와 같이 그럴듯한 침실 사진들을 만들어 내는 것을 보여준다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/99ce152f-46a4-4e9f-a539-b15cc2295542/Untitled.png)

위 그림과 같이 **latent space vectors(z)의 결과들에 대한 산술 연산적인 특징을 설명 할 수 있다.**

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f762554a-25dc-410f-8065-a8c3d0a57823/Untitled.png)

또한 Interpolination을 사용하여 결과의 pose를 바꿀 수 도 있다.

## 5. Conclusion

안정적인 아키텍쳐 구조의 DCGAN을 제안하면서 Image representations이 좋아지는 것을 보여주었습니다. 하지만 train을 길게 하면 subset of filters들이 붕괴되고 하나의 단일 모드로 붕괴된다는 불안정성이 있다.