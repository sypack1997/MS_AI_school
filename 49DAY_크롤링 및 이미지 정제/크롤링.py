from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import urllib.request


'''
폴더 구성
'''
def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        pass
    except OSError:
        print("error : Creating dirtectory..." + directory)


'''
키워드 입력, chromedriver 실행
'''
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

keyword = '사과'
chromedriver_path = "./chromedriver.exe"
driver = webdriver.Chrome(chromedriver_path, options=options)
driver.implicitly_wait(3)

### 키워드 입력 Selenium 실행
driver.get("https://www.google.co.kr/imghp?h1=-ko")
elem=driver.find_element_by_name("q")
elem.send_keys(keyword)
elem.send_keys(Keys.RETURN)

# xpath 주소 따는 법
# 홈페이지 F12 -> 'select element' 버튼 -> 주소 위치 선택 후 Elements 코드 copy -> 'copy XPath' 선택
# elem=driver.find_element_by_xpath("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")

### 스크롤
print(keyword + '스크롤 중...')
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

print(keyword + "찾은 이미지 개수: ", len(links))
print(links)
time.sleep(2)

### 데이터 다운로드
create_folder('./' + keyword + '_img__download')
for index, i in enumerate(links):
    url = i
    start = time.time()
    urllib.request.urlretrieve(url, "./" + keyword + "_img__download/" + keyword + "_" + str(index) + ".jpg")
    print(str(index) + "/" + str(len(links)) + " " + keyword + "다운로드 시간 ------: ", str(time.time() - start)[:5] + "초")

print(keyword + "다운로드 완료!!")