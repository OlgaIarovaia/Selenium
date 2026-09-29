# Курс на YouTube

## Сайты для тестирования

- https://testautomationpractice.blogspot.com/
- https://aqa-proka4.org/sandbox/web

---

## SELENIUM

**Web Driver** — API для управления браузером, независимый от языка.

**Driver** — сущность, которая отвечает за делегирование полномочий браузеру. Обеспечивает обмен данными между Selenium и браузером.

**Selenium** — фреймворк, связывающий все части с помощью, например, Python. Позволяет использовать все части браузера.

> Selenium — это не инструмент автоматизации, это инструмент для взаимодействия с браузером.

### Установка Selenium

В пустом проекте создаём виртуальное окружение:

```bash
pip install uv
uv venv venv
```

Далее устанавливаем selenium и webdriver (второй поддерживает самые актуальные штуки для взаимодействия с браузером):

```bash
uv pip install selenium
uv pip install webdriver-manager
```

Создаём папку для работы:

```bash
mkdir lesson_2
```

---

## НАЧАЛО РАБОТЫ В CHROME

### Инициализация драйвера

```python
# БИБЛИОТЕКИ
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# При запуске кода ниже откроется-закроется браузер
service = Service(ChromeDriverManager().install())  # тут лежит установленный хромдрайвер
driver = webdriver.Chrome(service=service)          # драйвер хрома
```

### Опции браузера

**Опции браузера** — это его настройки перед запуском (возможности браузера). Задаются **ДО** инициализации браузера, а `options` передаётся в него как параметр.

```python
# Инициализировать опции браузера
options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)  # в драйвер добавляем опции
```

#### Режим открытия страницы

| Опция | Что делает |
|---|---|
| `options.add_argument("--headless")` | Безголовый режим, запуск в фоновом режиме. Браузер без интерфейса, в фоне, без открытия окна; для автоматизаций |
| `options.add_argument("---incognito")` | Инкогнито режим. Без кэша и сохранения данных; для тестов |
| `options.add_argument("----disable-cache")` | Режим без кэша. Все ресурсы загружаются каждый раз заново |
| `options.add_argument("----ignore-certificate-errors")` | Игнор SSL-сертификата для https, если он закончился или отсутствует (ошибка «your connection is not private») |
| `options.add_argument("--window-size=700,700")` | Задать размер окна браузера. Аналог: `driver.set_window_size(700,700)` |

#### Стратегия загрузки страницы

- **normal** — используется по дефолту, ожидает загрузки всех ресурсов (картинки, js-код, шрифты и т.д.) на странице.
- **eager** — ожидает только готовности загрузки DOM (html-структуры), при этом картинки и прочее могут до сих пор грузиться.

```python
options.page_load_strategy = "normal"
options.page_load_strategy = "eager"
```

### Навигация браузера

После инициализации браузера:

```python
driver.get("https://example.ru")   # открытие страницы
driver.back()                       # переход назад
driver.forward()                    # переход вперёд
driver.refresh()                    # перезагрузка страницы
```

### Атрибуты и валидация

После инициализации браузера и открытия страницы:

```python
driver.current_url    # URL текущей страницы
driver.title          # заголовок текущей страницы (из кода сайта)
driver.page_source    # исходный код текущей страницы
```

Валидация:

```python
assert a == b, "A не равно Б"

# Пример
assert driver.current_url == "https://ru.wikipedia.org/wiki/Selenium", "Неверная ссылка!!!"
```

### Режим Web Driver

**Зачем:** часть сайтов может вызывать проблемы, если понимает, что с ней работает авто-ПО (включать капчи, блокировать).

Притвориться человеком:

```python
options.add_argument("--disable-blink-features=AutomationControlled")
```

Полный код:

```python
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
```

### Режим User Agent

Варианта выше для того, чтобы работа Selenium воспринималась как человек, часто недостаточно. Тогда добавляем к `--disable-blink-features=AutomationControlled` ещё опцию `user-agent`.

**User agent** — это программный элемент браузера (строка), обозначающий юзера, по сути некий идентификатор, который позволяет браузеру идентифицировать нас как пользователя.

В User-agent передаются следующие данные:

- Название и версия браузера.
- Язык.
- Версия операционной системы.
- Программное обеспечение, установленное на используемом устройстве.
- Тип устройства, с которого пользователь зашёл на сайт.

**Для чего он нужен:**

- Для обхода капчи и базовой аутентификации. Можно попросить разработчиков убирать капчу или базовую аутентификацию для пользователей с определённым юзер-агентом.
- Для того, чтобы сайты воспринимали исполнение кода веб-драйвером в качестве реального пользователя (да, отключение WebDriver-мода помогает, но по user-agent всё ещё можно определить, что вы работаете с помощью скрипта).
- Для тестирования поведения веб-приложения при разных параметрах, например поведение при разных языках.

```python
options.add_argument("--user-agent=Ваш кастомный или заранее выбранный юзер-агент")
```

Полный код:

```python
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--user-agent=Ваш кастомный или заранее выбранный юзер-агент")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
```

---

## ОЖИДАНИЯ

### Неявные ожидания

