import sys
from PyQt5.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
window = QLabel('PyQt5 Test - اگر این متن را می‌بینید PyQt5 درست کار می‌کند!')
window.resize(400, 100)
window.show()
app.exec_() 