# 창 띄우기
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, qApp
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('BSDP') # 창 타이틀
        self.move(400, 120) # 창 위치
        self.resize(1200, 800) # 창 사이즈

        #가입하기 버튼
        btnSign = QPushButton('가입하기', self)
        btnSign.move(1030, 720) # 버튼 위치
        btnSign.resize(btnSign.sizeHint())
        btnSign.clicked.connect(QCoreApplication.instance().quit) # quit 내용 바꿔야함

        #로그인하기 버튼
        btnLogin = QPushButton('로그인하기', self)
        btnLogin.move(900, 720)  # 버튼 위치
        btnLogin.resize(btnLogin.sizeHint())
        btnLogin.clicked.connect(QCoreApplication.instance().quit)  # quit 내용 바꿔야함
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())