**Неявное ожидание** — это количество времени (которое указывается нами), в течение которого WebDriver будет опрашивать DOM. Неявным оно называется, так как мы не указываем, чего ждать: изменения текста, размера и т.д.

- Указывается 1 раз в коде и работает для всей сессии.
- В основном применяется для `find_element()` и `find_elements()`, потому что как раз эти методы запрашивают обновления элемента на странице.
- При проверке на исчезновение элемента будет задерживать наши тесты.

> Предпочтительно использовать явные ожидания.

```python
driver.implicitly_wait(10)  # неявное ожидание в 10 сек
# ставим перед нужными действиями (например, перед поиском кнопки — ждём 10 сек и ищем кнопку)
```

### Явные ожидания

**Явное ожидание** — ожидание конкретного условия: появления элемента, исчезновения элемента, изменения текста и т.д. С этим работается в разы комфортнее.

**Особенности:**

- Объявляется только там, где нужно.
- Ожидает выполнения нужного условия.

**Кейсы, зачем:**

- быть уверенным, что элемент на странице уже прогружен;
- проверка, что элемент пропал.

Многие виды ожиданий требуют в себя кортеж. Важное отличие — они сами распаковывают, так что `*` не нужен.

**Частые условия явного ожидания:**

| Условие | Что делает |
|---|---|
| `element_to_be_clickable(locator)` | Ожидает видимости элемента и его кликабельности |
| `visibility_of_element_located(locator)` | Ожидание того, что элемент присутствует в DOM и виден визуально (высота и ширина > 0) |
| `invisibility_of_element_located(locator)` | Ожидание того, что элемент невидим или исчез из DOM |
| `text_to_be_present_in_element_value(locator, text)` | Ожидание наличия нужного текста в элементе |

**Доп. библиотеки для явного ожидания:**

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
```

**Базовая инициализация:**

```python
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
```

**Общие настройки ожидания:**

```python
wait = WebDriverWait(driver, 30, poll_frequency=1)
# аргументы: драйвер, время ожидания в секундах, частота проверки условия в секундах
```

**Ожидание определённого элемента** (перед этим открой сайт):

```python
BUTTON = ("xpath", "//button[@id='example']")
```

**Общий синтаксис:**

```python
wait.until(EC.УСЛОВИЕ(locator), message="Ваше кастомное сообщение при ошибке")
```

`wait.until` возвращает веб-элемент!

**Конкретный пример:**

```python
wait.until(EC.visibility_of_element_located(BUTTON))
```

**Дальше можно работать с веб-элементом:**

```python
# Задать его при wait.until
button = wait.until(EC.visibility_of_element_located(BUTTON))
button.click()

# Сначала дождаться, потом найти через поиск элемента
wait.until(EC.visibility_of_element_located(BUTTON))
driver.find_element(*BUTTON).click()
```

---

## ВЕБ-ЭЛЕМЕНТЫ

### Поиск веб-элементов

**WebElement** — это любой объект на странице, такой как кнопка, поле ввода и т.д. Для Selenium это объект типа `WebElement`.

```python
from selenium.webdriver.common.by import By  # класс даёт автодополнение
```

После инициализации браузера и открытия страницы:

```python
driver.find_element()        # поиск одного элемента
driver.find_elements()       # поиск списка элементов
driver.find_elements()[1]    # 2-й элемент списка
element.click()              # клик на элемент
```

**Логика поиска элемента:** указываем способ поиска (класс, id элемента и проч.), затем значение атрибута.

Если элемент в коде страницы `<input id="login_field" class="login"/>`:

```python
driver.find_element(By.ID, "login_field")     # по id
driver.find_element(By.CLASS_NAME, "login")   # по имени класса
driver.find_element(By.TAG_NAME, "input")     # по имени тэга
```

Класс `By` существует для удобного автоввода способа поиска и необязателен.

```python
driver.find_element(By.ID, "login_field")   # с By
driver.find_element("id", "login_field")    # без By
```

**Список обозначений для использования вместо `By`:**

```python
ID = "id"
XPATH = "xpath"
LINK_TEXT = "link text"
PARTIAL_LINK_TEXT = "partial link text"
NAME = "name"
TAG_NAME = "tag name"
CLASS_NAME = "class name"
CSS_SELECTOR = "css selector"
```

### XPath-локаторы

**XPATH (XML Path Language)** — это язык запросов к элементам XML, HTML-документов и других документов класса xml. Основывается на структуре DOM (древовидная структура) и позволяет искать элементы относительно корня, друг друга, соседей и т.д.

**Основные символы:**

- `//` — глобальный поиск относительно корня (начала) документа (обычно корень — это html-тег).
- `/` — поиск по уровню вложенности, например когда элемент внутри элемента (прямой наследник, первый наследник).

**Поиск в коде сайта:**

```xpath
(//headers//div)[3]              # 3-й блок div в блоке headers
//input[@type="email"]            # элемент ввода текста, у которого type = email
//button[contains(@class, "btn")] # кнопка, у которой class содержит btn (актуально при динамических параметрах!)
//button[text()="Sign In"]        # кнопка с текстом Sign In
(//button[text()="Sign In"])[1]  # первая кнопка с текстом Sign In
(//button[@class='btn' and @type="sign"])[1]  # кнопка с классом btn и type sign
```

