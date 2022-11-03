### 1. Ubuntu(리눅스) 가상환경 시스템 준비

- Docker 환경 세팅
    - Azure Ubuntu Server 20.04LTS에서 환경 준비
    
    ```powershell
    # cmd Ubuntu 가상환경 준비
    ssh sypack1997@공용 IP주기
    
    # docker image down (각각의 상태를 저장해 놓은 파일)
    sduo apt-get update # sudo : 관리자 권한을 가진다.
    sudo apt-get upgrade
    
    # docker package 설치
    sduo pat-get install \apt-transport-https\curl\gnupg\lsb-release
    
    # docker 암호화 관련 key 설치
    fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    echo \
    "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archivekeyring.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list >
    /dev/null
    
    # docker 관련 파일 설치
    sudo pat-get update
    sudo apt-get install docker-ce docker-ce-cli continerd.io
    
    # 설치확인
    sudo docker run hello-world
    
    # 사용자 권한 주기
    sudo usermod -a -G docker $USER
    sudo service docker restart
    exit
    ssh sypack1997@공용 IP주기
    
    # 컨테이너 실행 및 확인
    docker pull ubuntu:18.04
    docker images
    docker ps
    docker ps -a
    
    # 컨테이너 쌓기 및 확인
    docker run -it --name demo1 ubuntu:18.04 /bin/bash
    docker run -it -d --name demo2 ubuntu:18.04
    docker ps
    docker exec -it demo2 /bin/bash
    
    # 컨테이너 실시간 확인
    docker run --name demo3 -d busybox sh -c "while true; do $(echo date);
    sleep 1; done"
    
    # 컨테이너 제거 및 확인
    docker logs demo3
    docker logs demo3 -f
    
    docker stop demo3
    docker stop demo2
    docker stop demo1
    
    docker rm demo3
    docker rm demo2
    docker rm demo1
    
    docker images
    # busybox, ubuntu 가 있는 것을 확인하실 수 있습니다.
    docker rmi ubuntu
    ```
    
- Dockerfile 만들기
    
    ```powershell
    
    ```
    
- Docker Hub (에디터 사용)
    
    ```powershell
    # Docker lohin
    $ docker login
    username, password 입력
    Login Succeeded!
    
    # Docker Hub를 바라보도록 tag생성
    $ docker tag my-image:v1.0.0 koreaeva/my-image:v1.0.0
    docker tag <image_name>:<tag_name> <user_name>/<image_name>:<tag>
    
    # Docker image push to Docker Hub
    $ docker push koreaeva/my-image:v1.0.0
    docker push <user_name>/<image_name>:<tag>
    
    # Docker hub 접속 후 업로드한 이미지 확인
    ```