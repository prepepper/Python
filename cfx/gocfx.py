from selenium import webdriver
from datetime import datetime, timedelta
from selenium.common.exceptions import NoSuchElementException
import time
import datetime
import random

driver = webdriver.Chrome()
driver.implicitly_wait(15)

def check_exists_elem(css_selector):
    try:
        driver.find_element_by_css_selector(css_selector)
    except NoSuchElementException:
        return False
    return True

main_url = "https://www.chainflix.net"

# 페이지로 이동
driver.get(main_url)

# 로그인 페이지로 이동
driver.find_element_by_class_name('text-linker.pa-0.font-weight-regular.tp-7.overflow-hidden.has-max-line').click()
time.sleep(7)

# 이메일로 로그인 버튼 클릭
driver.find_element_by_css_selector('#app > div > main > div > div > div.row.fill-height.no-gutters.overflow-x-hidden > div > div > div > div:nth-child(1) > div > div.col.col-10.align-self-center > div > div.container.pa-8.container-area > div > div.row.pb-5.mt-3.no-gutters.align-center.justify-space-around > div:nth-child(4) > a > span').click()

# 아이디 입력
id_box = driver.find_element_by_css_selector('#app > div > main > div > div > div.row.fill-height.no-gutters.overflow-x-hidden > div > div > div > div:nth-child(1) > div > div.col.col-10.align-self-center > div > div.container.pa-8.container-area > div > div:nth-child(4) > form > div.v-input.mb-4.v-input--hide-details.v-input--dense.theme--light.v-text-field.v-text-field--is-booted.v-text-field--enclosed.v-text-field--outlined.v-text-field--placeholder > div > div > div.v-text-field__slot > input[type=text]')
id_box.send_keys("swhoo2002@hanmail.net")

# 비밀번호 입력
pw_box = driver.find_element_by_css_selector('#app > div > main > div > div > div.row.fill-height.no-gutters.overflow-x-hidden > div > div > div > div:nth-child(1) > div > div.col.col-10.align-self-center > div > div.container.pa-8.container-area > div > div:nth-child(4) > form > div.v-input.mb-6.v-input--hide-details.v-input--dense.theme--light.v-text-field.v-text-field--is-booted.v-text-field--enclosed.v-text-field--outlined.v-text-field--placeholder > div > div > div.v-text-field__slot > input[type=password]')
pw_box.send_keys("!a123123")

# 로그인 시도
pw_box.submit()
time.sleep(4)

# 무한 재생
while 1 == 1:
	# 랜덤으로 영상 컨텐츠 번호 가져오기
	num = random.randrange(17500,90000)

	# 페이지로 이동
	target_url = main_url + "/video?contentId={}".format(num)
	print("페이지 이동 url : " + target_url)
	driver.get(target_url)	

	# 영상이 등록되어있는지 체크
	go_back_btn = check_exists_elem("#app > div > main > div > div > div.row.fill-height.no-gutters.overflow-x-hidden > div > div > div.v-responsive.pa-0 > div.v-responsive__content > div > div > div.col.col-auto.align-self-center.mb-6 > div > button > span > p > span")
	# print("go_back_btn : {}".format(go_back_btn))

	# 등록된 영상이 없는 경우 처리
	if go_back_btn == True:		
		continue

	# time.sleep(2)

	# 재생버튼 누르기
	play_btn = driver.find_element_by_css_selector("#contentPlayer > div.row.no-gutters.control-bar.flex-nowrap.flex-column > div.col.py-2.px-4 > div > div:nth-child(1) > button").click()

	# 해당 영상 시간 가져오기
	video_time = driver.find_element_by_css_selector("#contentPlayer > div.row.no-gutters.control-bar.flex-nowrap.flex-column > div.col.py-2.px-4 > div > div:nth-child(4) > p:nth-child(2) > span").text
	print("video_time - " + video_time)	
	video_min = video_time[:2] # 영상 재생 시간(분) 가져오기
	print("video_min - " + video_min)

	# 영상 재생 후 대기시간 설정
	if video_min == "":
		rest_min = 3 # 기본 3분으로 설정
	else:
		# print("영상시간 타입변환 전 - {}".format(video_min))

		# 타입 변환 string -> int
		video_min = int(video_min)
		# print("영상시간 타입변환 후 - {}".format(video_min))

		if video_min > 10:
			rest_min = 10 # 영상이 10분 넘어가는 경우 최대 10분으로 설정
			print("영상시간 10분 초과 - {}".format(rest_min))
		elif video_min == 0:
			rest_min = 3
			print("영상시간 기본시간으로 설정")
		else :
			rest_min = video_min
			print("영상시간 10분 이내 - {}".format(rest_min))

	# 대기 시간(초)
	rest_sec = rest_min * 60

	# 현재 잔액
	check_cur_balance = check_exists_elem("#app > div > main > div > div > div.row.fill-height.no-gutters.overflow-x-hidden > div > div > div.content-info-area_3BJ59 > div.row.no-gutters.mt-6.flex-nowrap.overflow-hidden.flex-column.flex-lg-row > div.col.col-auto.pb-8 > div > div:nth-child(2) > div > div:nth-child(1) > p > span.tp-9")

	if check_cur_balance == True:
		nowDatetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		cur_balance = driver.find_element_by_css_selector("#app > div > main > div > div > div.row.fill-height.no-gutters.overflow-x-hidden > div > div > div.content-info-area_3BJ59 > div.row.no-gutters.mt-6.flex-nowrap.overflow-hidden.flex-column.flex-lg-row > div.col.col-auto.pb-8 > div > div:nth-child(2) > div > div:nth-child(1) > p > span.tp-9").text
		print("{} => cur_balance : {}".format(nowDatetime, cur_balance))

	# 영상 재생되는 동안 기다림	
	print("영상 재생되는 동안 기다림 - {} 초".format(rest_sec))	
	time.sleep(rest_sec)