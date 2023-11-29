from selenium import webdriver
import time
import requests
import json
import os

## *********************************************************** SELENIUM
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
## *********************************************************** SELENIUM


class LibGds:

    def __init__(self, user, type_akun, dirImg):
        self.user=user
        self.type_akun=type_akun
        self.dirImg=dirImg

        options = webdriver.ChromeOptions()
        options.add_argument("--verbose")
        options.add_argument('--no-sandbox')
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("--window-size=1920, 1200")
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options)


    def set_cookies(self):
        self.driver.get("https://shopee.co.id/")
        time.sleep(2)

        response_akun = requests.get("https://sistem.bebitesgroup.com/PROJECT/CPA/api_blast/?action=get_cookies_tiktok_update&user="+self.user+"&type_akun="+self.type_akun)
        json_akun   = response_akun.json()
        id_akun     = json_akun[0]["id_akun"]
        cookies     = json_akun[0]["cookies"]

        try:
            json_object = json.loads(cookies)
            for i in json_object:
                cookie_with_name_and_value = {
                    "name" : i["name"],
                    "value" : i["value"]
                }
                self.driver.add_cookie(cookie_with_name_and_value)
        except:
            print("JSON BUSUK")

        self.driver.get("https://shopee.co.id/")
        time.sleep(3)

        self.driver.get("https://live.shopee.co.id/pc/setup")
        time.sleep(3)

        try:
            frame = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div[4]/div/div/div[1]/input"))
            )
            frame.click()
            judul_live = "Diskon 50%"
            frame.send_keys(Keys.CONTROL + 'a' + Keys.NULL, judul_live)
        except:
            print("ELM JUDUL GAK ONOK")

        try:
            frame2 = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div[8]/div[1]/button"))
            )
            frame2.click()
        except:
            print("ELM TAMBAH PRODUCT GAK ONOK")

        time.sleep(3)

        
        # ========================================================== SCROLLL
        # frame3 = WebDriverWait(self.driver, 2).until(
        #     EC.visibility_of_element_located((By.XPATH, "//*[@id='product-select-scroll-container']/div"))
        # )
        # actions = ActionChains(self.driver)
        # actions.move_to_element(frame3).perform()
        # self.driver.execute_script("arguments[0].scrollIntoView();", frame3)
        # ========================================================== SCROLLL

        try:
            check_box = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//span[text()='Pilih semua produk di halaman ini']"))
            )
            check_box.click()
        except:
            print("ELM CheckBox GAK ONOK")

        time.sleep(3)

        try:
            btn_konfirm = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div/div[1]/div/article/div[3]/div[2]/button[2]"))
            )
            btn_konfirm.click()
        except:
            print("ELM BTN KONFIRMASI GAK ONOK")

        time.sleep(3)

        try:
            btn_x_product = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div/div[2]/i"))
            )
            btn_x_product.click()
            print("ELM X PRODUCT ONOK")
        except:
            print("ELM X PRODUCT GAK ONOK")

        try:
            btn_konfirm = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div[11]/div/button"))
            )
            btn_konfirm.click()
        except:
            print("ELM BTN LANJUT GAK ONOK")

        try:
            url_ = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/article/div/section[2]/div/div/article/section/div[2]/div"))
            )                                                                       
            print(url_.text)
        except:
            print("URL GAK ONOK")

        try:
            key_ = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/article/div/section[2]/div/div/article/section/div[4]/div"))
            )
            print(key_.text)
        except:
            print("KEY GAK ONOK")

        VBR="2500k"
        FPS="30"
        QUAL="medium"
        AUDIO_ENCODER="aac" 
        
        URL = url_.text
        KEY = key_.text
        VIDEO_SOURCE = input("Lebokno path vidione (.mp4) ??:")
        AUDIO_SOURCE = input("lebokno path suarane (.mp3):")
        note = input("Ojok Kesuwen Ndang Enteren Cooookkk kwkwkkw")

        os.system(f'ffmpeg -stream_loop -1 -i "{VIDEO_SOURCE}" -deinterlace -stream_loop -1 -i "{AUDIO_SOURCE}" -deinterlace -vcodec libx264 -pix_fmt yuv420p -preset {QUAL} -r {FPS} -g $(({FPS} * 2)) -b:v {VBR}  -acodec {AUDIO_ENCODER} -ar 44100 -threads 6 -qscale 3 -b:a 712000 -bufsize 512k -f flv "{URL}/{KEY}"')

        time.sleep(5)

        try:
            btn_mulai_strim = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/header/div/div[2]/div[3]/button"))
            )
            print(btn_mulai_strim.text)
            btn_mulai_strim.click()
        except:
            print("KEY GAK ONOK")
        
        time.sleep(999999999)
