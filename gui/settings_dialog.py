import json
import os
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton, QCheckBox, QMessageBox, QApplication

from search_engine.clip_search_engine import SearchEngine


class SettingsDialog(QDialog):
    def __init__(self, settings_path='settings_data/settings_data.json', parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.settings_file = settings_path
        self.setWindowTitle('Settings')
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.num_results_label = QLabel('Number of Results:')
        self.num_results_input = QSpinBox()
        self.num_results_input.setMaximum(20)
        self.num_results_input.setMinimum(3)
        self.num_results_input.setValue(self.get_num_results_data())

        layout.addWidget(self.num_results_label)
        layout.addWidget(self.num_results_input)

        self.cpu_checkbox = QCheckBox("Use CPU instead of GPU")
        layout.addWidget(self.cpu_checkbox)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        self.setLayout(layout)

        if not SearchEngine.is_cuda_available():
            self.cpu_checkbox.hide()
        else:
            self.cpu_checkbox.setChecked(self.get_use_cpu_setting())

    def get_num_results_data(self) -> int:
        settings = self.load_settings()
        return settings.get('num_results', 3)  # Default to 3 if not found

    def get_use_cpu_setting(self) -> bool:
        settings = self.load_settings()
        return settings.get('use_cpu', False)  # Default to False if not found

    def save_settings(self):
        num_results = self.num_results_input.value()
        use_cpu = self.cpu_checkbox.isChecked()

        settings = {
            "num_results": num_results,
            "use_cpu": use_cpu
        }

        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        with open(self.settings_file, 'w') as file:
            json.dump(settings, file)

        QMessageBox.information(self, "Settings", "Settings have been saved successfully.")

    def load_settings(self) -> dict:
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return {}
        return {}


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    dialog = SettingsDialog()
    dialog.exec()
