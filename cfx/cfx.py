from selenium import webdriver
from datetime import datetime, timedelta
import os
import time
import datetime
import random

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(15)

def check_exists_elem(css_selector):
    try:
        driver.find_element_by_css_selector(css_selector)
    except:
        return False
    return True

def loading():
	str_star = '☆☆☆☆☆'
	twinkle = ''

	for i in range(5):
		os.system('cls')
		twinkle += '★'
		str_star = twinkle + str_star[i+1:]

		print('로딩중 {}'.format(str_star))
		time.sleep(0.5)

	os.system('cls')

main_url = "https://www.chainflix.net"

print('체인플릭스 아이디를 입력하세요.')
cfx_id = input()
print('체인플릭스 비밀번호를 입력하세요.')
cfx_pw = input()

print('체인플릭스 사이트로 이동합니다. 잠시만 기다려주세요!')

# 페이지로 이동
driver.get(main_url)

# 로그인 페이지로 이동
driver.find_element_by_class_name('text-linker.pa-0.font-weight-regular.tp-7.overflow-hidden.has-max-line').click()

# 이메일로 로그인 버튼 클릭
driver.find_element_by_css_selector('#app > div > main > div > div > div.row.fill-height.no-gutters.overflow-x-hidden > div > div > div > div:nth-child(1) > div > div.col.col-10.align-self-center > div > div.container.pa-8.container-area > div > div.row.pb-5.mt-3.no-gutters.align-center.justify-space-around > div:nth-child(4)').click()

time.sleep(2)

# 아이디 입력
id_box = driver.find_element_by_css_selector('#app > div > main > div > div > div.row.fill-height.no-gutters.overflow-x-hidden > div > div > div > div:nth-child(1) > div > div.col.col-10.align-self-center > div > div.container.pa-8.container-area > div > div:nth-child(4) > form > div.v-input.mb-4.v-input--hide-details.v-input--dense.theme--light.v-text-field.v-text-field--is-booted.v-text-field--enclosed.v-text-field--outlined.v-text-field--placeholder > div > div > div.v-text-field__slot > input[type=text]')
id_box.send_keys(cfx_id)

# 비밀번호 입력
pw_box = driver.find_element_by_css_selector('#app > div > main > div > div > div.row.fill-height.no-gutters.overflow-x-hidden > div > div > div > div:nth-child(1) > div > div.col.col-10.align-self-center > div > div.container.pa-8.container-area > div > div:nth-child(4) > form > div.v-input.mb-6.v-input--hide-details.v-input--dense.theme--light.v-text-field.v-text-field--is-booted.v-text-field--enclosed.v-text-field--outlined.v-text-field--placeholder > div > div > div.v-text-field__slot > input[type=password]')
pw_box.send_keys(cfx_pw)

# 로그인 시도
pw_box.submit()

# 로딩
loading()

print('========== 자동 재생 시작 ==========')

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

	# 재생버튼 누르기
	play_btn = driver.find_element_by_css_selector("#contentPlayer > div.row.no-gutters.control-bar.flex-nowrap.flex-column > div.col.py-2.px-4 > div > div:nth-child(1) > button").click()

	# 해당 영상 시간 가져오기
	video_time = driver.find_element_by_css_selector("#contentPlayer > div.row.no-gutters.control-bar.flex-nowrap.flex-column > div.col.py-2.px-4 > div > div:nth-child(4) > p:nth-child(2) > span").text
	# print("video_time - " + video_time)
	
	video_min = video_time.split(":")[0] # 영상 재생 시간(분) 가져오기	
	# print("video_min - " + video_min)

	# 영상 재생 후 대기시간 설정
	if video_min == "":
		print("영상시간 불러오기 실패")
		continue # 영상시간 못가져오는 경우 다음 영상으로 이동
		# rest_min = 1 # 기본 1분으로 설정
	else:
		# print("영상시간 타입변환 전 - {}".format(video_min))

		# 타입 변환 string -> int
		video_min = int(video_min)
		# print("영상시간 타입변환 후 - {}".format(video_min))

		if video_min > 17:
			rest_min = 17 # 영상이 17분 넘어가는 경우 최대 15분으로 설정
			print("영상시간 17분 초과 - {}".format(rest_min))
		elif video_min == 0:
			# rest_min = 1
			# 1분 미만 or 영상시간 못가져오는 경우 건너뛰기
			print("영상 건너뛰기")
			continue			
		else :
			rest_min = video_min
			print("영상시간 17분 이내 - {}".format(rest_min))

	# 대기 시간(초)
	rest_sec = rest_min * 60

	# 현재 잔액
	check_cur_balance = check_exists_elem("#app > div > main > div > div > div.row.fill-height.no-gutters.overflow-x-hidden > div > div > div.content-info-area_3BJ59 > div.row.no-gutters.mt-6.flex-nowrap.overflow-hidden.flex-column.flex-lg-row > div.col.col-auto.pb-8 > div > div:nth-child(2) > div > div:nth-child(1) > p > span.tp-9")

	if check_cur_balance == True:
		nowDatetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		cur_balance = driver.find_element_by_css_selector("#app > div > main > div > div > div.row.fill-height.no-gutters.overflow-x-hidden > div > div > div.content-info-area_3BJ59 > div.row.no-gutters.mt-6.flex-nowrap.overflow-hidden.flex-column.flex-lg-row > div.col.col-auto.pb-8 > div > div:nth-child(2) > div > div:nth-child(1) > p > span.tp-9").text
		print("{} => 현재 보상 : {} CFX".format(nowDatetime, cur_balance))

	# 영상 재생되는 동안 기다림	
	print("{} 초 후 다음영상 재생".format(rest_sec))	
	time.sleep(rest_sec)