import os
import shutil

# Функция для копирования датасета с переименованием файлов
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

# Пример вызова функции
copy_dataset_with_rename('dataset\\', 'renamed_dataset')  # Копируем датасет с переименованием в новую директорию
