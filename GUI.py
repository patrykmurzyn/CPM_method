import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from datetime import datetime
from PyQt5.QtGui import *
from CpmCalculationService import CpmCalculationService


# Main Window
class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Logistyka - metoda CPM'
        self.left = 200
        self.top = 200
        self.width = 1200
        self.height = 600

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.layout = QVBoxLayout()
        self.tableWidget = QTableWidget()

        self.cpm_calculation = CpmCalculationService()

    def frame1(self, a, b, c):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        wyniki = self.cpm_calculation.calculate(a, b, c)
        label1 = QLabel("Wyniki: ")
        text_edit1 = QTextEdit()
        wyniki_str = "Wyniki obliczeń: \n"
        for val in wyniki:
            wyniki_str = wyniki_str + str(val) + '\n'
        text_edit1.setText(wyniki_str)

        again_button = QPushButton("Ja chce jeszcze raz !!!")
        again_button.setFixedHeight(40)
        again_button.setStyleSheet(
            "*{background:#404040;" +
            "border-radius: 3%;" +
            "color:white;}" +
            "*:hover{background:'#646464';} "

        )
        again_button.clicked.connect(self.frame0)
        self.layout.addWidget(label1)
        self.layout.addWidget(text_edit1)
        self.layout.addWidget(again_button)
        self.setLayout(self.layout)

    def frame0(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        exL1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        exL2 = ['7', '9', '3', '8', '5', '4', '2', '1']
        exL3 = ['', 'A', 'A', 'B', 'C', 'C', 'DEF', 'G']
        self.createTable(exL1, exL2, exL3)

        # set path of selected file
        def select_file():
            try:
                global filepath
                filepath = QFileDialog.getOpenFileName(None, 'Wybierz pliki do wgrania')
                filepath = str(filepath)
                print(str(datetime.now()) + " [INFO] " + "Wybrano plik: " + filepath)
                y = filepath.replace("('C:", '')
                filepath = y.replace("', 'All Files (*)')", '')
                label_select.setText(filepath)
                activities, durations, predecessors = self.csvToTable(filepath)
                self.createTable(activities, durations, predecessors)
            except:
                label_select.setText("ERROR: There is something wrong with this file")

        save_button = QPushButton("Oblicz")
        save_button.setFixedHeight(40)
        save_button.setStyleSheet(
            "*{background:#404040;" +
            "border-radius: 3%;" +
            "color:white;}" +
            "*:hover{background:'#646464';} "
        )

        activities = []
        durations = []
        predecessors = []

        for i in range(8):
            activities.append(self.tableWidget.item(i, 0).text())
            durations.append(int(self.tableWidget.item(i, 1).text()))
            predecessors.append(self.tableWidget.item(i, 2).text())

        save_button.clicked.connect(lambda: self.frame1(activities, durations, predecessors))

        label_top = QLabel(
            "\U0001F680" + " Zaawansowany program Logistyczny - metoda CPM \n Proszę wpisać dane do tabeli lub wgrać plik w celu dokonania obliczeń ")
        label_top.setFixedHeight(60)
        label_top.setStyleSheet("background: #202020;" + "color: 'white';" + "padding: 0;")
        label_top.setAlignment(QtCore.Qt.AlignCenter)

        label_bottom = QLabel("Created by: Szymon Michoń, Patryk Murzyn, Maciej Lisowski, Mateusz Ostrowski")
        label_bottom.setFixedHeight(30)
        label_bottom.setStyleSheet("background: #202020;" + "color: 'white';" + "padding: 0;")
        label_bottom.setAlignment(QtCore.Qt.AlignCenter)

        button_select = QPushButton("Select file")
        button_select.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        label_select = QLabel("Brak wybranego pliku")

        button_select.clicked.connect(select_file)

        self.layout.addWidget(label_top)
        self.layout.addWidget(self.tableWidget)
        self.layout.addWidget(button_select)
        self.layout.addWidget(label_select)

        self.layout.addWidget(save_button)
        self.layout.addWidget(label_bottom)

        self.setLayout(self.layout)

        self.show()

    def csvToTable(self, fileName):
        text = open(fileName, 'r')
        text = text.read()
        result = []
        for line in text.splitlines():
            result.append(tuple(line.split(",")))

        activities = []
        durations = []
        predecessors = []
        for i in result:
            activities.append(i[0])
            durations.append(i[1])
            predecessors.append(i[2])

        return activities, durations, predecessors

    # Create table
    def createTable(self, activities, durations, predecessors):
        self.tableWidget.setRowCount(8)
        self.tableWidget.setColumnCount(3)

        columnsName = ["activities", "durations", "predecessors"]
        self.tableWidget.setHorizontalHeaderLabels(columnsName)

        for id, x in enumerate(activities):
            self.tableWidget.setItem(id, 0, QTableWidgetItem(x))
        for id, x in enumerate(durations):
            self.tableWidget.setItem(id, 1, QTableWidgetItem(x))
        for id, x in enumerate(predecessors):
            self.tableWidget.setItem(id, 2, QTableWidgetItem(x))

        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.tableWidget.viewport().update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.frame0()
    sys.exit(app.exec_())
