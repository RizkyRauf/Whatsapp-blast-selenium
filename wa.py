import time
import mysql.connector
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#Bs
import pandas as pd

#regex
import re

#append
pesan = []
number_phone = []

#phone target yang akan dikirim
read_phone = pd.read_excel('test.xlsx')
for i in range(len(read_phone)):
    number = read_phone['phone'][i]  # number berisi lebih dari 1 value

    # pesan yang akan dikirim
    with open('pesan.txt', 'r', encoding="utf8") as file:
        pesan_tergabung = file.read()

    pesan = pesan_tergabung.split('\n')

    # Tentukan jalur ke ChromeDriver Anda
    chrome_driver_path = ''

    # Inisialisasi Service object
    service = Service(chrome_driver_path)

    # Inisialisasi Options object
    options = Options()
    options.add_argument("")  # Contoh penggunaan opsi lainnya

    # Inisialisasi WebDriver dengan menggunakan Service object dan Options object
    driver = webdriver.Chrome(service=service, options=options)

    url = 'https://api.whatsapp.com/send/?phone=62{}&text&type=phone_number&app_absent=0'.format(number)
    driver.get(url)

    # klik lanjut chat
    wait = WebDriverWait(driver, 100)
    lanjut_path = "//a[contains(@title,\"Bagikan di WhatsApp\")]"
    lanjut = wait.until(EC.presence_of_element_located((By.XPATH, lanjut_path)))
    lanjut.click()
    print("berhasil klik lanjut chat kepada {}".format(number))
    time.sleep(4)

    # gunakan Whatsapp Web
    gunakan_path = "//h4[@class='_9vd5'][2]/a[@class='_9vcv _9vcx']/span[@class='_advp _aeam']"
    gunakan = wait.until(EC.presence_of_element_located((By.XPATH, gunakan_path)))
    time.sleep(4)
    gunakan.click()
    print("berhasil gunakan whatsapp kepada {}".format(number))

    # Masukkan pesan per paragraf
    message_box_path = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
    message_box = wait.until(EC.presence_of_element_located((By.XPATH, message_box_path)))

    for message in pesan:
        message_box.send_keys(message)
        message_box.send_keys(Keys.SHIFT, '\n')
        message_box.send_keys(Keys.SHIFT, '\n')

    message_box.send_keys(Keys.ENTER)
    time.sleep(10)

    # Cek tanda centang ganda untuk memastikan pesan terkirim
    sent_tick_path = "//span[@data-testid='msg-dblcheck']"
    sent_tick = driver.find_elements(By.XPATH, sent_tick_path)
    if sent_tick:
        print("Pesan terkirim")
    else:
        print("Pesan tidak terkirim")

    driver.quit()
