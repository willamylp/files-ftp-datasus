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

        self.chkBPA = self.ui.checkBPA.isChecked()
        self.chkSISAIH01 = self.ui.checkSISAIH01.isChecked()
        self.chkSIHD2 = self.ui.checkSIHD2.isChecked()
        self.ui.checkBPA.clicked.connect(self.checked)
        self.ui.checkSISAIH01.clicked.connect(self.checked)
        self.ui.checkSIHD2.clicked.connect(self.checked)

        
        self.ui.DownloadButton.clicked.connect(self.download_BPA)
        
    def show(self):
        self.main_win.show()

    def checked(self):
        self.chkBPA = self.ui.checkBPA.isChecked()
        self.chkSISAIH01 = self.ui.checkSISAIH01.isChecked()
        self.chkSIHD2 = self.ui.checkSIHD2.isChecked()

        if(self.chkBPA):
            self.ui.input_BPA.setEnabled(True)
            self.ui.text_STATUS.appendPlainText('BPA MARCADO')
        else:
            self.ui.input_BPA.setEnabled(False)
            self.ui.text_STATUS.appendPlainText('BPA DESMARCADO')

        if(self.chkSISAIH01):
            self.ui.input_SISAIH01.setEnabled(True)    
        else:
            self.ui.input_SISAIH01.setEnabled(False)
        
        if(self.chkSIHD2):
            self.ui.input_CMPT.setEnabled(True)
            self.ui.input_VERSAO.setEnabled(True)
        else:
            self.ui.input_CMPT.setEnabled(False)
            self.ui.input_VERSAO.setEnabled(False)
        
        if(self.chkBPA or self.chkSIHD2 or self.chkSISAIH01):
            self.ui.DownloadButton.setEnabled(True)
            
        elif(self.chkBPA and self.chkSIHD2 and self.chkSISAIH01):
            self.ui.DownloadButton.setEnabled(False)
            
    def getSize(self, filename):
        st = os.stat(filename)
        return st.st_size

    def verifica_dir(self, directorio):
        if not (os.path.isdir(directorio)):
            os.makedirs(directorio)

    def download_file(self, ftp_host, username, password, remote_dir, filename, local_dir):
        self.ftp = FTP(ftp_host, username, password)
        self.ftp.login()
        self.ftp.cwd(remote_dir)
        
        # Download do arquivo
        self.verifica_dir(local_dir)
        self.ui.text_STATUS.appendPlainText(
            '--> Baixando Arquivo {} ...'.format(filename))
        self.local_filename = os.path.join(r"{}".format(local_dir), filename)
        self.lf = open(self.local_filename, "wb")
        self.ftp.retrbinary("RETR " + filename, self.lf.write, 8*1024)
        self.lf.close()
        
    def download_BPA(self):
        self.user_os = getpass.getuser()
        self.filename = self.ui.input_BPA.text()
        self.ftp_host = "arpoador.datasus.gov.br"
        self.remote_dir = "/siasus/sia/"
        self.local_dir = '/Users/{}/Downloads/Arquivos_Atualizacao/BPA'.format(self.user_os)

        self.download_file(self.ftp_host, "", "", self.remote_dir,
                      self.filename, self.local_dir)

        self.ui.text_STATUS.appendPlainText(
            '--> {} Baixado com Sucesso!\n'.format(self.filename))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = Download_FTP()
    main_win.show()
    sys.exit(app.exec_())