**Поиск элемента по xpath:**

```python
driver.find_element(By.XPATH, "//input[@class='wikipedia-search-input']")
```

### Кортеж

**Что такое кортеж на примере:**

```python
data = ('Alex', 'QA')

def print_name(first_name, last_name):
    print(first_name, last_name)

print_name(*data)  # чтобы передать в функцию data, добавляем * — распаковываем кортеж
```

Кортеж удобно использовать для передачи данных в `find_element`, ожидания и прочее.

**Пример:**

```python
# Поиск по xpath
driver.find_element("xpath", "//input[@class='wikipedia-search-input']")

# Поиск с кортежем
button = ("xpath", "//input[@class='wikipedia-search-input']")
driver.find_element(*button)
```

### Поля ввода

К текстовым полям можно отнести теги `<input/>` и `<textarea>`.

После инициализации браузера, открытия страницы, когда получили элемент текстового поля с помощью `driver.find_element()`:

```python
assert email_field.get_attribute("value") == ""  # проверить, что поле пустое
element.send_keys('текст 1')                      # ввод текста
element.get_attribute('value')                    # получение текущего текста
element.clear()                                   # удаление текущего текста
```

**Важно:** `value` — это атрибут-текст в поле ввода.

---

## ЗАГРУЗКА И СКАЧИВАНИЕ

### Загрузка

Стандартная загрузка файлов на сайтах реализована тегом `<input>`, а именно `<input type="file"/>`.

Если у кнопки загрузки такой тип, то можно сразу загрузить файл через метод ввода текста — указав директорию и название файла. Если у кнопки загрузки тип у элемента **НЕ** file, значит, элемент с типом file для загрузки скрыт — нужно найти нужный скрытый элемент через `<input type="file"/>` в консоли!

```python
# Поле ввода для загрузки файла
upload_file_field = driver.find_element(By.XPATH, "//input[@type='file']")

# Загружаем картинку
upload_file_field.send_keys(f"{os.getcwd()}\\downloads\\test-upload.png")
```

> **Нюанс:** для пользователей Windows все пути к файлам необходимо прописывать с обратным слешем; иногда даже с двойным.

### Скачивание

```python
# Инициализировать опции браузера
options = webdriver.ChromeOptions()

# Задать особые настройки браузера (куда скачать файл)
preferences = {"download.default_directory": f"{os.getcwd()}\\downloads"}

# Передать указанные опции в инициализацию браузера
options.add_experimental_option('prefs', preferences)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
```

> **Нюанс:** для пользователей Windows все пути к файлам необходимо прописывать с обратным слешем; иногда даже с двойным.

```python
# Получить список картинок-ссылок (скачиваются при нажатии на ссылку)
driver.get('https://the-internet.herokuapp.com/download')
time.sleep(5)
file_list = driver.find_elements(By.XPATH, "//div[@class='example']//a")

# Скачивание — клик на элемент a
file_list[0].click()  # первый элемент списка
```

> Если запустить без `preferences` выше — выскочит окно «куда скачать» и файл не скачается!

---

## COOKIE

**Куки (cookies)** — это небольшие текстовые файлы, которые веб-сайты сохраняют на вашем компьютере, когда вы их посещаете. Когда вы снова посещаете тот же веб-сайт, ваш браузер отправляет эти файлы на сервер, чтобы веб-сайт мог «вспомнить» некоторую информацию о вас.

В реальной жизни, для автоматизации тестирования одна из самых главных областей применения куков — это логин в аккаунт, т.е. авторизация. Их использование позволяет не логиниться каждый раз через форму логина на сайт.

```python
driver.get_cookie("name")      # получить cookie по name (вернёт словарь)
driver.get_cookies()           # получить все cookie с сайта (вернёт список словарей)
driver.add_cookie(DICT)        # добавить новые cookie (передаём словарь)
driver.delete_cookie("name")   # удалить cookie по name
driver.delete_all_cookies()    # удалить все cookie с сайта
```

**Сохранить все cookie с сайта:**

```python
import pickle  # библиотека для работы

# если задача сохранить куки захода в аккаунт — заходим в аккаунт
pickle.dump(driver.get_cookies(), open(f"{os.getcwd()}\\cookies\\cookies.pkl", "wb"))
# 1 что — сохраняем куки; 2 куда — обязательно в формате pkl; 3 операция — записываем биты
```

**Прочитать все cookie из файла pkl:**

```python
import pickle

cookies = pickle.load(open(f"{os.getcwd()}\\cookies\\cookies.pkl", "rb"))
# 1 что — открываем куки из файла; 2 операция — читаем биты
```

**Заменить все cookie на сайте из файла pkl:**

```python
# удаляем все куки методом delete_all_cookies
for cookie in cookies:
    driver.add_cookie(cookie)  # идём по списку словарей куки и проставляем их на сайт

driver.refresh()  # обязательно делаем рефреш страницы, чтобы новые куки применились
```
