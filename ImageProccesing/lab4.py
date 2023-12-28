import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QMessageBox, QCheckBox
from PyQt5.QtCore import Qt
import threading
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from typing import Callable

class ImageProcessorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.input_folder = ""
        self.output_folder = "output"

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel('Выберите папку с изображениями')
        layout.addWidget(self.label)

        select_folder_btn = QPushButton('Выбрать папку')
        select_folder_btn.clicked.connect(self.show_folder_dialog)
        layout.addWidget(select_folder_btn)

        self.sharpen_checkbox = QCheckBox('Применить Sharpen фильтр')
        layout.addWidget(self.sharpen_checkbox)

        self.sepia_checkbox = QCheckBox('Применить Sepia фильтр')
        layout.addWidget(self.sepia_checkbox)

        self.resize_checkbox = QCheckBox('Применить Resize фильтр')
        layout.addWidget(self.resize_checkbox)

        process_images_btn = QPushButton('Обработать изображения')
        process_images_btn.clicked.connect(self.process_images)
        layout.addWidget(process_images_btn)

        self.setLayout(layout)

    def show_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Выберите папку с изображениями', os.path.expanduser('~'))
        if folder_path:
            self.input_folder = folder_path
            self.label.setText(f'Выбрана папка: {self.input_folder}')

    def prepare(self, image_path, output_path,  filters: list[str]):
        image = Image.open(image_path)
        if "sepia" in filters:
            image = ImageOps.colorize(image.convert("L"), "#704214", "#C0A080")
        if "resize" in filters:
            image = image.resize((512, 512))
        if "sharpen" in filters:
            image = image.filter(ImageFilter.SHARPEN)
        output_path = os.path.join(self.output_folder, os.path.basename(output_path)) + ".formated.png"

        image.save(output_path)
        print(f'All selected filters applied to {image_path} and saved to {output_path}')

    def show_message_box(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle('Генерация завершена')
        msg.exec_()

    def process_images(self):
        if not self.input_folder:
            self.show_message_box('Выберите папку с изображениями.')
            return

        os.makedirs(self.output_folder, exist_ok=True)

        image_files = [f for f in os.listdir(self.input_folder) if f.endswith(('.png', '.jpg', '.jfif'))]
        new_size = (200, 200)

        threads = []
        for image_file in image_files:
            input_path = os.path.join(self.input_folder, image_file)
            output_path = os.path.join(self.output_folder, image_file)

            filters = []
            if self.sharpen_checkbox.isChecked():
                filters.append("sharpen")

            if self.sepia_checkbox.isChecked():
                filters.append("sepia")

            if self.resize_checkbox.isChecked():
                filters.append("resize")

            threads.append(threading.Thread(target=self.prepare, args=(input_path, output_path, filters)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        self.show_message_box('Генерация изображений завершена.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageProcessorApp()
    window.setWindowTitle('Image Processor')
    window.setGeometry(100, 100, 400, 250)
    window.show()
    sys.exit(app.exec_())
