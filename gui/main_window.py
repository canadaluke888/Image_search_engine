from PyQt6.QtGui import QPixmap, QIcon, QCursor, QMovie
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog, QListWidget, \
    QListWidgetItem, QHBoxLayout, QMessageBox, QMenu, QApplication
from PyQt6.QtCore import Qt, QThreadPool, QRunnable, pyqtSignal, QObject
import os
import platform

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

        self.loading_label = QLabel()
        self.loading_movie = QMovie('icons/SearchGif.gif')
        self.loading_label.setMovie(self.loading_movie)
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.loading_label)
        self.loading_label.setVisible(False)

        self.result_list = QListWidget()
        self.result_list.itemClicked.connect(self.open_file_explorer)
        self.result_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.result_list.customContextMenuRequested.connect(self.show_context_menu)
        self.main_layout.addWidget(self.result_list)

        self.main_layout.addLayout(self.top_layout)

        self.threadpool = QThreadPool()

        self.num_results = self.get_num_results_setting()
        self.use_cpu = self.get_use_cpu_setting()
        self.search_engine = SearchEngine(use_cpu=self.use_cpu)

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

        self.loading_label.setVisible(True)
        self.loading_movie.start()
        self.result_list.clear()

        worker = ImageSearchWorker(self.search_engine, directory, search_phrase, self.num_results)
        worker.signals.results_ready.connect(self.display_results)
        self.threadpool.start(worker)

    def display_results(self, results):
        self.loading_movie.stop()
        self.loading_label.setVisible(False)
        self.result_list.clear()
        for path, score in results:
            item = QListWidgetItem(f"{path} (Score: {score})")
            thumbnail = QPixmap(path).scaled(100, 100)
            item.setIcon(QIcon(thumbnail))
            item.setData(Qt.ItemDataRole.UserRole, path)
            self.result_list.addItem(item)

    def open_file_explorer(self, item):
        path = item.data(Qt.ItemDataRole.UserRole)

        if platform.system() == 'Windows':
            os.system(f'explorer /select, "{path}"')
        elif platform.system() == 'Darwin':
            os.system(f'open -R "{path}"')
        elif platform.system() == 'Linux':
            QMessageBox.information(self, 'Info', "Your file manager does not support direct file selection on Linux.")
        else:
            QMessageBox.warning(self, 'Warning', 'Unsupported OS for opening file explorer.')

    def show_context_menu(self, position):
        item = self.result_list.itemAt(position)
        if item is not None:
            menu = QMenu()
            copy_action = menu.addAction("Copy")
            action = menu.exec(QCursor.pos())
            if action == copy_action:
                path = item.data(Qt.ItemDataRole.UserRole)
                clipboard = QApplication.clipboard()
                clipboard.setText(path)

    def open_settings(self):
        dialog = SettingsDialog(parent=self)
        if dialog.exec():
            self.num_results = self.get_num_results_setting()
            self.use_cpu = self.get_use_cpu_setting()
            self.search_engine = SearchEngine(use_cpu=self.use_cpu)

    def get_num_results_setting(self):
        settings_dialog = SettingsDialog()
        return settings_dialog.get_num_results_data()

    def get_use_cpu_setting(self):
        settings_dialog = SettingsDialog()
        return settings_dialog.get_use_cpu_setting()


class ImageSearchWorker(QRunnable):
    class Signals(QObject):
        results_ready = pyqtSignal(list)

    def __init__(self, search_engine, directory, search_phrase, top_k):
        super().__init__()
        self.search_engine = search_engine
        self.directory = directory
        self.search_phrase = search_phrase
        self.top_k = top_k
        self.signals = self.Signals()

    def run(self):
        results = self.search_engine.search_images(self.directory, self.search_phrase, top_k=self.top_k)
        self.signals.results_ready.emit(results)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
