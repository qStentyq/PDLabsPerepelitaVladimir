import os
import csv

# Функция для создания файла-аннотации
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

# Пример вызова функции
create_annotation_file('dataset\\', 'annotations.csv')
