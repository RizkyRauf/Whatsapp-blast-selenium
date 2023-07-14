# Whatsapp-blast-selenium

**Whatsapp-blast-selenium** adalah metode penggunaan Selenium untuk mengirim pesan massal di WhatsApp. Dengan menggunakan otomatisasi Selenium, pengguna dapat mengirim pesan kepada banyak kontak atau grup secara efisien dan otomatis.

## Requirement

- **install package** yang dibutuhkan dengan cara:

    ```
    pip install -r requirements.txt
    ```

    > Untuk requirement program ini bisa dilihat pada [``requirement.txt``](requirements.txt)

- **prepare data** yang dibutuhkan, yaitu:
    - phone.xlsx
    - pesan.txt 

## Running Programs

Pastikan `path user` dan `chrome driver` sudah di set
- `options.add_argument("user-data-dir=[path user]")`
- `chrome_driver_path = "[path driver chrome ]"`

dan jalankan programnya
```py
# mengirim pesan teks
python wa.py
# mengirim pesan teks dan gambar
python wa_images.py 
```

