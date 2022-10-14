import requests
import os

chapter_number = 1

chapter_number1 = 1

ufr_error = requests.get("https://img3.cdnlibs.link//manga/all-you-need-is-kill/chapters/1-1/33.jpg")

error = 0
while True:
    chapter_dir1 = r'C:\Users\Dimash\Pictures\Manga\\' + str(chapter_number)
    chapter_url1 = "https://img3.cdnlibs.link//manga/all-you-need-is-kill/chapters/" + str(chapter_number)
    error1 = 0
    while True:
        chapter_dir = chapter_dir1 + '-' + str(chapter_number) + '\\'
        chapter_url = chapter_url1 + "-" + str(chapter_number) + "/"
        os.mkdir(chapter_dir)
        number = 1
        while True:
            url = chapter_url + str(number).zfill(2) + ".jpg"
            ufr = requests.get(url)
            if ufr.content == ufr_error.content:
                url = chapter_url + str(number).zfill(2) + ".png"
                ufr = requests.get(url)
                if ufr.content == ufr_error.content:
                    error += 1
                    error1 += 1
                    break
                f = open(chapter_dir + str(number).zfill(2) + '.png', "wb+")
                f.write(ufr.content)  # записываем содержимое в файл; как видите - content запроса
                f.close()
                number += 1
                continue
            f = open(chapter_dir + str(number).zfill(2) + '.jpg', "wb+")
            f.write(ufr.content)  # записываем содержимое в файл; как видите - content запроса
            f.close()
            number += 1

        if error1 == 2:
            break

        chapter_number += 1

    if error == 3:
        break
    chapter_number1 += 1