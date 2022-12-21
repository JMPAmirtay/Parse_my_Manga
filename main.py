import time

import os
import urllib.request
from selenium.common.exceptions import ElementNotInteractableException

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Подключаемся к Селениуму
options = Options()
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
browser = webdriver.Firefox(options=options,
                            executable_path=r"venv\driver\geckodriver.exe")

# Заходим на Мангалиб
browser.get('https://mangalib.me/')

# Что находиться внутри элемента?
# elem.get_attribute('innerHTML')

# Нажимаем кнопку поиск
browser.find_element(By.ID, 'search-link').click()
# Вводим в адресную строку интересующую мангу
browser.find_element(By.TAG_NAME, 'input').send_keys("onepunchman")
time.sleep(2)
# Нажимаем на первую встречную
browser.find_element(By.CLASS_NAME, 'manga-list-item__cover').click()
time.sleep(1)
# Убираем ненужное окно
browser.find_element(By.CLASS_NAME, 'media-sidebar').find_elements(By.TAG_NAME, 'a')[3].click()
time.sleep(2)

# Смотрим сколько глав в манге
browser.find_elements(By.CLASS_NAME, 'reader-header-action__text')[1].click()
browser.find_elements(By.CLASS_NAME, 'modal__close')[2].click()

# Записываем номер последней главы
last_chapter = int(browser.find_element(By.CLASS_NAME, 'menu__item').text.split(" - ")[0].split(" ")[-1])
print(last_chapter)

# Записываем номер текущей главы
now_chapter = int(browser.find_elements(By.CLASS_NAME, 'reader-header-action__text')[1].text.split(" ")[-1])
print(now_chapter)

# Сверяем их и когда дойдёт до последней главы программа завершается
while now_chapter < last_chapter:
    url = browser.find_element(By.TAG_NAME, 'img').get_attribute('src')

    name = url.split("/")[-4]
    # Создаем все нужные папки
    if not os.path.isdir('Download'):
        os.mkdir('Download')
    if not os.path.isdir('Download/' + name):
        os.mkdir('Download/' + name)
    if not os.path.isdir('Download/' + name + "/chapters"):
        os.mkdir('Download/' + name + "/chapters")
    # Записываем последюю страницу в главе
    lost_img_number = int(browser.find_element(By.CLASS_NAME, 'reader-pages__label').text.split("/")[-1])

    # Цикл работает столько сколько страниц в главе
    for img_number in range(0, lost_img_number):
        url = browser.find_elements(By.TAG_NAME, 'img')[img_number].get_attribute('src')

        # Записываем номер главы
        chapter = url.split("/")[-2]

        # Записываем имя картинки
        name_img = url.split("/")[-1]

        # Создаем папку с главой
        if not os.path.isdir('Download/' + name + "/chapters/" + chapter):
            os.mkdir('Download/' + name + "/chapters/" + chapter)

        # Записываем изображение
        urllib.request.urlretrieve(url, 'Download/' + name + "/chapters/" + chapter + "/" + name_img)

        # Нажимаем на картинку
        try:
            browser.find_elements(By.TAG_NAME, 'img')[img_number].click()
        except ElementNotInteractableException:
            time.sleep(1)

    # Обновляем текущую главу
    print(browser.find_elements(By.CLASS_NAME, 'reader-header-action__text')[1].text)
    now_chapter = int(browser.find_elements(By.CLASS_NAME, 'reader-header-action__text')[1].text.split(" ")[-1])

    # Последняя итерация
    if now_chapter == last_chapter:
        now_chapter += 1
