from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import urllib.request
from multiprocessing import Pool
import pandas as pd


'''
폴더 구성
'''
def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("error : Creating dirtectory..." + directory)


def image_download(keywords):
    create_folder('./' + keywords + '_img_resolution')
    
    # 크롬 드라이버 호출
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    chromedriver = "./chromedriver.exe"
    driver = webdriver.Chrome(chromedriver, options=options)
    driver.implicitly_wait(3)

    # 검색
    print('검색>>', keywords)
    driver.get("https://www.google.co.kr/imghp?h1=-ko")
    keyword=driver.find_element_by_name("q")
    keyword.send_keys(keywords)
    keyword.send_keys(Keys.RETURN)

    # 스크롤 내리기 -> 결과 더보기 버튼 클릭
    print(keywords + '스크롤 중...')
    elem=driver.find_element_by_tag_name('body')
    for i in range(60):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)

    try:
        driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div[2]/div[1]/div[2]/div[2]/input').click()
        for i in range(60):
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
    except:
        pass

    links = []
    images = driver.find_elements_by_css_selector("img.rg_i.Q4LuWd") # 이미지 class name
    for image in images:
        if image.get_attribute('src') != None:
            links.append(image.get_attribute('src'))
    print(keywords + "찾은 이미지 개수: ", len(links))
    time.sleep(2)
    
    for index, i in enumerate(links):
        url = i
        start = time.time()
        urllib.request.urlretrieve(url, "./" + keywords + "_img_resolution/" + keywords + "_" + str(index) + ".jpg")
        print(str(index+1) + "/" + str(len(links)) + " " + keywords + "다운로드 시간 ------: ", str(time.time() - start)[:5] + "초")
    print(keywords + "다운로드 완료!!")


# 검색 키워드 호출
key = pd.read_csv('./keyword.txt', encoding='utf-8', names=['keyword'])
keyword = []
[keyword.append(key['keyword'][x]) for x in range(len(key))]
print(keyword)

# 실행
if __name__ == '__main__':
    pool = Pool(processes=3)
    pool.map(image_download, keyword)