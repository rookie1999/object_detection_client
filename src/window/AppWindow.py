import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QScrollArea, \
    QTextEdit, QHBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class ImageLabel(QLabel):
    def __init__(self, parent, width_ratio, height_ratio):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.width_ratio = width_ratio
        self.height_ratio = height_ratio

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setFixedSize(self.parent().width() * self.width_ratio, self.parent().height() * self.height_ratio)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("目标检测")
        self.setGeometry(50, 50, 800, 600)

        main_layout = QVBoxLayout()

        self.image_label = ImageLabel(self, 0.8, 0.6)
        self.prediction_label = ImageLabel(self, 0.8, 0.6)

        self.label1 = QLabel('请上传待预测图片')
        self.label1.setFixedWidth(200)
        self.upload_button = QPushButton('选择图片')
        self.upload_button.setFixedWidth(150)
        self.upload_button.clicked.connect(self.open_file)

        self.label2 = QLabel('请输入要预测的标签')
        self.label2.setFixedWidth(200)
        self.add_text_button = QPushButton('添加标签')
        self.add_text_button.setFixedWidth(150)
        self.add_text_button.clicked.connect(self.add_text_field)

        self.selectImgLayout = QHBoxLayout()
        self.selectImgLayout.addWidget(self.label1, alignment=Qt.AlignLeft)
        self.selectImgLayout.addWidget(self.upload_button, alignment=Qt.AlignLeft)

        self.addLabelLayout = QHBoxLayout()
        self.addLabelLayout.addWidget(self.label2, alignment=Qt.AlignLeft)
        self.addLabelLayout.addWidget(self.add_text_button, alignment=Qt.AlignLeft)

        # 创建一个垂直布局的滚动区域
        self.labels_layout = QVBoxLayout()
        self.labels_layout.setAlignment(Qt.AlignLeft)
        self.scroll_area = QScrollArea()
        self.scroll_area.setMinimumHeight(self.height() * 0.2)
        self.scroll_area.setMaximumHeight(self.height() * 0.4)
        self.scroll_area_widget_contents = QWidget()
        self.scroll_area_widget_contents.setLayout(self.labels_layout)
        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        self.scroll_area.setWidgetResizable(True)

        self.predictBtn = QPushButton("Predict")
        self.predictBtn.setMinimumHeight(50)
        self.predictBtn.setMinimumWidth(400)
        self.predictBtn.clicked.connect(self.open_file2)

        self.picTextLayout = QHBoxLayout()
        self.rawPicText = QLabel('原始图片')
        self.predPicText = QLabel('预测后的图片')
        self.picTextLayout.addWidget(self.rawPicText, alignment=Qt.AlignLeft)
        self.picTextLayout.addWidget(self.predPicText, alignment=Qt.AlignRight)

        self.picImageLayout = QHBoxLayout()
        self.picImageLayout.addWidget(self.image_label, alignment=Qt.AlignLeft)
        self.picImageLayout.addWidget(self.prediction_label, alignment=Qt.AlignRight)

        main_layout.addLayout(self.selectImgLayout)
        main_layout.addLayout(self.addLabelLayout)
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(self.predictBtn, alignment=Qt.AlignRight)
        main_layout.addLayout(self.picTextLayout)
        main_layout.addLayout(self.picImageLayout)


        self.add_text_field()
        self.setLayout(main_layout)

        self.show()

    def open_file(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;JPEG Files (*.jpeg);;PNG Files (*.png)",
                                                  options=options)
        if filename:
            pixmap = QPixmap(filename)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(),
                                                     Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def add_text_field(self):
        layout = QHBoxLayout()
        text_edit = QTextEdit()
        text_edit.setFixedSize(400, 30)
        button = QPushButton('删除标签')
        button.setProperty("label", text_edit)
        button.setProperty("layout", layout)
        button.setFixedSize(150, 30)
        button.clicked.connect(self.removeTextEdit)
        layout.addWidget(text_edit)
        layout.addWidget(button)
        self.labels_layout.addLayout(layout)  # 将文本框和按钮添加到垂直布局中

    def show_prediction(self, pixmap):
        self.prediction_label.setPixmap(
            pixmap.scaled(self.prediction_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def removeTextEdit(self):
        source = self.sender()
        text_edit = source.property("label")
        layout = source.property("layout")
        layout.removeWidget(text_edit)
        layout.removeWidget(source)
        del layout

    def open_file2(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;JPEG Files (*.jpeg);;PNG Files (*.png)",
                                                  options=options)
        if filename:
            pixmap = QPixmap(filename)
            self.show_prediction(pixmap)
