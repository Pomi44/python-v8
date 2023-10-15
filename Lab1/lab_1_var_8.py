import requests
from bs4 import BeautifulSoup
import os
import re
    
def url(film):
    film_url = "https://www.rottentomatoes.com/m/" + film + "/reviews?type=user"
    return film_url

# Создаем папки для хранения рецензий
if not os.path.exists("dataset/good"):
    os.makedirs("dataset/good")
if not os.path.exists("dataset/bad"):
    os.makedirs("dataset/bad")

films=["the_equalizer_3","taylor_swift_the_eras_tour","anatomy_of_a_fall"]
for film in films:
    film_reviews = url(film)
    good_reviews = 0
    bad_reviews = 0
    max_reviews_for_one_film = 400
    page_number = 2
    response = requests.get(film_reviews)
    soup = BeautifulSoup(response.text, "html.parser") 
    movie_title = film    
    # Находим блоки с рецензиями 
    while good_reviews < max_reviews_for_one_film or bad_reviews < max_reviews_for_one_film:
        response = requests.get(film_reviews, params={"page": page_number})
        if response.status_code == 200:
            review_blocks = soup.find_all('div',class_="audience-review-row")
            for review_block in review_blocks:
                # Получаем текст рецензии
                review_text = review_block.find('p', class_="audience-reviews__review js-review-text").get_text()
                # Определяем, является ли рецензия "good" или "bad"
                star_display = review_block.find('span', class_='star-display')
                filled_stars = star_display.find_all('span', class_='star-display__filled')
                half_stars = star_display.find_all('span', class_='star-display__half')
                count_filled_stars = len(filled_stars)+ len(half_stars)
                if count_filled_stars <=3:       
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
                
                # Записываем информацию в файл
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(f"Movie: {movie_title}\n")
                    file.write(review_text)
            page_number += 1
        else:
            print("Ошибка при отправке запроса на страницу.")
        break
print(f"Собрано {good_reviews+1} хороших рецензий и {bad_reviews+1} плохих рецензий.")
    