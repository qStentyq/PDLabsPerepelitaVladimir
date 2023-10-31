import os
import csv
import shutil
import random
from bs4 import BeautifulSoup
import urllib.parse
import requests

def create_annotation_file(dataset_path, annotation_file):
    with open(annotation_file, 'w', newline='') as csvfile: # Открываем файл для записи
        csvwriter = csv.writer(csvfile, delimiter='|') # Создаем объект для записи CSV
        csvwriter.writerow(['Absolute Path', 'Relative Path', 'Class Label']) # Записываем заголовок

        # Рекурсивно обходим все файлы и директории внутри dataset_path
        for root, _, files in os.walk(dataset_path):
            for file in files:
                if file.endswith(".jpg"):  # Предполагается, что jpg изображения
                    absolute_path = os.path.join(f"{os.getcwd()}", root, file) # Получаем абсолютный путь к файлу
                    print(absolute_path) # Выводим абсолютный путь (можно удалить эту строку)
                    relative_path = os.path.relpath(absolute_path, dataset_path) # Получаем относительный путь относительно dataset_path
                    class_label = os.path.basename(root) # Извлекаем метку класса из имени директории
                    csvwriter.writerow([absolute_path, relative_path, class_label]) # Записываем данные в CSV файл

def copy_dataset_with_rename(source_path, destination_path):
    for root, _, files in os.walk(source_path):  # Рекурсивно обходим файлы и директории в исходной директории
        for file in files:
            if file.endswith(".jpg"):  # Предполагается, что у вас jpg изображения
                class_label = os.path.basename(root)  # Извлекаем метку класса из имени текущей директории
                new_filename = f'{class_label}_{file}'  # Создаем новое имя файла, включая метку класса
                source_file = os.path.join(root, file)  # Формируем путь к исходному файлу
                destination_file = os.path.join(destination_path, new_filename)  # Формируем путь к файлу в целевой директории
                print(class_label, '\t', new_filename, '\t', source_file, '\t', destination_file)  # Выводим информацию о копировании
                shutil.copyfile(source_file, destination_file)  # Копируем файл с новым именем в целевую директорию

# Функция для создания копии датасета с случайными именами файлов
def copy_dataset_with_random_names(source_path, destination_path):
    for root, _, files in os.walk(source_path):  # Рекурсивно обходим файлы и директории в исходной директории
        for file in files:
            if file.endswith(".jpg"): 
                random_name = f'{random.randint(0, 10000):04d}.jpg'  # Генерируем случайное имя файла
                source_file = os.path.join(root, file)  # Формируем путь к исходному файлу
                destination_file = os.path.join(destination_path, random_name)  # Формируем путь к файлу в целевой директории
                shutil.copyfile(source_file, destination_file)  # Копируем файл с новым случайным именем в целевую директорию

def get_next_instance(class_label, dataset_path):

    instances = []  # Создаем пустой список для хранения экземпляров класса
    for root, _, files in os.walk(os.path.join(dataset_path, class_label)):  # Рекурсивно обходим файлы и директории в папке, соответствующей метке класса
        for file in files:
            if file.endswith(".jpg"):  
                instances.append(os.path.join(root, file))  # Добавляем абсолютный путь к изображению в список instances
    print(instances)
    return iter(instances)  # Возвращаем итератор для последовательного доступа к экземплярам

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Функция для загрузки изображений

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
            print(img_url)
            img_data = requests.get(img_url).content
            # print(img_data)

            # Создаем имя файла в формате 0000.jpg, 0001.jpg и т.д.
            filename = f"{i * len(img_tags) + img_tags.index(img_tag):04d}.jpg"
            file_path = os.path.join(output_directory, filename)

            # Записываем изображение в файл
            with open(file_path, 'wb') as img_file:
                img_file.write(img_data)

