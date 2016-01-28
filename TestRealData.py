#-*-coding: utf-8 -*-
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QAxContainer import *

## reference: https://wikidocs.net/3124
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 300, 400)

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.connect(self.kiwoom, SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"), self.OnReceiveTrData)
        self.kiwoom.connect(self.kiwoom, SIGNAL("OnReceiveRealData(QString, QString, QString)"), self.OnReceiveRealData)

        btn1 = QPushButton("Log In", self)
        btn1.move(20, 20)
        self.connect(btn1, SIGNAL("clicked()"), self.btn_clicked)

        btn1 = QPushButton("Log Out", self)
        btn1.move(120, 20)
        self.connect(btn1, SIGNAL("clicked()"), self.btn_term_clicked)

        btn2 = QPushButton("Get Info", self)
        btn2.move(20, 70)
        self.connect(btn2, SIGNAL("clicked()"), self.btn_clicked2)

        btn3 = QPushButton("접속 상태 확인", self)
        btn3.move(20, 120)
        self.connect(btn3, SIGNAL("clicked()"), self.btn_clicked3)

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 170)
        self.textbox.resize(270,40)

        self.list = QListWidget(self)
        self.list.move(20, 220)
        self.list.resize(270,140)

    def OnReceiveTrData(self, sScrNo, sRQName, sTRCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSPlmMsg):
        if sRQName == "주식기본정보":
            cnt = self.kiwoom.dynamicCall('GetRepeatCnt(QString, QString)', sTRCode, sRQName)
            name = self.kiwoom.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sTRCode, "", sRQName, 0, "종목명")
            cur_price = self.kiwoom.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sTRCode, "", sRQName, 0, "현재가")
            
            self.textbox.setText(name.strip() + " : " + cur_price.strip())
            print(name.strip())
            print(cur_price.strip())

        elif sRQName == "코스피200지수요청":
            cnt = self.kiwoom.dynamicCall('GetRepeatCnt(QString, QString)', sTRCode, sRQName)
            print("cnt: ", cnt)
            for i in range(cnt):
                list = self.kiwoom.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sTRCode, "", sRQName, 0, "코스피200")
                print("nDataLength: ", len(list))

    def write(self, data):
            item = QListWidgetItem(data)
            self.list.addItem(item)

            with open("realData.txt", 'a') as f:
                f.write(data)


            ## 8. 실시간 FID
    def OnReceiveRealData(self, sJongmokCode, sRealType, sRealData):
            print("OnReceiveRealData: ", sJongmokCode, ", ", sRealType, ", ", sRealData)
            # self.textbox2.setText(sJongmokCode + "\n" + sRealType + "\n" + sRealData)

            if sRealType == "주식체결":
                data2 = self.kiwoom.dynamicCall('CommGetData(QString, QString, QString, int, QString)', sJongmokCode, sRealType, 10, 0, "")
                print("current price: ", data2)

            data = sRealData.split("\t")

            self.write("********************************")
            self.write(sJongmokCode)
            self.write(sRealType)

            self.write("sRealType: %s" % sRealType)

            for i in range(len(data)):
                self.write("Item %i %s" % (i, data[i]))

            self.write("**************************")
            self.write(sJongmokCode)
            self.write(sRealType)
            self.write(len(data), data)

    def btn_clicked(self):
        ret = self.kiwoom.dynamicCall("CommConnect()")

    def btn_term_clicked(self):
        ret = self.kiwoom.dynamicCall("CommTerminate()")

    def btn_clicked2(self):
        ret = self.kiwoom.dynamicCall('SetInputValue(QString, QString)', "종목코드", "000660")
        ret = self.kiwoom.dynamicCall('CommRqData(QString, QString, int, QString)', "주식기본정보", "OPT10001", 0, "0101")

    def btn_clicked3(self):
        if self.kiwoom.dynamicCall('GetConnectState()') == 0:
            print("Not connected")
        else:
            print("Connnected")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
