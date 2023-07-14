import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os

# Fungsi untuk mengirim pesan dan menghitung jumlah pesan terkirim
def kirim_pesan(number, pesan):
    try:
        # Tentukan jalur ke ChromeDriver Anda
        chrome_driver_path = '[path driver]/chromedriver'

        # Inisialisasi Service object
        service = Service(chrome_driver_path)

        # Inisialisasi Options object
        options = Options()
        options.add_argument("user-data-dir=[path user data directory]")

        # Inisialisasi WebDriver dengan menggunakan Service object dan Options object
        driver = webdriver.Chrome(service=service, options=options)

        url = 'https://api.whatsapp.com/send/?phone=62{}&text&type=phone_number&app_absent=0'.format(number)
        driver.get(url)
        time.sleep(2)

        # Klik lanjut chat
        wait = WebDriverWait(driver, 50)
        lanjut_path = "//a[contains(@title,\"Bagikan di WhatsApp\")]"
        lanjut = wait.until(EC.presence_of_element_located((By.XPATH, lanjut_path)))
        lanjut.click()
        time.sleep(2)

        # Gunakan WhatsApp Web
        gunakan_path = "//h4[@class='_9vd5'][2]/a[@class='_9vcv _9vcx']/span[@class='_advp _aeam']"
        gunakan = wait.until(EC.presence_of_element_located((By.XPATH, gunakan_path)))
        time.sleep(2)
        gunakan.click()

        # Masukkan pesan per paragraf
        message_box_path = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
        message_box = wait.until(EC.presence_of_element_located((By.XPATH, message_box_path)))
        message_box.click()

        for message in pesan:
            message_box.send_keys(message)
            message_box.send_keys(Keys.SHIFT, '\n')
            message_box.send_keys(Keys.SHIFT, '\n')

        message_box.send_keys(Keys.ENTER)
        print ("=============================================")
        print("Berhasil mengirim pesan kepada = {}".format(number))
        print ("=============================================")

        time.sleep(5)
        
        # File yang akan dikirim, bisa 1 atau lebih
        image_paths = ["C:\\Users\\anand\\Downloads\\wa2.jpeg", "C:\\Users\\anand\\Downloads\\wa3.jpeg"] # contoh

        for x in range(len(image_paths)):

            # 1. klik tombol clip
            clip_path = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div'
            clip_button = wait.until(EC.presence_of_element_located((By.XPATH, clip_path)))
            clip_button.click()

            # 2. Klik untuk lampirkan
            lampirkan_path = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div'
            lampirkan_button = wait.until(EC.presence_of_element_located((By.XPATH, lampirkan_path)))
            lampirkan_button.click()

            # 3. Attach multiple images
            image_path = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input'
            image_button = wait.until(EC.presence_of_element_located((By.XPATH, image_path)))
            image_button.send_keys(image_paths[x])

            # 4. images send
            image_send_button_xpath = '//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div'
            image_send_button = wait.until(EC.presence_of_element_located((By.XPATH, image_send_button_xpath)))
            image_send_button.click()

            print ("=============================================")
            print("Berhasil mengirim foto kepada = {}".format(number))
            print ("=============================================")
            time.sleep(5)

        # Cek tanda centang ganda untuk memastikan pesan terkirim
        sent_tick_path = "//span[@data-testid='msg-dblcheck']"
        sent_tick = driver.find_elements(By.XPATH, sent_tick_path)
        pesan_terkirim = bool(sent_tick)

        driver.quit()

        return pesan_terkirim

    except TimeoutException as e:
        print (e)
        print ("=============================================")
        print("Terjadi kesalahan saat mengirim pesan kepada {}".format(number))
        print ("=============================================")
        return False


# Baca data phone.xlsx
read_phone = pd.read_excel('test.xlsx')

# Baca pesan dari file pesan.txt
with open('pesan.txt', 'r', encoding="utf8") as file:
    pesan_tergabung = file.read()

pesan = pesan_tergabung.split('\n')

# Inisialisasi variabel jumlah pesan terkirim dan jumlah tidak memiliki WhatsApp Web
pesan_terkirim = 0
tidak_punya_whatsapp_web = 0

# Kirim pesan untuk setiap nomor telepon
for i in range(len(read_phone)):
    number = str(read_phone['phone'][i])  # number berisi lebih dari 1 value

    # Kirim pesan dan periksa apakah terkirim
    terkirim = kirim_pesan(number, pesan)

    if terkirim:
        pesan_terkirim += 1
    else:
        tidak_punya_whatsapp_web += 1

print("Jumlah pesan terkirim: {}".format(pesan_terkirim))
print("Jumlah tidak memiliki WhatsApp Web: {}".format(tidak_punya_whatsapp_web))
