from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QPalette, QColor
from PyQt5 import QtCore
from socket import *
from threading import *
from multiprocessing import Queue
import time
import sys, errno

isconnectserver = False
messagelist = Queue()

class Client(QDialog):
    def __init__(self, username):
        super(Client, self).__init__()
        self.UI()
        self.username = username
        self.ChatInfo
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

        # Create Child Widgets
        self.createIpPortPart()
        self.CreateChatPart()

        mainLayout = QGridLayout()
        mainLayout.addLayout(toplayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.IpPortPart, 1, 0)
        mainLayout.addWidget(self.ChatPart, 2, 0)
        self.setLayout(mainLayout)
        mainLayout.setRowStretch(1, 0)
        mainLayout.setRowStretch(2, 1)
        self.setGeometry(200, 200, 500, 500)

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

    def createIpPortPart(self):
        self.IpPortPart = QGroupBox("Connect to server")

        global Ip_Line
        global Port_Line
        global connect_button
        global disconnect_button
        Ip_Label = QLabel("Server Address: ")
        Ip_Line = QLineEdit()
        Ip_Line.setFixedWidth(200)
        Ip_Line.setText("127.0.0.1")
        Port_Label = QLabel("Port Number: ")
        Port_Line = QSpinBox()
        Port_Line.setFixedWidth(100)
        Port_Line.setMinimum(0)
        Port_Line.setMaximum(65535)
        Port_Line.setValue(8888)
        connect_button = QPushButton("Connect")
        disconnect_button = QPushButton("Disconnect")
        connect_button.setFixedWidth(100)
        disconnect_button.setFixedWidth(100)
        connect_button.clicked.connect(self.ConnecttoServer)
        connect_button.setAutoDefault(False)
        disconnect_button.clicked.connect(self.disconnect)
        disconnect_button.setAutoDefault(False)

        layout = QGridLayout()
        layout.addWidget(Ip_Label, 1, 0)
        layout.addWidget(Ip_Line, 1, 1)
        layout.addWidget(Port_Label, 2, 0)
        layout.addWidget(Port_Line, 2, 1)
        layout.addWidget(disconnect_button, 3, 0)
        layout.addWidget(connect_button, 3, 1)
        layout.setColumnStretch(1, 1)
        self.IpPortPart.setLayout(layout)

    def CreateChatPart(self):
        self.ChatPart = QGroupBox("Chat box")
        global Msg_Line
        global Send_Button
        self.ChatInfo = QPlainTextEdit()
        Msg_Line = QLineEdit()
        Send_Button = QPushButton("Send")
        Send_Button.clicked.connect(self.putMsg)
        Send_Button.setAutoDefault(False)
        Msg_Line.returnPressed.connect(Send_Button.click)
        send_layout = QGridLayout()
        send_layout.addWidget(Msg_Line, 0, 0)
        send_layout.addWidget(Send_Button, 0, 1)
        layout = QGridLayout()
        layout.addWidget(self.ChatInfo, 0, 0)
        layout.addLayout(send_layout, 1, 0)
        self.ChatPart.setLayout(layout)

    def ConnecttoServer(self):
        global isconnectserver
        try:
            if isconnectserver == False:
                self.contoserver = ConnectThread(self)
                self.contoserver.Message.connect(self.updateText)
                self.contoserver.start()
            else:
                self.ChatInfo.appendPlainText("Already connect to the server !")
        except Exception as e:
            self.ChatInfo.appendPlainText("Something wrong !")
            self.ChatInfo.appendPlainText(e)

    def updateText(self, text):
        self.ChatInfo.appendPlainText(text)

    def disconnect(self):
        global isconnectserver
        if isconnectserver:
            messagelist.put(None)
            self.contoserver.disconnect()
            isconnectserver = False
            self.ChatInfo.appendPlainText("Disconnect !")
        else:
            self.ChatInfo.appendPlainText("Not connected yet !")

    def putMsg(self):
        global isconnectserver
        if isconnectserver:
            try:
                msg = Msg_Line.text()
                msg = time.strftime("%m-%d %H:%M:%S ", time.localtime()) + self.username + " : " + msg
                messagelist.put(msg)
                Msg_Line.setText("")
            except IOError as e:
                if e.errno == errno.EPIPE:
                    print(e)
        else:
            self.ChatInfo.appendPlainText("Connect to server first !")

class ConnectThread(QtCore.QThread):
    Message = QtCore.pyqtSignal(str)
    # global client_socket
    global isconnectserver
    def __init__(self, parent=None):
        super(ConnectThread, self).__init__(parent)
        self.client_socket = None
    def run(self):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((Ip_Line.text(), Port_Line.value()))
        global isconnectserver
        isconnectserver = True
        self.Message.emit("Connect to server successfully! ")
        recvthread = Thread(target = self.recvMsg)
        recvthread.start()
        sendthread = Thread(target = self.sendMsg)
        sendthread.daemon = True
        sendthread.start()

    def recvMsg(self):
        while isconnectserver:
            recv_data = self.client_socket.recv(1024)
            self.Message.emit(recv_data.decode('utf-8'))

    def sendMsg(self):
        while isconnectserver:
            msg = messagelist.get()
            if msg != None and len(msg) > 0:
                self.client_socket.send(msg.encode('utf-8'))

    def disconnect(self):
        if isconnectserver:
            self.client_socket.close()

# if __name__ == "__main__":
    # import sys
    # app = QApplication(sys.argv)
    # client = Client("TestUser")
    # client.show()
    # sys.exit(app.exec_()) 
