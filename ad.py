import sys
import random
import sqlite3
import PyQt5.QtWidgets

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QPlainTextEdit
from PyQt5.QtWidgets import QMainWindow, QLabel, QLCDNumber, QLineEdit
from PyQt5.QtWidgets import QComboBox

a = ['ad', 'Bayern', "Borussia Dortmund", "Barcelona", "Real Madrid",
     "Atletico Madrid", "Juventus", "Manchester City", "Manchester United",
     "Chelsea", "Arsenal", "Liverpool"]


class FirstForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 900, 700)
        self.setWindowTitle('Football')
        self.setStyleSheet("background-color : orange")

        self.tim = QtCore.QTimer()
        self.tim.timeout.connect(self.til)

        self.lcd = QLCDNumber(self)
        self.cnt = 0
        self.lcd.display(0)
        self.lcd.move(550, 80)
        self.oj = QLabel(self)
        self.oj.move(480, 80)
        self.oj.setText("Количество очков")

        self.x = QComboBox(self)
        self.x.setStyleSheet("background-color : white")
        self.x.clear()
        self.x.resize(150, 30)
        for i in range(1, len(a)):
            self.x.addItem(a[i])

        self.b = QPushButton(self)
        self.b.move(151, 0)
        self.b.clicked.connect(self.runinf)
        self.b.setText('Выбрать')
        self.b.setStyleSheet("background-color : violet")
        self.ded = 0

        self.l = QLabel(self)
        self.l.move(0, 70)
        self.l.resize(300, 400)
        self.l.setStyleSheet("QLabel { background-color : ; color : blue; }")

        self.st = QPushButton(self)
        self.st.setText('Начать игру')
        self.st.move(550, 0)
        self.st.setStyleSheet("background-color : red")
        self.st.resize(100, 50)
        self.st.clicked.connect(self.ready)

        self.qu = QLabel(self)
        self.qu.setText('Угадай в каком клубе футболист, что бы начать нажми Начать игру')
        self.qu.move(400, 50)
        self.qu.resize(350, 30)
        self.qu.setStyleSheet("QLabel { background-color : ; color : green; }")

        self.ba = QPushButton(self)
        self.ba.move(550, 200)
        self.ba.resize(100, 40)
        self.ba.setStyleSheet("background-color : green; color : black;")
        self.ba.clicked.connect(self.ruin)
        self.bb = QPushButton(self)
        self.bb.move(550, 250)
        self.bb.setStyleSheet("background-color : pink; color : black;")
        self.bb.resize(100, 40)
        self.bb.clicked.connect(self.ruin)
        self.bc = QPushButton(self)
        self.bc.move(550, 300)
        self.bc.setStyleSheet("background-color : white; color : black;")
        self.bc.resize(100, 40)
        self.bc.clicked.connect(self.ruin)
        self.bd = QPushButton(self)
        self.bd.move(550, 350)
        self.bd.setStyleSheet("background-color : purple; color : black;")
        self.bd.resize(100, 40)
        self.bd.clicked.connect(self.ruin)

        self.pl = QLabel(self)
        self.pl.move(500, 150)
        self.pl.setText('                           Вопрос:')
        self.pl.resize(220, 30)
        self.pl.setStyleSheet("QLabel { background-color : ; color : blue; }")

        self.pa = QLabel(self)
        self.pa.move(500, 450)
        self.pa.resize(220, 30)
        self.pa.setStyleSheet("QLabel { backfround-color : white; color : green; }")

        self.ot = ''
        self.bur = list()
        self.ok = 0
        self.stop = 0

    def til(self):
        if self.stop < 10:
            self.ready()

    def ruin(self):
        if self.ok == 0:
            return
        if self.sender() is self.ba:
            if self.ot == self.bur[0]:
                self.pa.setText('ДА ПРАВИЛЬНО ВЫ МОЛОДЕЦ')
                self.ded = 0
                self.ok = 0
                self.cnt += 1
                self.lcd.display(self.cnt)
                if self.stop < 10:
                    self.ready()
            else:
                self.pa.setText('Это не верный ответ, попробуйте снова')
        elif self.sender() is self.bb:
            if self.ot == self.bur[1]:
                self.pa.setText('ДА ПРАВИЛЬНО ВЫ МОЛОДЕЦ')
                self.ded = 0
                self.ok = 0
                self.cnt += 1
                self.lcd.display(self.cnt)
                if self.stop < 10:
                    self.ready()
            else:
                self.pa.setText('Это не верный ответ, попробуйте снова')
        elif self.sender() is self.bc:
            if self.ot == self.bur[2]:
                self.pa.setText('ДА ПРАВИЛЬНО ВЫ МОЛОДЕЦ')
                self.ded = 0
                self.ok = 0
                self.cnt += 1
                self.lcd.display(self.cnt)
                if self.stop < 10:
                    self.ready()
            else:
                self.pa.setText('Это не верный ответ, попробуйте снова')
        elif self.sender() is self.bd:
            if self.ot == self.bur[3]:
                if self.stop < 10:
                    self.pa.setText('ДА ПРАВИЛЬНО ВЫ МОЛОДЕЦ')
                self.ded = 0
                self.ok = 0
                self.cnt += 1
                self.lcd.display(self.cnt)
                if self.stop < 10:
                    self.ready()
            else:
                self.pa.setText('Это не верный ответ, попробуйте снова')

    def ready(self):
        if self.sender() is self.st:
            self.stop = 0
            self.cnt = 0
            self.lcd.display(self.cnt)
        self.stop += 1
        self.ded = 1
        self.ok = 1
        self.tim.start(10000)
        self.pa.clear()
        self.l.clear()
        con = sqlite3.connect('clubs.db')
        cur = con.cursor()
        res = cur.execute("""SELECT * FROM Players""").fetchall()
        x = random.choice(res)
        self.pl.setText(x[1] + ' ' + str(x[4]) + 'лет позиция ' + x[2])
        self.bur.clear()
        self.ot = a[x[3]]
        self.bur.append(a[x[3]])
        cnt = 1
        while cnt != 4:
            sf = random.choice(a)
            ok = 0
            for i in self.bur:
                if sf == i or sf == 'ad':
                    ok = 1
            if ok == 0:
                self.bur.append(sf)
                cnt += 1
        random.shuffle(self.bur)
        self.ba.setText(self.bur[0])
        self.bb.setText(self.bur[1])
        self.bc.setText(self.bur[2])
        self.bd.setText(self.bur[3])

    def runinf(self):
        if self.ded != 1:
            self.l.clear()
            k = self.x.currentText()
            ig = a.index(k)
            con = sqlite3.connect('clubs.db')
            cur = con.cursor()
            res = cur.execute("SELECT * FROM Players WHERE Club_id ".format(ig)).fetchall()
            for i in res:
                if i[3] == ig:
                    ab = self.l.text()
                    s = i[1] + ' ' + str(i[4]) + " Years old"
                    self.l.setText(ab + s + '\n')
        else:
            self.l.setText('Нельзя читерить')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstForm()
    ex.show()
    sys.exit(app.exec())
