import sys
import cv2
import numpy as np
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class ImageFilterProgram(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Filter Program")

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)

        self.filter_button = QPushButton("Grayscale Filter")
        self.filter_button.clicked.connect(self.Grayscale_filter)

        self.filter_button1 = QPushButton("Blur Filter")
        self.filter_button1.clicked.connect(self.Blur_filter)

        self.filter_button2 = QPushButton("Edge Detection Filter")
        self.filter_button2.clicked.connect(self.Edge_Detection_filter)

        self.filter_button3 = QPushButton("Sharpening Filter")
        self.filter_button3.clicked.connect(self.Sharpening_filter)

        self.filter_button4 = QPushButton("Gamma Correction Filter")
        self.filter_button4.clicked.connect(self.Gamma_Correction_filter)

        self.filter_button5 = QPushButton("Color Transformation Filter")
        self.filter_button5.clicked.connect(self.Color_Transformation_filter)

        self.filter_button6 = QPushButton("Apply Filter")
        self.filter_button6.clicked.connect(self.apply_filter)

        self.filter_button7 = QPushButton("Resize Filter")
        self.filter_button7.clicked.connect(self.Resize_filter_dialog)

        self.analyze_button = QPushButton("Analyze Image")
        self.analyze_button.clicked.connect(self.analyze_image)
        self.analyze_button.setEnabled(False)

        self.resolution_label = QLabel()
        self.rgb_color_label = QLabel()
        self.hsv_color_label = QLabel()
        self.file_size_label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.load_button)
        layout.addWidget(self.filter_button)
        layout.addWidget(self.filter_button1)
        layout.addWidget(self.filter_button2)
        layout.addWidget(self.filter_button3)
        layout.addWidget(self.filter_button4)
        layout.addWidget(self.filter_button5)
        layout.addWidget(self.filter_button6)
        layout.addWidget(self.filter_button7)
        layout.addWidget(self.analyze_button)
        layout.addWidget(self.resolution_label)
        layout.addWidget(self.rgb_color_label)
        layout.addWidget(self.hsv_color_label)
        layout.addWidget(self.file_size_label)
        self.setLayout(layout)

        self.image = None

    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)",
            options=options
        )
        if file_path:
            self.image = cv2.imread(file_path)
            self.display_image()
            self.analyze_button.setEnabled(True)

    def Grayscale_filter(self):
        if self.image is not None:
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.image = gray_image
            self.display_image()

    def Blur_filter(self):
        if self.image is not None:
            blurred_image = cv2.blur(self.image, (5, 5))
            self.image = blurred_image
            self.display_image()

    def Edge_Detection_filter(self):
        if self.image is not None:
            edges = cv2.Canny(self.image, 100, 200)
            self.image = edges
            self.display_image()

    def Sharpening_filter(self):
        if self.image is not None:
            kernel = np.array([[-1, -1, -1],
                               [-1,  9, -1],
                               [-1, -1, -1]])
            sharpened_image = cv2.filter2D(self.image, -1, kernel)
            self.image = sharpened_image
            self.display_image()

    def Gamma_Correction_filter(self):
        if self.image is not None:
            gamma = 1.5
            gamma_corrected = np.power(self.image / 255.0, gamma) * 255.0
            gamma_corrected = gamma_corrected.astype(np.uint8)
            self.image = gamma_corrected
            self.display_image()

    def Color_Transformation_filter(self):
        if self.image is not None:
            converted_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
            self.image = converted_image
            self.display_image()

    def apply_filter(self):
        if self.image is not None:
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
            self.image = binary_image
            self.display_image()

    def Resize_filter_dialog(self):
        if self.image is not None:
            dialog = FilterDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                width_ratio = dialog.get_width_ratio()
                height_ratio = dialog.get_height_ratio()

                resized_image = cv2.resize(self.image, None, fx=width_ratio, fy=height_ratio)
                self.image = resized_image
                self.display_image()

    def analyze_image(self):
        if self.image is not None:
            height, width, _ = self.image.shape
            resolution_text = f"Resolution: {width} x {height}"
            self.resolution_label.setText(resolution_text)

            rgb_info = self.calculate_color_info(self.image, 'RGB')
            hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
            hsv_info = self.calculate_color_info(hsv_image, 'HSV')

            rgb_text = "RGB Color Information:\n"
            for channel, value in rgb_info.items():
                rgb_text += f"{channel}: {value}\n"
            self.rgb_color_label.setText(rgb_text)

            hsv_text = "HSV Color Information:\n"
            for channel, value in hsv_info.items():
                hsv_text += f"{channel}: {value}\n"
            self.hsv_color_label.setText(hsv_text)

            file_path = "temp_image.png"
            counter = 1
            while os.path.exists(file_path):
                file_path = f"temp_image{counter}.png"
                counter += 1

            cv2.imwrite(file_path, self.image)
            file_size = os.path.getsize(file_path)
            file_size_text = f"File Size: {file_size} bytes"
            self.file_size_label.setText(file_size_text)

            os.remove(file_path)

    def display_image(self):
        if self.image is not None:
            image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            height, width, channel = image_rgb.shape
            bytes_per_line = channel * width
            q_image = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)

            scaled_pixmap = pixmap.scaled(640, 480, Qt.KeepAspectRatio)
            self.image_label.setPixmap(scaled_pixmap)

    def calculate_color_info(self, image, color_space):
        channels = cv2.split(image)
        color_info = {}
        if color_space == 'RGB':
            channel_names = ['Red', 'Green', 'Blue']
        elif color_space == 'HSV':
            channel_names = ['Hue', 'Saturation', 'Value']

        for i, channel_name in enumerate(channel_names):
            channel_values = channels[i].ravel()
            channel_mean = np.mean(channel_values)
            channel_std = np.std(channel_values)
            color_info[channel_name] = f"Mean: {channel_mean:.2f}, Std: {channel_std:.2f}"
        return color_info

class FilterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resize filter")

        self.width_input = QLineEdit()
        self.height_input = QLineEdit()

        form_layout = QFormLayout()
        form_layout.addRow("Enter width ratio:", self.width_input)
        form_layout.addRow("Enter height ratio:", self.height_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

    def get_width_ratio(self):
        return float(self.width_input.text())

    def get_height_ratio(self):
        return float(self.height_input.text())

def open_image_filter_program():
    app = QApplication(sys.argv)
    program = ImageFilterProgram()
    program.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    open_image_filter_program()
