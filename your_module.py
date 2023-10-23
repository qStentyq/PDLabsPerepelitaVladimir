import os
import csv
import shutil
import random

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
