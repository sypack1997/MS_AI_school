## 1. StyleGAN-ada pytorch

환경설정

```
- conda create -n StyleGAN_ada python=3.7
- pip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
```

StyleGAN-ada git site 접속 후 git clone

```
terminal
- git clone [https://github.com/NVlabs/stylegan2-ada-pytorch](https://github.com/NVlabs/stylegan2-ada-pytorch)
```

## 2. 사전학습된 이미지 랜덤 생성

사전 학습된 네트워크는 로컬 파일 이름 또는 URL을 사용하여 참조할 수 있는 *.pkl 파일로 저장된다.

```
ex)
python [generate.py](http://generate.py/) --outdir=./out --trunc=1 --seeds=85,265,297,849 --network=https://nvlabs-fi-cdn.nvidia.com/stylegan2-ada-pytorch/pretrained/metfaces.pkl 
```

→ out 폴더 안에 사전학습된 이미지 파일 생성됨.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/b52fae45-0d15-423d-852f-c0e8bb34f54d/Untitled.png)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/40c145bd-f06f-496e-814f-a257b74c9e93/Untitled.png)

- 다음과 같은 오류가 많이 발생한다.
    
    1) RuntimeError: Could not find MSVC/GCC/CLANG installation on this computer. Check compiler_bindir_search_path list in "C:\my\work\cuda\stylegan2\dnnlib\tflib\custom_ops.py”
    
    >> Visual Studio 설치 후 ‘C++를 사용한 데스크톱 개발’에서 MSVCv143 선택하여 설치. 
    
    >> 디폴트 값은 해당 파일이 Program Files(x86)에 설치되어야 하지만, Program Files에 설치되어 오류가 발생 -> custom_ops.py에서 def _find_compiler_bindir() 함수에 'C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Auxiliary/Build/vcvars64.bat'경로 추가.
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/055b7f70-4ad4-4f07-b388-1eefdc0fc9d6/Untitled.png)
    
    2) No module named 'upfirdn2d_plugin’
    

## 3.1 데이터셋 생성

generator target으로서 사용될 데이터셋이 필요하다. 훈련할 데이터 이미지를 다운로드 후, dataset_tool.py를 통해 GAN train에 적합한 이미지셋으로 변환해준다.

```
python dataset_tool.py --source=./avarta_dataset --dest=./dataset/dataset.zip --width=128 --height=128
```

→ dest에 변환되어 저장될 경로값을 입력한다. 변환 후,  zip파일이 생성되는데 그 안에 리사이즈된 이미지와 json파일이 있다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/64acef51-f666-451d-a2a7-3d3e9fc2797d/Untitled.png)

## 3.2 Convert Image data

대용량 데이터의 경우 다음과 같이 진행하면된다.

‘source’ 폴더 생성 후 다운받은 dataset 이미지 넣기 → ‘dest’ 폴더 생성 후 dataset_tool.py 실행 → 해당 툴을 통해 jpeg파일을 StyleGAN이 사용할 수 있는 이미지 형식(tf 레코드 형식)으로 변환해준다.

## 4. 훈련 모듈 체크

```
python train.py --outdir=./training-runs --data=./dataset/dataset.zip --dry-run
```

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/bb4b76f1-34ee-4401-8b83-72f34b9aa766/Untitled.png)

훈련될 데이터셋에 대한 정보를 확인하는 작업

## 5. 훈련모델 실행

- 오류발생
    
    1) UnicodeEncodeError: 'charmap' codec can't encode characters in position 1009-1011: character maps to <undefined>
    
    >>