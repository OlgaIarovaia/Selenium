### БИБЛИОТЕКИ
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, date, timedelta
import pandas as pd
import calendar 
import pickle 
import os 
import json 
import time
import requests
import urllib.parse



### ИНИЦИАЛИЗАЦИЯ БРАУЗЕРА 
# Задача опций браузера 
options = webdriver.ChromeOptions() #опции браузера
options.add_argument("--headless") #"безголовый режим" - запуск браузера в фоне, без открытия
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service,options=options)
wait = WebDriverWait(driver, 10, poll_frequency=1)  #явное ожидаение прогрузки


 
### КУКИ ДЛЯ АУТЕНТИФИКАЦИИ
### Важно - перед началом работ сохраняем куки в json-файл с помощью расширения Chrome Cookie-Editor
# Заходим на страницу аутентицикации
driver.get("https://passport.yandex.ru/auth/list?retpath=https%3A%2F%2Fid.yandex.ru%2F&noreturn=1") # заходим на сайт аутентификации яндекс аккаунта
wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete") #ждем полной загрузки страницы
print("Страница авторизации загружена")
driver.delete_all_cookies() # удаляем текущие куки - чтобы проставить заранее сохраненные (с пройденной аутентификацией)
# Подготавливаем сохраненные куки к загрузке
cookies_path = os.path.join(os.getcwd(), "cookies", "cookies_yandex.json") # открываем сохраненные куки
with open(cookies_path, "r", encoding="utf-8") as file:
    cookies = json.load(file)
for cookie in cookies: # удаляем из сохраненных кук поля, которые Selenium не принимает
    cookie.pop('sameSite', None)
    cookie.pop('expiry', None)
    cookie.pop('expirationDate', None)
    cookie.pop('httpOnly', None)
    cookie.pop('secure', None)
    cookie.pop('hostOnly', None)
    cookie.pop('session', None)
    if 'domain' in cookie and cookie['domain'].startswith('.'):
        cookie['domain'] = cookie['domain'][1:] # удаляем sameSite из набора кук - он не нужен и все ломает
for cookie in cookies: # добавляем по одной куке из оставлегося списка 
    driver.add_cookie(cookie) 
driver.refresh() #обязательно делаем рефреш страницы, чтобы новые куки применились
print('Пройдена аутентификация, проставлены актуальные cookie для работы')



### ВЫГРУЗКА ДАННЫХ ВОРДСТАТ
driver.get("https://wordstat.yandex.ru/") #переходим на страницу Вордстат
driver.refresh()
wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete") #ждем полной загрузки страницы
print("Страница Вордстат загружена")
time.sleep(5)

# Собираем куки в строку для запроса ниже
cookie_wordstat = driver.get_cookies()
cookie_wordstat = {cook['name']: cook['value'] for cook in cookie_wordstat}
cookie_wordstat_str = '; '.join([f"{name}={value}" for name, value in cookie_wordstat.items()])

# Выводим показатели для запроса
user_agent = driver.execute_script("return navigator.userAgent")
current_url = driver.current_url
accept_language = driver.execute_script("return navigator.language")
platform = driver.execute_script("return navigator.platform")

# Переменные для выгрузки 
url = 'https://wordstat.yandex.ru/wordstat/api/search'
search_word = 'Яндекс'
encoded_word = urllib.parse.quote(search_word)
group_period = "day"
devices = "desktop,phone,tablet"
regions = "all"
# Получаем границы прошлого месяца
today = date.today()  # например, 2026-09-29
# Первое число прошлого месяца
first_day_this_month = today.replace(day=1)
last_day_prev_month = first_day_this_month - timedelta(days=1)
first_day_prev_month = last_day_prev_month.replace(day=1)
# Последнее число прошлого месяца
last_day = calendar.monthrange(last_day_prev_month.year, last_day_prev_month.month)[1]
last_date_prev_month = last_day_prev_month.replace(day=last_day)
# Формат ДД.ММ.ГГГГ
first_date = first_day_prev_month.strftime('%d.%m.%Y')
last_date = last_date_prev_month.strftime('%d.%m.%Y')
print(f'Грузим даты {first_date} - {last_date}')

# Запрос данных - он появляется в network при поиске по фразе
payload = {
        "currentDevice": devices,
        "currentGraphType": group_period,
        "dbname": "rus", 
        "endDate": last_date,
        "filters": {
            "region": regions, 
            "tableType": "popular"
        },
        "searchValue": search_word,
        "startDate": first_date,
        "text": {
            "graph": {
                "title": f"История запросов «{search_word}»",
                "disclaimer": f"Для каждой даты с {first_date} по {last_date} мы посчитали отношение числа запросов «{search_word}» к среднему числу таких запросов за весь период.\\nГрафик показывает, как отличается дневное количество запросов от среднего значения."
            },
            "map": {
                "title": "",
                "disclaimer": ""
            },
            "table": {
                "title": "",
                "disclaimer": ""
            }
        }
    }

# Заголовки для отчета
headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": f"{accept_language},en-US;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": cookie_wordstat_str,
        "Origin": "https://wordstat.yandex.ru",
        "Referer": f"https://wordstat.yandex.ru/?region=all&view=graph&words={encoded_word}",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site", 
        "Host": "wordstat.yandex.ru",
        "User-Agent": user_agent,
        "sec-ch-ua": '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": f'"{platform}"',
        "priority": "u=1, i",
    }

# Запрос к Вордстат
response = requests.post(url=url, headers=headers, json=payload)
print(f'status code - {response.status_code}')

# Диагностика ошибки
if response.status_code != 200:
    print(f"❌ Ошибка запроса: {response.status_code}")
    print(f"📄 Заголовки ответа: {dict(response.headers)}")
    print(f"📄 Текст ответа (первые 500 символов):\n{response.text[:500]}")
    # Если вернулась HTML-страница с ошибкой
    if "html" in response.text.lower():
        print("\n⚠️ Сервер вернул HTML-страницу вместо JSON.")
        print("   Возможные причины:")
        print("   1. Истекли или невалидны куки")
        print("   2. Нет доступа к Wordstat")
        print("   3. Некорректные параметры запроса")
else:
    json_resp = response.json()['graph']['images']['timeSeries']['preparedValues']['absolute']
    print('Данные выгружены успешно!')

# Обработка данных 
df = pd.DataFrame(json_resp)
# Переименовываем 'y' в понятное имя и удаляем колонку month (при выгрузке по дням она None)
df = pd.DataFrame(json_resp).drop(columns=['month']).rename(columns={'y': 'requests'})
# Преобразуем 'day' в datetime
df['day'] = pd.to_datetime(df['day'])
# Добавляем новые колонки
df['search_word'] = search_word
df['month'] = datetime.strptime(first_date, '%d.%m.%Y').strftime('%Y-%m-%d')
print(df)
