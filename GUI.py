import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore                
from datetime import date, datetime
from PyQt5.QtGui import *

#do obliczeń
import networkx as nx
import matplotlib.pyplot as plt

#Main Window
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

    def frame1(self,a,b,c):
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)
        
        wyniki = licz(a,b,c)
        label1 = QLabel("Wyniki: ")
        textEdit1 = QTextEdit()
        wynikiStr = "Wyniki obliczeń: \n"
        for val in wyniki:
            wynikiStr = wynikiStr+str(val)+'\n'
        textEdit1.setText(wynikiStr)

        againButton = QPushButton("Ja chce jeszcze raz !!!")
        againButton.setFixedHeight(40)
        againButton.setStyleSheet(
                "*{background:#404040;"+
                "border-radius: 3%;" +
                "color:white;}"+
                "*:hover{background:'#646464';} "
                
        ) 
        againButton.clicked.connect(self.frame0)
        self.layout.addWidget(label1)
        self.layout.addWidget(textEdit1)
        self.layout.addWidget(againButton)
        self.setLayout(self.layout)

    def frame0(self):
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)
        exL1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        exL2 = ['7', '9', '3', '8', '5', '4', '2', '1']
        exL3 = ['', 'A', 'A', 'B', 'C', 'C', 'DEF', 'G']
        self.createTable(exL1,exL2,exL3)

       #set path of selected file
        def selectFile(): 
            try:
                global filepath
                filepath = QFileDialog.getOpenFileName(None, 'Wybierz pliki do wgrania')
                filepath = str(filepath)
                print(str(datetime.now())+" [INFO] "+ "Wybrano plik: "+filepath)
                y = filepath.replace("('C:",'')
                filepath = y.replace("', 'All Files (*)')",'')
                labelSelect.setText(filepath)
                activities,durations,predecessors = self.csvToTable(filepath)
                self.createTable(activities,durations,predecessors)
            except:
                labelSelect.setText("ERROR: There is something wrong with this file")

        saveButton = QPushButton("Oblicz")
        saveButton.setFixedHeight(40)
        saveButton.setStyleSheet(
                "*{background:#404040;"+
                "border-radius: 3%;" +
                "color:white;}"+
                "*:hover{background:'#646464';} "
         ) 

        activities = []
        durations = []
        predecessors = []
  
        for i in range(8):
            activities.append(self.tableWidget.item(i,0).text())
            durations.append(int(self.tableWidget.item(i,1).text()))
            predecessors.append(self.tableWidget.item(i,2).text())
    

        saveButton.clicked.connect(lambda: self.frame1(activities,durations,predecessors))
        
        labelTop = QLabel("\U0001F680" +" Zaawansowany program Logistyczny - metoda CPM \n Proszę wpisać dane do tabeli lub wgrać plik w celu dokonania obliczeń ")
        labelTop.setFixedHeight(60)
        labelTop.setStyleSheet("background: #202020;" + "color: 'white';" + "padding: 0;")
        labelTop.setAlignment(QtCore.Qt.AlignCenter)

        labelBottom = QLabel("Created by: Szymon Michoń, Patryk Murzyn, Maciej Lisowski, Mateusz Ostrowski")
        labelBottom.setFixedHeight(30)
        labelBottom.setStyleSheet("background: #202020;" + "color: 'white';" + "padding: 0;")
        labelBottom.setAlignment(QtCore.Qt.AlignCenter)
        
        buttonSelect = QPushButton("Select file")
        buttonSelect.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        labelSelect = QLabel("Brak wybranego pliku")

        buttonSelect.clicked.connect(selectFile)

        self.layout.addWidget(labelTop)
        self.layout.addWidget(self.tableWidget)
        self.layout.addWidget(buttonSelect)
        self.layout.addWidget(labelSelect)

        self.layout.addWidget(saveButton)
        self.layout.addWidget(labelBottom)

        self.setLayout(self.layout)

        
        self.show()
       
        
    def csvToTable(self,fileName):
        text = open(fileName,'r')
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

        return activities,durations,predecessors

    #Create table
    def createTable(self,activities,durations,predecessors):
        self.tableWidget.setRowCount(8)
        self.tableWidget.setColumnCount(3)

        columnsName = ["activities", "durations", "predecessors"]
        self.tableWidget.setHorizontalHeaderLabels(columnsName)

        for id,x in enumerate(activities):
            self.tableWidget.setItem(id,0,QTableWidgetItem(x))
        for id,x in enumerate(durations):
            self.tableWidget.setItem(id,1,QTableWidgetItem(x))
        for id,x in enumerate(predecessors):
            self.tableWidget.setItem(id,2,QTableWidgetItem(x))

        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.tableWidget.viewport().update()
        
    
successors = [] #['BC', 'D', 'EF', 'G', 'G', 'G', 'H', '']
def licz(activities,durations,predecessors):
    wyniki = []
    ES = [] #Early Start
    EF = [] #Early Finish
    LS = [] #Late Start
    LF = [] #Late Finish
    SK = [] #Slack Value

    G = nx.DiGraph()   

    for i in range(len(activities)):
        successors.append('')

    wyniki.append("Edges:")
    for i in range(len(activities)):

        if(i == 0):
            ES.append(0)
            EF.append(durations[0])
        
        else:
            max = 0

            for j in range(len(predecessors[i])):
                G.add_edge(predecessors[i][j], activities[i])
                wyniki.append(predecessors[i][j] + "->" + activities[i])
                successors[activities.index(predecessors[i][j])] += activities[i];

                if(EF[activities.index(predecessors[i][j])] > max):
                    max = EF[activities.index(predecessors[i][j])]
            
            ES.append(max)
            EF.append(max + durations[i])

    wyniki.append("Successors:")
    for i in successors:
        wyniki.append(i)     
    
    wyniki.append("-----------ES-----------")
    for i in ES:
        wyniki.append(i)

    wyniki.append("-----------EF-----------")
    for i in EF:
        wyniki.append(i)

        
    size = len(activities) 

    wyniki.append("Start")
    for i in range(len(activities)):
        if(i == 0):
            LF.append(EF[size - 1])
            LS.append(LF[0] - durations[size - 1])
            
        else:
            min = 1000000000000

            for j in range(len(successors[size - i - 1])):

                if(LS[size - 1 - activities.index(successors[size - i - 1][j])] < min):
                    wyniki.append("IN")
                    min = LS[size - 1 - activities.index(successors[size - i - 1][j])]

            LF.append(min)
            LS.append(min - durations[size - i - 1])


    LS.reverse()
    LF.reverse()

    wyniki.append("-----------LS-----------")
    for i in LS:
        wyniki.append(i)

    wyniki.append("-----------LF-----------")
    for i in LF:
        wyniki.append(i)

    for i in range(len(activities)):
        SK.append(LS[i] - ES[i])


    wyniki.append("-----------SK-----------")
    for i in SK:
        wyniki.append(i)        

    pos = nx.spring_layout(G, seed=12)
    for k,v in pos.items():
        pos[k]=(-v[1],v[0])

    nx.draw_networkx_nodes(G,pos = pos, node_shape = 'o', node_size = 300, 
                        node_color = 'none', edgecolors='k')
    nx.draw_networkx_edges(G,pos = pos, 
                        node_shape = 's', width = 1,  node_size = 200)
    nx.draw_networkx_labels(G,pos = pos, font_size = 11)

    plt.savefig("test")
    return wyniki

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.frame0()
    sys.exit(app.exec_())
