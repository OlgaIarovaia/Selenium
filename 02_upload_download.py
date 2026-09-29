### БИБЛИОТЕКИ
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
import time
import os



### ИНИЦИАЛИЗАЦИЯ БРАУЗЕРА - ДЛЯ ЗАГРУЗКИ
# Задача опций  
options = webdriver.ChromeOptions() 
# Инициализация 
service = Service(ChromeDriverManager().install()) 
driver = webdriver.Chrome(service=service,options=options)

### ЗАГРУЗКА ФАЙЛА НА САЙТ
# Открытие страницы 
driver.get('https://demoqa.com/upload-download')
time.sleep(3)
# Поле ввода для загрузки файла 
upload_file_field = driver.find_element(By.XPATH, "//input[@type='file']")
# Загружаем картинку через поле ввода (=аналогично вводу текста)
upload_file_field.send_keys(f"{os.getcwd()}\\downloads\\test-upload.png") #этот код загружает файл test-upload.png из текущей рабочей директории
time.sleep(3)



### ИНИЦИАЛИЗАЦИЯ БРАУЗЕРА - ДЛЯ СКАЧИВАНИЯ
# Задача опций браузера 
options = webdriver.ChromeOptions() 
# Куда скачивать файлы
script_dir = os.path.dirname(os.path.abspath(__file__)) # директория файла скрипта
download_path = os.path.join(script_dir, "downloads") # папка downloads в директории хранения текущего скрипта
preferences = {"download.default_directory": download_path} # задаем путь для скачивания файла  - в директорию файла скрипта
options.add_experimental_option('prefs',preferences) # добавляем preferences в опции браузера
# Инициализация браузера с опциями
service = Service(ChromeDriverManager().install()) 
driver = webdriver.Chrome(service=service,options=options) 

### СКАЧИВАНИЕ ФАЙЛОВ С САЙТА
# Открытие страницы 
driver.get('https://the-internet.herokuapp.com/download')
time.sleep(5)
# Получаем список элементов-картинок
file_list = driver.find_elements(By.XPATH,"//div[@class='example']//a")
# Скачиваем файлы через цикл - только первые 3
for file in file_list[:3]:
    file.click()
time.sleep(5)
