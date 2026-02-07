import sys
import threading
import requests

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile


class App(QWidget):
    def __init__(self):
        super().__init__()

        # Load UI
        loader = QUiLoader()
        ui_file = QFile("main.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.ui.setWindowTitle("sp4m_L1nks")
        self.ui.setFixedSize(self.ui.size())

        # Button event
        self.ui.start_btn.clicked.connect(self.start)

    def log(self, text):
        self.ui.log_box.append(text)

    def start(self):
        link = self.ui.link_input.text().strip()
        count = self.ui.count_spin.value()

        if not link:
            self.log("❌ Please enter a valid link.")
            return

        self.ui.start_btn.setEnabled(False)
        self.log("▶️ Starting requests...")

        thread = threading.Thread(
            target=self.spam,
            args=(link, count),
            daemon=True
        )
        thread.start()

    def spam(self, link, count):
        success = 0

        for i in range(count):
            try:
                response = requests.get(link, timeout=5)

                if response.status_code == 200:
                    success += 1
                    self.log(f"✔ [{i+1}/{count}] Request successful")
                else:
                    self.log(f"⚠ [{i+1}/{count}] Status code: {response.status_code}")

            except Exception:
                self.log(f"❌ [{i+1}/{count}] Request failed")

        self.log(f"✅ Finished | Successful requests: {success}/{count}")
        self.ui.start_btn.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
