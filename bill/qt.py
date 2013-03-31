import sys
import os

from PySide import QtGui, QtCore

from main import search_duplicates, check_uniques



class Button(QtGui.QPushButton):
    """docstring for Button"""
    
    def __init__(self, name, parent, x, y):
        super(Button, self).__init__(name, parent)

        self.resize(self.sizeHint())
        self.move(x, y)
        self.label = QtGui.QLabel(parent)
        self.label.setGeometry(x + 130, y, 100, 25)
        self.label.set_text = self.label.setText
        self.label.set_text("...")
        
    def get_filename(self):
        """docstring for get_filename"""
        filepath = QtGui.QFileDialog.getOpenFileName()
        self.filepath = filepath[0]
        filename = os.path.basename(self.filepath) 
        self.filename = filename
        self.label.set_text(filename)

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()

    def calculate(self):
        """docstring for calculate"""
        uniques, duplicates = search_duplicates(self.btn2.filepath)
        check_uniques(self.btn1.filepath, uniques, duplicates)

        
    def initUI(self):
        
        
        self.btn1 = Button('Vhodni excel', self, 20, 20)
        self.btn1.clicked.connect(self.btn1.get_filename)

        # self.btn1 = self.make_button('Vhodni podatki', 20, 60)
        self.btn2 = Button('Vhodni podatki', self, 20, 60)
        self.btn2.clicked.connect(self.btn2.get_filename)
        
        # self.btn1 = self.make_button('Izhodni excel', 20, 100)
        self.btn3 = Button('Izhodni excel', self, 20, 100)
        self.btn3.clicked.connect(self.btn3.get_filename)
        
        #  self.btn1 = self.make_button('Izracunaj', 20, 140)
        self.btn4 = Button('Izcracunaj', self, 20, 140)
        self.btn4.clicked.connect(self.calculate)


        self.btn5 = QtGui.QPushButton('Zapri', self)
        self.btn5.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.btn5.resize(self.btn5.sizeHint())
        self.btn5.move(20, 200)       

        self.setGeometry(300, 300, 250, 250)
        self.setWindowTitle('Revija 112')    
        self.show()
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
