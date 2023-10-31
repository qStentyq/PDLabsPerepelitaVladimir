import os
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt


# Импортируем функции для выполнения задач из предыдущих скриптов
from your_module import create_annotation_file, copy_dataset_with_rename, copy_dataset_with_random_names, get_next_instance, create_directory, download_images

class DatasetApp(QtWidgets.QMainWindow): #Создание класса с интерфейсом
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Dataset App")
        self.setGeometry(100, 100, 400, 300)

        self.number_pages = 1
        self.image_name = ''
        self.folderpath = ''
        self.current_class_label = 'polar_bear'  
        self.current_instance_generator = None

        #Добавляем кнопки для удобного пользования функционалом интерфейса
        self.btn_download_data = QtWidgets.QPushButton("Dowload new data", self)
        self.btn_download_data.clicked.connect(self.download_data)

        self.btn_select_folder = QtWidgets.QPushButton("Select Dataset Folder", self)
        self.btn_select_folder.clicked.connect(self.select_folder)

        self.btn_create_annotation = QtWidgets.QPushButton("Create Annotation File", self)
        self.btn_create_annotation.clicked.connect(self.create_annotation)

        self.btn_next_instance = QtWidgets.QPushButton("Next Image", self)
        self.btn_next_instance.clicked.connect(self.get_next_instance_file)

        self.btn_change_class = QtWidgets.QPushButton("Change Class Label", self)
        self.btn_change_class.clicked.connect(self.change_class_label)

        #Переменная для хранения картинок
        self.label_image = QtWidgets.QLabel(self)
        self.label_image.setAlignment(Qt.AlignCenter) 

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.btn_download_data)
        layout.addWidget(self.btn_select_folder)
        layout.addWidget(self.btn_create_annotation)
        layout.addWidget(self.btn_change_class)
        layout.addWidget(self.btn_next_instance)
        layout.addWidget(self.label_image)

        container = QtWidgets.QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def download_data(self):
        text,ok = QtWidgets.QInputDialog.getText(self, 'Data Download', 'Enter text:')
        if ok:
             self.image_name = str(text)
             if self.image_name:
                download_images(self.image_name, "dataset/" + self.image_name, self.number_pages)
    def change_class_label(self, ):
        text,ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Enter text:')
        if ok:
             self.current_class_label = str(text)
             if self.folderpath and self.current_class_label:
                self.current_instance_generator = get_next_instance(self.current_class_label, self.folderpath)
    def select_folder(self):
        self.folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Dataset Folder')
        
        # Установите self.current_instance_generator после выбора папки
        if self.folderpath and self.current_class_label:
            self.current_instance_generator = get_next_instance(self.current_class_label, self.folderpath)


    def create_annotation(self):
        if self.folderpath:
            create_annotation_file(self.folderpath, 'annotations.csv')
            

    def get_next_instance_file(self):
        print(self.current_instance_generator)
        if self.folderpath and self.current_instance_generator:
            try:
                next_instance = next(self.current_instance_generator)

                # Отладочный вывод
                print(f"Loading image: {next_instance}")

                pixmap = QtGui.QPixmap(next_instance)  # Загрузка изображения (путь к изображению)
                self.label_image.setPixmap(pixmap)  # Установка изображения в QLabel

            except StopIteration:
                self.current_instance_generator = None
                print("No more instances.")
                pixmap = QtGui.QPixmap('noImages')
                pixmap_resized = pixmap.scaled(400, 320, Qt.KeepAspectRatio)
                self.label_image.setPixmap(pixmap_resized)

#Запуск интерфейса 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = DatasetApp()
    window.show()
    sys.exit(app.exec_())


