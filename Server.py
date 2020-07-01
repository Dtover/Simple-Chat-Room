from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QPalette, QColor
from socket import *
from threading import *
import time

ServerisRunning = False
client_sockets = []
# server_socket = socket(AF_INET, SOCK_STREAM)

class Server(QDialog):
    def __init__(self, parent=None):
        super(Server, self).__init__(parent)
        self.UI()
        self.ClientInfoText
        self.styleComboBox

    # Main Window UI design
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
        self.createClientInfoPart()

        mainLayout = QGridLayout()
        mainLayout.addLayout(toplayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.IpPortPart, 1, 0)
        mainLayout.addWidget(self.ClientInfo, 2, 0)
        self.setLayout(mainLayout)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        self.setGeometry(200, 200, 500, 500)

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))


    def changeColor(self, color):
        if color == "black":
            # Somehow, the style of QComboBox has to be set up separately
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
            # Use default color style
            white_palette = QPalette()
            self.setPalette(white_palette)

    def createIpPortPart(self):
        self.IpPortPart = QGroupBox("Start a server")

        global Ip_Line
        global Port_Line
        global start_button
        global stop_button
        Ip_Label = QLabel("Server Address: ")
        Ip_Line = QLineEdit()
        Ip_Line.setFixedWidth(200)
        Ip_Line.setText("127.0.0.1")
        Port_Label = QLabel("Port Number: ")
        # Port_Line = QLineEdit()
        Port_Line = QSpinBox()
        Port_Line.setFixedWidth(100)
        Port_Line.setMinimum(0)
        Port_Line.setMaximum(65535)
        Port_Line.setValue(8888)
        start_button = QPushButton("Start")
        stop_button = QPushButton("Close")
        start_button.setFixedWidth(100)
        stop_button.setFixedWidth(100)
        start_button.clicked.connect(self.startServer)
        stop_button.clicked.connect(self.stopServer)

        layout = QGridLayout()
        layout.addWidget(Ip_Label, 1, 0)
        layout.addWidget(Ip_Line, 1, 1)
        layout.addWidget(Port_Label, 2, 0)
        layout.addWidget(Port_Line, 2, 1)
        layout.addWidget(stop_button, 3, 0)
        layout.addWidget(start_button, 3, 1)
        layout.setColumnStretch(1, 1)
        self.IpPortPart.setLayout(layout)

    def createClientInfoPart(self):

        self.ClientInfo = QGroupBox("Client Information")
        self.ClientInfoText = QPlainTextEdit()
        self.ClientInfoText.setFixedHeight(200)
        layout = QGridLayout()
        layout.addWidget(self.ClientInfoText)
        self.ClientInfo.setLayout(layout)

    # Main functions
    def startServer(self):
        global ServerisRunning
        if ServerisRunning == False:
            self.serverthread = StartThread(self)
            self.serverthread.ChatInfoUpdate.connect(self.updateText)
            self.serverthread.start()
        else:
            self.ClientInfoText.appendPlainText("Server is already running!")

    def updateText(self, text):
        self.ClientInfoText.appendPlainText(text)

    def stopServer(self):
        global ServerisRunning
        # global server_socket
        if ServerisRunning:
            # server_socket.close()
            ServerisRunning = False
            self.ClientInfoText.appendPlainText("Server stopped!")
        else:
            self.ClientInfoText.appendPlainText("No server running!")
        self.close()

class StartThread(QtCore.QThread):
    ChatInfoUpdate = QtCore.pyqtSignal(str)
    # global server_socket
    def run(self):
        global ServerisRunning
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((Ip_Line.text(), Port_Line.value()))
        server_socket.listen()
        ServerisRunning = True
        self.ChatInfoUpdate.emit("Server is running on " + Ip_Line.text() + " : " + str(Port_Line.value()))
        while ServerisRunning:
            client_socket, client_info = server_socket.accept()
            client_sockets.append(client_socket)
            getmsgthread = Thread(target = self.fetchMsg, args = (client_socket, ))
            getmsgthread.start()
            self.ChatInfoUpdate.emit("client " + str(client_info[1]) + " connects to this server!")

    # This function will get message and send them to all the clients in the client list
    def fetchMsg(self, client_socket):
        global ServerisRunning
        # global client_sockets
        while ServerisRunning:
            recv_data = client_socket.recv(1024)
            if len(recv_data) > 0:
                self.ChatInfoUpdate.emit(recv_data.decode('utf-8'))
            for client_socket in client_sockets:
                client_socket.send(recv_data)

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    server = Server()
    server.show()
    sys.exit(app.exec_())
