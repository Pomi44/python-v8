import requests
from bs4 import BeautifulSoup
import os

def url(page):
    book_url = "https://www.livelib.ru/reviews/~" + str(page) + "#reviews"
    return book_url

# Создаем папки для хранения рецензий
if not os.path.exists("dataset/good"):
    os.makedirs("dataset/good")
if not os.path.exists("dataset/bad"):
    os.makedirs("dataset/bad")

good_reviews = 0
bad_reviews = 0
max_reviews_for_one_book = 10
page_number = 2

# Находим блоки с рецензиями 
while good_reviews < max_reviews_for_one_book or bad_reviews < max_reviews_for_one_book:
    book_reviews = url(page_number)
    response = requests.get(book_reviews)
    soup = BeautifulSoup(response.content, "html.parser")
    if response.status_code == 200:
        review_blocks = soup.find_all('article', class_="review-card lenta__item")
        for review_block in review_blocks:
            # Получаем текст рецензии
            review_text = review_block.find('div', class_="lenta-card__text without-readmore").get_text()

            # Определяем, является ли рецензия "good" или "bad"
            rating = int(review_block.find('span', class_='lenta-card__mymark').text.strip())
            if rating <= 3:       
                category = "bad"      
            else:
                category = "good" 

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
            book_title = review_block.find('a', class_='lenta-card__book-title').text.strip()
            # Записываем информацию в файл
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(f"Book: {book_title}\n")
                file.write(review_text)
        page_number += 1
    else:
        print("Ошибка при отправке запроса на страницу.")
        break  # Выход из цикла в случае ошибки
print(f"Собрано {good_reviews+1} хороших рецензий и {bad_reviews+1} плохих рецензий.")


    