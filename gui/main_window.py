import os

from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog, QListWidget, \
    QListWidgetItem, QHBoxLayout
from PyQt6.QtCore import Qt

from search_engine.clip_search_engine import SearchEngine
from gui.settings_dialog import SettingsDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Search Engine")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.top_layout = QHBoxLayout()
        self.settings_button = QPushButton('Settings')
        self.settings_button.clicked.connect(self.open_settings)
        self.top_layout.addWidget(self.settings_button)


        self.main_layout = QVBoxLayout(self.central_widget)

        self.label = QLabel("Select Directory:")
        self.main_layout.addWidget(self.label)

        self.directory_line_edit = QLineEdit()
        self.main_layout.addWidget(self.directory_line_edit)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_directory)
        self.main_layout.addWidget(self.browse_button)

        self.search_label = QLabel("Enter Search Phrase:")
        self.main_layout.addWidget(self.search_label)

        self.search_line_edit = QLineEdit()
        self.main_layout.addWidget(self.search_line_edit)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_images)
        self.main_layout.addWidget(self.search_button)

        self.result_list = QListWidget()
        self.main_layout.addWidget(self.result_list)

        self.main_layout.addLayout(self.top_layout)

        self.search_engine = SearchEngine()
        self.num_results = self.get_num_results_setting()

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.directory_line_edit.setText(directory)

    def search_images(self):
        directory = self.directory_line_edit.text()
        search_phrase = self.search_line_edit.text()

        if not os.path.isdir(directory):
            self.result_list.clear()
            self.result_list.addItem("Invalid directory.")
            return

        if not search_phrase:
            self.result_list.clear()
            self.result_list.addItem("Please enter a search phrase.")
            return

        results = self.search_engine.search_images(directory, search_phrase, top_k=self.num_results)
        self.display_results(results)

    def display_results(self, results):
        self.result_list.clear()
        for path, score in results:
            item = QListWidgetItem(f"{path} (Score: {score})")
            thumbnail = QPixmap(path).scaled(100, 100)
            item.setIcon(QIcon(thumbnail))
            self.result_list.addItem(item)

    def open_settings(self):
        dialog = SettingsDialog(parent=self)
        if dialog.exec():
            self.num_results = self.get_num_results_setting()

    def get_num_results_setting(self):
        settings_dialog = SettingsDialog()
        return settings_dialog.get_num_results_data()