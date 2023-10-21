import requests
from bs4 import BeautifulSoup
import os
from time import sleep
import logging
import random

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}
logging.basicConfig(level=logging.INFO)

def get_page(page):
    url = "https://www.livelib.ru/reviews/~" + str(page)
    try:
        sleep_time = random.uniform(5, 7)
        sleep(sleep_time)
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    except requests.exceptions.RequestException:
        logging.error(f"Ошибка при получении страницы")
        return None
    except Exception as e:
        logging.error(f"Необработанная ошибка")
        return None

def create_dataset():
    try:
        if not os.path.exists("dataset/good"):
            os.makedirs("dataset/good")
        if not os.path.exists("dataset/bad"):
            os.makedirs("dataset/bad")
    except Exception:
        logging.exception(f"Ошибка при создании папки")


def process_review(review_block, good_reviews, bad_reviews):
    try:
        # Получаем текст рецензии
        text_element = review_block.find('div', class_="lenta-card__text without-readmore")
        if text_element is not None:
            review_text = text_element.get_text()
        else:
            review_text = "Текст рецензии не найден"
            print(review_text)
        # Определяем, является ли рецензия "good" или "bad"
        rating_element = soup.find('span', class_='lenta-card__mymark')
        if rating_element is not None:
            rating = float(rating_element.get_text())
            if rating <= 3:
                category = "bad"
            else:
                category = "good"
        else:
            category = "unknown"
            print(category)

        # Создаем уникальный идентификатор в виде числа от 0001 до 0999
        if category == "good":
            good_reviews = len(os.listdir("dataset/good"))
            unique_id = str(good_reviews + 1).zfill(4)
        else:
            bad_reviews = len(os.listdir("dataset/bad"))
            unique_id = str(bad_reviews + 1).zfill(4)

        # Создаем путь к файлу, включая папку с категорией
        file_name = f"{unique_id}_{category}.txt"
        file_path = os.path.join("dataset", category, file_name)
        book_title_ = review_block.find('a', class_='lenta-card__book-title')
        if book_title_ is not None:
            book_title = book_title_.text.strip()
        else:
            book_title = "Название книги не найдено"
            print(book_title)

        # Записываем информацию в файл
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"Book: {book_title}\n")
            file.write(review_text)
    except Exception:
        # Обработка ошибки при обработке рецензии
        print(f"Ошибка при обработке рецензии")

    return good_reviews, bad_reviews



good_reviews = 0
bad_reviews = 0
max_reviews_for_one_book = 10
page_number = 2

while good_reviews < max_reviews_for_one_book or bad_reviews < max_reviews_for_one_book:
    soup = get_page(page_number)
    if soup:
        review_blocks = soup.find_all('article', class_="review-card lenta__item")
        for review_block in review_blocks:
            good_reviews, bad_reviews = process_review(review_block, good_reviews, bad_reviews)
        page_number += 1
    else:
        print("Ошибка при отправке запроса на страницу.")
        break

print(f"Собрано {good_reviews+1} хороших рецензий и {bad_reviews+1} плохих рецензий.")




    