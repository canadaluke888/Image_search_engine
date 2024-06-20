import json
import os
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton, QMessageBox, QApplication

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

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_num_results)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def get_num_results_data(self) -> int:
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as file:
                try:
                    settings_file = json.load(file)
                    num_results = settings_file.get('num_results', 3)  # Default to 3 if not found
                except json.JSONDecodeError:
                    num_results = 3
        else:
            num_results = 3
        return num_results

    def save_num_results(self):
        num: int = self.num_results_input.value()
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        with open(self.settings_file, 'w') as file:
            num_results_dict = {"num_results": num}
            json.dump(num_results_dict, file)
        QMessageBox.information(self, "Settings", "Settings have been saved successfully.")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    dialog = SettingsDialog()
    dialog.exec()
