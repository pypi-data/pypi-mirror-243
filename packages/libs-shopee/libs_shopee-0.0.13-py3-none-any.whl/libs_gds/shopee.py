from selenium import webdriver
import time
import requests
import json
import subprocess
import logging

## *********************************************************** SELENIUM
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
## *********************************************************** SELENIUM

logging.basicConfig(level=logging.INFO, format="%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

class LibGds:

    def __init__(self, user, type_akun, video, suara, ffmpeg, vPython):
        self.user=user
        self.type_akun=type_akun
        self.video=video
        self.suara=suara
        self.ffmpeg=ffmpeg
        self.vPython=vPython

        options = webdriver.ChromeOptions()
        options.add_argument("--verbose")
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
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
            print("ELM JUDUL ONOK")
        except:
            print("ELM JUDUL GAK ONOK")

        try:
            frame2 = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div[8]/div[1]/button"))
            )
            frame2.click()
            print("ELM TAMBAH PRODUCT ONOK")
        except:
            print("ELM TAMBAH PRODUCT GAK ONOK")

        # time.sleep(3)

        
        # ========================================================== SCROLLL
        scroll = 1
        str_scroll = 20
        while scroll < 5: # scroll 5 times
            try:
                str_scroll = str_scroll*scroll
                frame3 = WebDriverWait(self.driver, 4).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@id='product-select-scroll-container']/div/div[1]/div["+str(str_scroll)+"]"))
                )
                frame3.click()
            except:
                print("scroll entek")

            time.sleep(1)
            scroll += 1
        # ========================================================== SCROLLL

        try:
            check_box = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//span[text()='Pilih semua produk di halaman ini']"))
            )
            check_box.click()
            print("ELM CheckBox ONOK")
        except:
            print("ELM CheckBox GAK ONOK")

        time.sleep(3)

        try:
            btn_konfirm = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div/div[1]/div/article/div[3]/div[2]/button[2]"))
            )
            btn_konfirm.click()
            print("ELM BTN KONFIRMASI ONOK")
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
            print("KEY BTN LANJUT ONOK")
        except:
            print("ELM BTN LANJUT GAK ONOK")

        try:
            url_ = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/article/div/section[2]/div/div/article/section/div[2]/div"))
            )                                                                       
            print(url_.text)
            print("URL ONOK")
        except:
            print("URL GAK ONOK")

        try:
            key_ = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/article/div/section[2]/div/div/article/section/div[4]/div"))
            )
            print(key_.text)
            print("KEY ONOK")
        except:
            print("KEY GAK ONOK")

        try:
            btn_mulai_strim = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div/div[1]/div[3]/div/button[2]"))
            )
            btn_mulai_strim.click()
            print("BTN KONFIRM ONOK")
        except:
            print("BTN KONFIRM GAK ONOK")
                
        URL = url_.text
        KEY = key_.text
        VIDEO_SOURCE = self.video
        AUDIO_SOURCE = self.suara

        subprocess.Popen([f"{self.vPython}", f"{self.ffmpeg}", URL, KEY, VIDEO_SOURCE, AUDIO_SOURCE])

        try:
            btn_mulai_strim = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/header/div/div[2]/div[3]/button"))
            )
            print(btn_mulai_strim.text)
            btn_mulai_strim.click()
        except:
            print("TEXT STRIMING")

        url_strim = self.driver.current_url
        while True:
            if url_strim == self.driver.current_url:
                print("Strimming MLAKU")
                time.sleep(120)
            else:
                print("Strimming Mandek")
                break

        time.sleep(999999999)
