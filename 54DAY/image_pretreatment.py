import os
import glob
import argparse
from PIL import Image
# 오렌지 : Orange
# 자몽 : grapefruit
# 레드향 : Kanpei
# 천혜향 : setoka
# 한라봉 : Dekopon

# 폴더 구성 / dataset / image / 각 폴더명 생성 / 이미지 저장 (resize 400 x 400)
# 직사각형 -> 정사각형 리사이즈 비율 유지하는 함수
def expand2square(img, background_color):

    width_temp, height_temp = img.size
    print(width_temp, height_temp)
    if width_temp == height_temp:
        return img
    elif width_temp > height_temp:
        result = Image.new(
            img.mode, (width_temp, width_temp), background_color)
        result.paste(img, (0, (width_temp - height_temp) // 2))
        return result
    elif width_temp < height_temp:
        result = Image.new(
            img.mode, (height_temp, height_temp), background_color)
        result.paste(img, ((height_temp - width_temp) // 2,  0))
        return result


def image_prossing(orange_data, grapefruit_data, kanpei_data,setoka_data, dekopon_data):
    orange = orange_data
    grapefruit = grapefruit_data
    kanpei = kanpei_data
    setoka = setoka_data
    dekopon = dekopon_data
    for i in orange:
        file_name = i.split('\\')
        file_name_temp = file_name
        file_name = file_name[2]
        file_name = file_name.replace('.jpg', '.png')
        orange_img = Image.open(i)
        print(file_name_temp, orange_img)
        orange_img_resize = expand2square(
            orange_img, (0, 0, 0)).resize((400, 400))

        # 폴더 생성
        os.makedirs("./dataset/image/orange", exist_ok=True)
        orange_img_resize.save(f"./dataset/image/orange/{file_name}")

    for i in grapefruit:
        file_name = i.split('\\')
        file_name_temp = file_name
        file_name = file_name[2]
        file_name = file_name.replace('.jpg', '.png')
        grapefruit_img = Image.open(i)
        print(file_name_temp, grapefruit_img)
        grapefruit_img_resize = expand2square(
            grapefruit_img, (0, 0, 0)).resize((400, 400))

        # 폴더 생성
        os.makedirs("./dataset/image/grapefruit", exist_ok=True)
        orange_img_resize.save(f"./dataset/image/grapefruit/{file_name}")

    for i in kanpei:
        file_name = i.split('\\')
        file_name_temp = file_name
        file_name = file_name[2]
        file_name = file_name.replace('.jpg', '.png')
        kanpei_img = Image.open(i)
        print(file_name_temp, kanpei_img)
        kanpei_img_resize = expand2square(
            kanpei_img, (0, 0, 0)).resize((400, 400))

        # 폴더 생성
        os.makedirs("./dataset/image/kanpei", exist_ok=True)
        kanpei_img_resize.save(f"./dataset/image/kanpei/{file_name}")

    for i in setoka:
        file_name = i.split('\\')
        file_name_temp = file_name
        file_name = file_name[2]
        file_name = file_name.replace('.jpg', '.png')
        setoka_img = Image.open(i)
        print(file_name_temp, setoka_img)
        setoka_img_resize = expand2square(
            setoka_img, (0, 0, 0)).resize((400, 400))

        # 폴더 생성
        os.makedirs("./dataset/image/setoka", exist_ok=True)
        setoka_img_resize.save(f"./dataset/image/setoka/{file_name}")

    for i in dekopon:
        file_name = i.split('\\')
        file_name_temp = file_name
        file_name = file_name[2]
        file_name = file_name.replace('.jpg', '.png')
        dekopon_img = Image.open(i)
        print(file_name_temp, dekopon_img)
        dekopon_img_resize = expand2square(
            dekopon_img, (0, 0, 0)).resize((400, 400))

        # 폴더 생성
        os.makedirs("./dataset/image/dekopon", exist_ok=True)
        dekopon_img_resize.save(f"./dataset/image/dekopon/{file_name}")


def image_file_check(opt):
    # --image-folder-path
    image_path = opt.image_folder_path
    print(image_path)
    # 각 폴더별 데이터 갯수 체크
    orange_data = glob.glob(os.path.join(image_path, "orange", "*.jpg"))
    print("orange_data len >> ", len(orange_data))

    grapefruit_data = glob.glob(os.path.join(image_path, "grapefruit", "*.jpg"))
    print("grapefruit_data len >> ", len(grapefruit_data))

    kanpei_data = glob.glob(os.path.join(image_path, "kanpei", "*.jpg"))
    print("kanpei_data len >> ", len(kanpei_data))

    setoka_data = glob.glob(os.path.join(image_path, "setoka", "*.jpg"))
    print("setoka_data len >> ", len(setoka_data))

    dekopon_data = glob.glob(os.path.join(image_path, "dekopon", "*.jpg"))
    print("dekopon_data len >> ", len(dekopon_data))

    return orange_data, grapefruit_data, kanpei_data, setoka_data, dekopon_data

# image_path 설정
def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-folder-path", type=str, default="./image")
    opt = parser.parse_args()

    return opt

if __name__ == "__main__":
    opt= parse_opt()
    orange_data, grapefruit_data, kanpei_data, setoka_data, dekopon_data = image_file_check(opt)
    image_prossing(orange_data, grapefruit_data, kanpei_data, setoka_data, dekopon_data)