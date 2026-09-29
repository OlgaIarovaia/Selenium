### БИБЛИОТЕКИ
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
import time

### ИНИЦИАЛИЗАЦИЯ БРАУЗЕРА
service = Service(ChromeDriverManager().install()) 
driver = webdriver.Chrome(service=service) 


### ПОИСК ЭЛЕМЕНТОВ ПО АРТИБУТАМ
# Открытие страницы
driver.get('https://testautomationpractice.blogspot.com/')
# Поиск элементов
element_class_icon = driver.find_element(By.CLASS_NAME,'wikipedia-icon') #иконка Википедиа по имени класса
print('Иконка Википедиа',element_class_icon)
element_id_input = driver.find_element(By.ID,'Wikipedia1_wikipedia-search-input') #поле ввода по id
print('Поле ввода',element_id_input)



### КЛИК ПО ЭЛЕМЕНТАМ
# Получение элементов-дат для клика по списку
elements_list = driver.find_elements(By.XPATH, "//div[@class = 'form-check form-check-inline']//input[@type = 'checkbox']")
# Клик по элементам подряд
for index, element in enumerate(elements_list):
    print("Клик по элементу номер ", index+1, "; день недели ", element.get_attribute("id"))
    element.click()
    time.sleep(1)



### ВВОД ТЕКСТА
# Открытие страницы
driver.get('https://demoqa.com/text-box')
time.sleep(3)
# Получение элементов
full_name = driver.find_element(By.XPATH,'//input[@id = "userName"]')
email = driver.find_element(By.XPATH,'//input[@id = "userEmail"]')
current_adress = driver.find_element(By.XPATH,'//textarea[@id = "currentAddress"]')
permanent_adress = driver.find_element(By.XPATH,'//textarea[@id = "permanentAddress"]')
# Очистка и ввод данных
full_name.clear()
full_name.send_keys('Olga')
time.sleep(1) 
email.clear()
email.send_keys('olga@gmail.com') 
time.sleep(1)
current_adress.clear()
current_adress.send_keys('Moscow 1') 
time.sleep(1)
permanent_adress.clear()
permanent_adress.send_keys('Moscow 2') 
time.sleep(5)
# Проверка ввода
assert full_name.get_attribute("value") == "Olga", "Неверно указано имя"
assert email.get_attribute("value") == "olga@gmail.com", "Неверно указана почта"
assert current_adress.get_attribute("value") == "Moscow 1", "Неверно указан текущий адрес"
assert permanent_adress.get_attribute("value") == "Moscow 2", "Неверно указано постоянный адрес"
