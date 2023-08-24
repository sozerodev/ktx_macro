"""_summary_
    ktx 예매 매크로.
    절대... 절대 악용하지 마세요. 무조건 피치못할 개인의 사정을 위해서만 사용할 것. 
"""
from selenium import webdriver
import time
import sys
import pygame
import datetime

def alert_get_ticket():
    # Initialize Pygame mixer
    pygame.mixer.init()
    
    # Load the sound file
    sound = pygame.mixer.Sound("./resource/school_bell.mp3")
    
    # Play the sound
    sound.play()
    
    # Wait until sound has finished playing
    while pygame.mixer.get_busy():
      pygame.time.Clock().tick(10)

    # Cleanup
    pygame.mixer.quit()



if __name__ == '__main__':
    import time
    

    # *여기를 입력해주세요!*
    # ========================================================================================================
    ko_id = "ID" # 코레일계정 회원번호
    ko_pw = "PW" # 코레일 계정 비번
    
    go_start, go_end = "광명", "서울" # 출발지, 도착지
    go_start_time = "01" # 몇시부터 예약할건지 (00, 01, 02, 03, 04, 05, 06, ... 12, 13, 14, ... 22, 23, 24)
    
    go_year, go_month, go_day = "2023", "05", "13" # 연도, 월, 일
    
    # 몇번째 행에 있는 티켓을 예매할건지
    reserve_time_list = [1, 2, 3] # 1행, 2행, 3행에 있는 것을 예매하겠다는 뜻 (시간대)
                                  # 예를 들어 01시부터 예약하면 01시 10분, 01시 20분, 01시 30분 3가지 모두 예약하려면 [1, 2, 3]이고)
                                  # 두번째인 01시 20분에 해당하는 1가지만 예약하려면 [2]이고)
    # ========================================================================================================
    
    
    
    
    login_url = "https://www.letskorail.com/korail/com/login.do"
    
    
    for idx, set_time in enumerate(reserve_time_list):
        reserve_time_list[idx] = 2*set_time -1
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    # chromedriver.exe가 위치한 절대 경로 설정
    driver = webdriver.Chrome(options=options, executable_path="./resource/chromedriver.exe") 

    driver.implicitly_wait(3)

    driver.get(login_url)
    time.sleep(float(1))

    # 현재 창의 핸들러 저장
    main_window_handle = driver.current_window_handle
    
    driver.execute_script(f"document.getElementById('txtMember').value = '{ko_id}'")
    driver.execute_script(f"document.getElementById('txtPwd').value = '{ko_pw}'")
    driver.execute_script("document.querySelector('.btn_login a').click()")


    # 팝업창 클릭 또는 팝업창이 자동으로 열리는 경우, 다른 핸들러가 추가됨

    time.sleep(1)
    
    # 출발지/도착지 설정
    driver.execute_script(f"document.getElementById('txtGoStart').value = '{go_start}'")
    driver.execute_script(f"document.getElementById('txtGoEnd').value = '{go_end}'")
    
    
    driver.execute_script("document.querySelector('option[value=\"21\"]').removeAttribute('selected')")
    
    # 예매 시간 설정
    driver.execute_script(f"document.querySelector('option[value=\"{go_start_time}\"]').setAttribute('selected', 'selected')")
    
    # 예매 날짜
    driver.execute_script(f"document.form1.selGoYear.value='{go_year}'")
    driver.execute_script(f"document.form1.selGoMonth.value='{go_month}'")
    driver.execute_script(f"document.form1.selGoDay.value='{go_day}'")

    
    driver.execute_script("document.querySelector('#res_cont_tab01 > form > div > fieldset > p > a').click()")

    time.sleep(5)
    
    is_finished = False
    
    while True:
        time.sleep(float(0.5))

        for set_time in reserve_time_list:
            try:
                driver.execute_script(f'document.querySelector("#tableResult > tbody > tr:nth-child({set_time}) > td:nth-child(6) > a:nth-child(1)").click()')

                driver.switch_to.alert.accept()
                driver.switch_to.alert.accept()
                
                print("\n\n\n\n\n")
                print("******************예약 완료***********************")
                now = datetime.datetime.now()
                formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
                print(f"예약 완료 시각은", formatted_date)
                after_20_minutes = now + datetime.timedelta(minutes=20)

                formatted_date = after_20_minutes.strftime("%Y-%m-%d %H:%M:%S")
                print("\n\n\n")
                print(f"*************{formatted_date} 까지 예약해야 합니다! *******************")
                
                # 완료 알람 울리기
                alert_get_ticket()    
                is_finished = True
                break
                
            except:
                print("",end="")

        
        if is_finished: sys.exit(0)
        
        driver.refresh()
        print("새로고침 중..")
    