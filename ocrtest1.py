import easyocr
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# setup Driver|Chrome : 크롬드라이버를 사용하는 driver 생성
driver = webdriver.Chrome('C:/chromedriver.exe')
# 사이즈조절
driver.set_window_size(1400, 1000)
driver.get('https://ticket.interpark.com/Gate/TPLogin.asp')

driver.switch_to.frame(driver.find_element(By.XPATH, "//div[@class='leftLoginBox']/iframe[@title='login']"))
userId = driver.find_element(By.ID, 'userId')
userId.send_keys('아이디')
userPwd = driver.find_element(By.ID, "userPwd")
userPwd.send_keys('비밀번호')
userPwd.send_keys(Keys.ENTER)

goodsCode = 99999989
driver.get('https://ticket.interpark.com/Ticket/Goods/GoodsInfo.asp?GoodsCode=' + '22008442')

time.sleep(1)

driver.find_element(By.XPATH, "//*[@id='popup-prdGuide']/div/div[3]/button").click()
driver.find_element(By.XPATH, "//*[@id='productSide']/div/div[2]/a[1]").click()

# 예매하기 눌러서 팝업창이 뜨면 포커스를 새창으로 바꿔준다
driver.switch_to.window(driver.window_handles[1])
# driver.get_window_position(driver.window_handles[1])

# iframe 이동
time.sleep(1)
driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmSeat']"))

# 입력해야될 문자 이미지 캡쳐하기.
capchaPng = driver.find_element(By.XPATH, "//*[@id='imgCaptcha']")

# easyocr 이미지내 인식할 언어 지정
reader = easyocr.Reader(['en'])
# 캡쳐한 이미지에서 문자열 인식하기
result = reader.readtext(capchaPng.screenshot_as_png, detail=0)

# 이미지에 점과 직선이 포함되어있어서 문자 인식이 완벽하지 않아서 데이터를 수동으로 보정해주기로 했습니다.
capchaValue = result[0].replace(' ', '').replace('5', 'S').replace('0', 'O').replace('$', 'S').replace(',', '')\
    .replace(':', '').replace('.', '').replace('+', 'T').replace("'", '').replace('`', '')\
    .replace('1', 'L').replace('e', 'Q').replace('3', 'S').replace('€', 'C').replace('{', '').replace('-', '')

# 입력할 텍스트박스 클릭하기.
driver.find_element_by_class_name('validationTxt').click()
# 추출된 문자열 텍스트박스에 입력하기.
chapchaText = driver.find_element_by_id('txtCaptcha')
chapchaText.send_keys(capchaValue)

#chapchaText.send_keys(Keys.ENTER)