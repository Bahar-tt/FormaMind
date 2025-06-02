import sys
from PyQt5.QtWidgets import QApplication
from formamind.workout_gui import WorkoutApp

def main():
    app = QApplication(sys.argv)
    window = WorkoutApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 