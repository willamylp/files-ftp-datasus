import os
import sys
from ftplib import FTP
import getpass
from UI import Ui_Sys_Datasus
from PyQt5.QtWidgets import QApplication, QMainWindow

class Download_FTP:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_Sys_Datasus()
        self.ui.setupUi(self.main_win)

        self.ui.checkBPA.clicked.connect(self.checked)
        self.ui.checkSISAIH01.clicked.connect(self.checked)
        self.ui.checkSIHD2.clicked.connect(self.checked)

    def show(self):
        self.main_win.show()

    def checked(self):
        if(self.ui.checkBPA.isChecked()):
            self.ui.input_BPA.setEnabled(True)
        else:
            self.ui.input_BPA.setEnabled(False)

        if(self.ui.checkSISAIH01.isChecked()):
            self.ui.input_SISAIH01.setEnabled(True)
        else:
            self.ui.input_SISAIH01.setEnabled(False)
        
        if(self.ui.checkSIHD2.isChecked()):
            self.ui.input_CMPT.setEnabled(True)
            self.ui.input_VERSAO.setEnabled(True)
        else:
            self.ui.input_CMPT.setEnabled(False)
            self.ui.input_VERSAO.setEnabled(False)
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = Download_FTP()
    main_win.show()
    sys.exit(app.exec_())
