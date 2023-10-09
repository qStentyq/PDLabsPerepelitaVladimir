import os
import requests
from bs4 import BeautifulSoup
import urllib.parse

# Функция для создания папки, если она не существует
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Функция для загрузки изображений
#1 page = 30 images
def download_images(search_query, output_directory, num_pages):
    create_directory(output_directory)
    base_url = "https://yandex.ru/images/search"

    for i in range(num_pages):
        query_params = {
            "text": search_query + str(i),
        }

        img_tags = []
        response = requests.get(base_url, params=query_params)
        print(response.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)
        img_tags = soup.find_all("img", {"class": "serp-item__thumb"}) 
       
        

        for img_tag in img_tags:
            # print(img_tag)
            img_url = img_tag["src"]
            img_url = urllib.parse.urljoin(base_url, img_url)
            # print(img_url)
            img_data = requests.get(img_url).content
            # print(img_data)

            # Создаем имя файла в формате 0000.jpg, 0001.jpg и т.д.
            filename = f"{i * len(img_tags) + img_tags.index(img_tag):04d}.jpg"
            file_path = os.path.join(output_directory, filename)

            # Записываем изображение в файл
            with open(file_path, 'wb') as img_file:
                img_file.write(img_data)

# Загрузка изображений polar bear
# download_images("polar bear", "dataset/polar_bear", 50)

# Загрузка изображений brown bear
download_images("brown bear", "dataset/brown_bear", 10)
# download_images("dota 2", "dataset/pussy", 10)



 