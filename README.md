# Whatsapp-blast-selenium

## requirement

1. Untuk requirement bisa dilihat pada [``requirement.txt``](requirements.txt)
install package yang dibutuhkan dengan cara

```
pip install -r requirements.txt
```
jika memiliki kendala pada instalan seperti
```
× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    
    If you wish to install a non-Debian packaged Python application,
    it may be easiest to use pipx install xyz, which will manage a
    virtual environment for you. Make sure you have pipx installed.
    
    See /usr/share/doc/python3.11/README.venv for more information.

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
```

maka bisa disarankan dengan cara:
- menghapus dari file ``usr/lib/python3.xxx/EXTERNALLY-MANAGED
- menggunakan tambahakn argument ``--break-system-packages`` pada akhir dari packages yang mau diinstall sebagai contoh
    ```
    pip install nama_package --break-system-packages
    ```
    ```
    pip install -r requirements.txt --break-system-packages
    ```
- tambahkan fungsi pada `~/.config/pip/pip.conf``
```
[global]
break-system-packages = true
```

kemudian jalankan program dengan perintah
```
python wa.py
```

