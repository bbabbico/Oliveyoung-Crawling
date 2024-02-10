from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#selenium 크롤링 기본 설정 
'''
크롬 드라이버 설치
pip install chromedriver-autoinstaller
'''

driver = webdriver.Chrome()
url = 'https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000156230&dispCatNo=90000010001&trackingCd=Home_Curation2_1&curation=recent&egcode=a901_a901&rccode=pc_main_02_c&egrankcode=1&t_page=%ED%99%88&t_click=%ED%81%90%EB%A0%88%EC%9D%B4%EC%85%982_%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_number=2'
driver.get(url)

#정적 크롤링 (품명 , 브랜드 , 메인 이미지)
name = (driver.find_element(By.CLASS_NAME,'prd_name')).text
brand = (driver.find_element(By.ID,'moveBrandShop')).text
main_img = (driver.find_element(By.ID,'mainImg'))
img =main_img.get_attribute('src')

# 동적 크롤링 (전성분)
driver.find_element(By.XPATH,'//a[@class="goods_buyinfo"]').click()
time.sleep(2)
ingredients = (driver.find_element(By.CSS_SELECTOR,'#artcInfo .detail_info_list:nth-child(8) dd')).text

#화장품 종류 입력
type=input('화장품 종류 : ')

print('상품사진 : '+img+'\n'
      +'품명 : '+name+'\n'
      +'제작회사 : '+brand+'\n'
      +'종류 : '+type+'\n'
      +'전성분 : '+ingredients)