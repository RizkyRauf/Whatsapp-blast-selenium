from __future__ import annotations

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd


# Fungsi untuk mengirim pesan dan menghitung jumlah pesan terkirim
def kirim_pesan(number: str, pesan: list[str]) -> bool:
    """
     mengirim pesan ke kontak whatsapp dengan automasi WebDriver

     args:
         number (str) : nomor kontak yang ingin dituju
         pesan (list[str]): list dari pesan kata
     return:
         bool: True jika pesan dikirim berhasil, False kemungkinan lain

     raises:
        Exception: jika proses number tidak ditemukan
    contoh:
     number = "09xxxxxxx"
     pesan = ["saya", "ganteng"]

     sukses = kirim_pesan(number, pesan)
     if sukses:
         print("sukses")
     else:
         print(failed)
    """
    try:
        # Tentukan jalur ke ChromeDriver Anda
        chrome_driver_path = "[path driver chrome ]"

        # Inisialisasi Service object
        service = Service(chrome_driver_path)

        # Inisialisasi Options object
        options = Options()
        options.add_argument("user-data-dir=[path user]")

        # Inisialisasi WebDriver dengan menggunakan Service object dan Options object
        with webdriver.Chrome(service=service, options=options) as driver:
            url = f"https://api.whatsapp.com/send/?phone=62{number}&text&type=phone_number&app_absent=0"
            driver.get(url)
            time.sleep(2)

            # Klik lanjut chat
            wait = WebDriverWait(driver, 100)
            lanjut_path = '//a[contains(@title,"Bagikan di WhatsApp")]'
            lanjut = wait.until(EC.presence_of_element_located((By.XPATH, lanjut_path)))
            lanjut.click()
            time.sleep(2)

            # Gunakan WhatsApp Web
            gunakan_path = "//h4[@class='_9vd5'][2]/a[@class='_9vcv _9vcx']/span[@class='_advp _aeam']"
            gunakan = wait.until(
                EC.presence_of_element_located((By.XPATH, gunakan_path))
            )
            time.sleep(2)
            gunakan.click()

            # Masukkan pesan per paragraf
            message_box_path = (
                '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
            )
            message_box = wait.until(
                EC.presence_of_element_located((By.XPATH, message_box_path))
            )

            for message in pesan:
                message_box.send_keys(message)
                message_box.send_keys(Keys.SHIFT, "\n")
                message_box.send_keys(Keys.SHIFT, "\n")

            message_box.send_keys(Keys.ENTER)
            print("=" * 45)
            print(f"Berhasil mengirim pesan kepada {str(number)}")
            print("=" * 45)
            time.sleep(5)

            # Cek tanda centang ganda untuk memastikan pesan terkirim
            sent_tick_path = "//span[@data-testid='msg-dblcheck']"
            sent_tick = driver.find_elements(By.XPATH, sent_tick_path)
            pesan_terkirim = bool(sent_tick)

        return pesan_terkirim

    except Exception:
        print("=" * 45)
        print(f"Terjadi kesalahan saat mengirim pesan kepada {number}")
        # print(f"info error {error_try}")
        print("=" * 45)
        return False


def main() -> None:
    try:
        baca_nomor = pd.read_excel("phone.xlsx")
        with open("pesan.txt", "r", encoding="utf8") as file:
            pesan_tergabung = file.read()
        pesan = pesan_tergabung.split("\n")

        pesan_terkirim = 0
        tidak_punya_whatsapp_web = 0

        for number in baca_nomor["phone"].astype(str):
            terkirim = kirim_pesan(number, pesan)

            if terkirim:
                pesan_terkirim += 1
            else:
                tidak_punya_whatsapp_web += 1

        print(f"jumlah pesan terkirim: {pesan_terkirim}")
        print(f"jumlah tidak memiliki whatsapp web: {tidak_punya_whatsapp_web}")

    except Exception as filenotfound:
        print(filenotfound)
    except Exception as e:
        print(f"error : {e}")


if __name__ == "__main__":
    main()
