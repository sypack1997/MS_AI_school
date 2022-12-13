from PIL import Image
import os

def expand2square(pil_img, background_color):
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        # image add(추가 이미지, 붙일 위치(가로, 세로))
        result.paste(pil_img, (0,(width - height) // 2))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result


def image_file(image_folder_path):
    all_root = []
    for (path, dir, files) in os.walk(image_folder_path):
        for filename in files:
            # image.xml -> .xml
            ext = os.path.splitext(filename)[-1]
            if ext == ".jpg" or ext == ".png" :
                root = os.path.join(path, filename)
                # ./cavt_annotations/annotations.xml
                all_root.append(root)
            else:
                print("no xml file..")
                break
    return all_root


img_path_list = image_file("./images/")

for img_path in img_path_list:
    image_name_temp = os.path.basename(img_path)
    image_name = image_name_temp.replace(".jpg", "")

    img = Image.open(img_path)
    img_new = expand2square(img, (0, 0, 0)).resize((224, 224))
    os.makedirs("./resize", exist_ok=True)
    img_new.save(f"./resize/{image_name}.png", quality=100)