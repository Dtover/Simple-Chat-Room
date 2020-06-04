from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QPalette, QColor
import Login
import Client

class LoginUI(QDialog, Login.Login):
    def __init__(self):
        super(LoginUI, self).__init__()
        self.UI()
        self.alert
        self.styleComboBox

    def UI(self):
        self.styleComboBox = QComboBox()
        self.styleComboBox.addItems(QStyleFactory.keys()[::-1])
        self.styleComboBox.activated[str].connect(self.changeStyle)

        styleLable = QLabel("&Style:")
        styleLable.setBuddy(self.styleComboBox)

        colorLabel = QLabel("Color:")
        BlackRadioButton = QRadioButton("black")
        BlackRadioButton.clicked.connect(lambda : self.changeColor('black'))
        WhiteRadioButton = QRadioButton("white")
        WhiteRadioButton.setChecked(True)
        WhiteRadioButton.clicked.connect(lambda : self.changeColor('white'))


        toplayout = QHBoxLayout()
        stylelayout = QHBoxLayout()
        stylelayout.addWidget(styleLable)
        stylelayout.addWidget(self.styleComboBox)

        # Set the distance between stylelayout and colorlayout
        stylelayout.setContentsMargins(0, 0, 20, 0)

        colorlayout = QHBoxLayout()
        colorlayout.addWidget(colorLabel)
        colorlayout.addWidget(WhiteRadioButton)
        colorlayout.addWidget(BlackRadioButton)
        toplayout.addLayout(stylelayout)
        toplayout.addLayout(colorlayout)
        toplayout.addStretch(1)

        name = QLabel("Username: ")
        name.setFixedWidth(100)
        name_line = QLineEdit()
        name_line.setFixedWidth(200)
        namelayout = QHBoxLayout()
        namelayout.addWidget(name)
        namelayout.addWidget(name_line)
        passwd = QLabel("Password: ")
        passwd.setFixedWidth(100)
        passwd_line = QLineEdit()
        passwd_line.setFixedWidth(200)
        passwd_line.setEchoMode(QLineEdit.Password)
        passwdlayout = QHBoxLayout()
        passwdlayout.addWidget(passwd)
        passwdlayout.addWidget(passwd_line)
        login_button = QPushButton("Login")
        login_button.setFixedWidth(100)
        login_button.clicked.connect(lambda : self.login_handle(name_line.text(), passwd_line.text()))
        sign_button = QPushButton("Sign up")
        sign_button.setFixedWidth(100)
        sign_button.clicked.connect(lambda : self.signup_handle(name_line.text(), passwd_line.text()))
        buttonlayout = QHBoxLayout()
        buttonlayout.addWidget(login_button)
        buttonlayout.addWidget(sign_button)

        layout = QGridLayout()
        layout.addLayout(toplayout, 0 ,0)
        # layout.addWidget(name, 1, 0)
        # layout.addWidget(name_line, 1, 1)
        layout.addLayout(namelayout, 1, 0)
        # layout.addWidget(passwd, 2, 0)
        # layout.addWidget(passwd_line, 2, 1)
        layout.addLayout(passwdlayout, 2, 0)
        layout.addLayout(buttonlayout, 3, 0)
        # layout.addWidget(sign_button, 3, 0)
        # layout.addWidget(login_button, 3, 1)
        self.setLayout(layout)
        # self.setGeometry(100, 100, 100, 100)


        # palette = QPalette()
        # palette.setColor(QPalette.Window, QColor(53, 53, 53))
        # palette.setColor(QPalette.WindowText, Qt.white)
        # palette.setColor(QPalette.Base, QColor(25, 25, 25))
        # palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        # palette.setColor(QPalette.ToolTipBase, Qt.white)
        # palette.setColor(QPalette.ToolTipText, Qt.white)
        # palette.setColor(QPalette.Text, Qt.white)
        # palette.setColor(QPalette.Button, QColor(53, 53, 53))
        # palette.setColor(QPalette.ButtonText, Qt.white)
        # palette.setColor(QPalette.BrightText, Qt.red)
        # palette.setColor(QPalette.Link, QColor(78, 154, 6))
        # palette.setColor(QPalette.Highlight, QColor(78, 154, 6))
        # palette.setColor(QPalette.HighlightedText, Qt.black)
        self.alert = QMessageBox()
        # QMessageBox.setStyleSheet(self.alert, "QLabel { color: red }")
        # QMessageBox.setStyleSheet(self.alert, "background-color: rgb(53, 53, 53); color: rgb(255, 255, 255)")
        # QMessageBox.setStyleSheet(self.alert, "background-color { color: black}" )
        # QMessageBox.setStyleSheet(self.alert, "Background { color: black }")
        # self.setPalette(palette)

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))

    def changeColor(self, color):
        if color == "black":
            black_style =  "QComboBox QAbstractItemView {"
            black_style += "background: rgb(53, 53, 53) ;"
            black_style += "selection-background-color: rgb(78, 154, 6);"
            black_style += "color: white"
            black_style += "}"
            black_style += "QComboBox {"
            black_style += "selection-background-color: rgb(78, 154, 6);"
            black_style += "background: rgb(53, 53, 53);"
            black_style += "color: white"
            black_style += "}"
            self.styleComboBox.setStyleSheet(black_style)

            black_palette = QPalette()
            black_palette.setColor(QPalette.Window, QColor(53, 53, 53))
            black_palette.setColor(QPalette.WindowText, Qt.white)
            black_palette.setColor(QPalette.Base, QColor(25, 25, 25))
            black_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            black_palette.setColor(QPalette.ToolTipBase, Qt.white)
            black_palette.setColor(QPalette.ToolTipText, Qt.white)
            black_palette.setColor(QPalette.Text, Qt.white)
            black_palette.setColor(QPalette.Button, QColor(53, 53, 53))
            black_palette.setColor(QPalette.ButtonText, Qt.white)
            black_palette.setColor(QPalette.BrightText, Qt.red)
            black_palette.setColor(QPalette.Link, QColor(78, 154, 6))
            black_palette.setColor(QPalette.Highlight, QColor(78, 154, 6))
            black_palette.setColor(QPalette.HighlightedText, Qt.black)
            self.setPalette(black_palette)
            QMessageBox.setStyleSheet(self.alert, "background-color: rgb(53, 53, 53); color: rgb(255, 255, 255)")

        else:
            white_style =  "QComboBox QAbstractItemView {"
            white_style += "background: white;"
            white_style += "selection-background-color: rgb(48,140,198);"
            white_style += "color: black"
            white_style += "}"
            white_style += "QComboBox {"
            white_style += "selection-background-color: rgb(48,140,198);"
            white_style += "background: white;"
            white_style += "color: black"
            white_style += "}"
            self.styleComboBox.setStyleSheet(white_style)
            white_palette = QPalette()
            self.setPalette(white_palette)

    def login_handle(self, username, passwd):
        result = self.login(username, passwd)
        if result == "Miss":
            self.alert.setText('Input missing !')
            # self.setStyleSheet("background-color rgb(0, 0, 0)")
            self.alert.exec_()
        elif result == "None":
            self.alert.setText('No user found !')
            self.alert.exec_()
        elif result == "Success":
            self.hide()
            self.client = Client.Client(username)
            self.client.show()
        elif result == "WrongPwd":
            self.alert.setText('Wrong password !')
            self.alert.exec_()

    def signup_handle(self, username, passwd):
        result = self.sign_up(username, passwd)
        if result == "Miss":
            self.alert.setText('Input missing !')
            # self.setStyleSheet("background-color rgb(0, 0, 0)")
            self.alert.exec_()
        elif result == "Success":
            self.alert.setText('Sign up successfully !')
            # self.setStyleSheet("background-color rgb(0, 0, 0)")
            self.alert.exec_()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    try:
        login = LoginUI()
        login.show()
    except Exception as e:
        print(e)
        # print("Run mysql !")
    sys.exit(app.exec_())

