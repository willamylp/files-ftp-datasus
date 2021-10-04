import os
import sys
from ftplib import FTP
import getpass
from ui.UI import Ui_Sys_Datasus

from PyQt5.QtWidgets import QApplication, QMainWindow

class Download_FTP:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_Sys_Datasus()
        self.ui.setupUi(self.main_win)

        self.ui.checkCNES.clicked.connect(self.checked)
        self.ui.checkBPA.clicked.connect(self.checked)
        self.ui.checkSISAIH01.clicked.connect(self.checked)
        self.ui.checkSIHD2.clicked.connect(self.checked)

        self.ui.DownloadButton.clicked.connect(self.verifica_checked)
        
    def show(self):
        self.main_win.show()

    def checked(self):
        self.chkCNES = self.ui.checkCNES.isChecked()
        self.chkBPA = self.ui.checkBPA.isChecked()
        self.chkSISAIH01 = self.ui.checkSISAIH01.isChecked()
        self.chkSIHD2 = self.ui.checkSIHD2.isChecked()

        if(self.chkCNES):
            self.ui.input_CMPT_CNES.setEnabled(True)
        else:
            self.ui.input_CMPT_CNES.setEnabled(False)

        if(self.chkBPA):
            self.ui.input_BPA.setEnabled(True)
        else:
            self.ui.input_BPA.setEnabled(False)

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
        
        if(self.chkCNES or self.chkBPA or self.chkSIHD2 or self.chkSISAIH01):
            self.ui.DownloadButton.setEnabled(True)
        else:
            self.ui.DownloadButton.setEnabled(False)

    def log_status(self, msg):
        self.ui.text_STATUS.appendPlainText(msg)

    def verifica_checked(self):
        self.chkCNES = self.ui.checkCNES.isChecked()
        self.chkBPA = self.ui.checkBPA.isChecked()
        self.chkSISAIH01 = self.ui.checkSISAIH01.isChecked()
        self.chkSIHD2 = self.ui.checkSIHD2.isChecked()
        
        if(self.chkCNES):
            self.download_CNES()
        if(self.chkBPA):
            self.download_BPA()
        if(self.chkSISAIH01):
            self.download_SISAIH01()
        if(self.chkSIHD2):
            self.download_SIHD2()
        
    def verifica_dir(self, directorio):
        if not (os.path.isdir(directorio)):
            os.makedirs(directorio)

    def download_file(self, ftp_host, username, password, remote_dir, filename, local_dir):
        self.ftp = FTP(ftp_host, username, password)
        self.ftp.login()
        self.ftp.cwd(remote_dir)
        self.size_file = (self.ftp.size(filename) / 1e+6)

        self.verifica_dir(local_dir)
        
        self.ui.text_STATUS.appendPlainText(
            '--> Baixando Arquivo {} —> {} MB'.format(filename, self.size_file))
        self.local_filename = os.path.join(r"{}".format(local_dir), filename)
        self.lf = open(self.local_filename, "wb")
        self.ftp.retrbinary("RETR " + filename, self.lf.write, 8*1024)
        self.lf.close()
    
    def download_CNES(self):
            self.user_os = getpass.getuser()
            self.compt = self.ui.input_CMPT_CNES.text()
            self.compt = self.compt.split('/')

            self.ftp_host = "ftp.datasus.gov.br"
            self.local_dir = '/Users/{}/Downloads/Arquivos_Atualizacao/CNES/CMPT {}-{}'.format(
                self.user_os, self.compt[0], self.compt[1])

            self.files = {
                'Fornec': ['/cnes/', 'FORNEC_{}.ZIP'.format(self.compt[1]+self.compt[0])],
                'Import': ['/cnes/', 'IMPORT_{}.ZIP'.format(self.compt[1]+self.compt[0])],
                'TercBR': ['/cnes/', 'TERCEIROSBRASIL24_{}.ZIP'.format(self.compt[1]+self.compt[0])],
            }

            for key in self.files.keys():
                self.download_file(self.ftp_host, "", "",
                self.files[key][0], self.files[key][1], self.local_dir)

                self.msg = '--> {} Baixado com Sucesso!\n'.format(self.files[key][1])
                self.log_status(self.msg)

    def download_BPA(self):
        self.user_os = getpass.getuser()
        self.filename = self.ui.input_BPA.text()
        self.ftp_host = "arpoador.datasus.gov.br"
        self.remote_dir = "/siasus/sia/"
        self.local_dir = '/Users/{}/Downloads/Arquivos_Atualizacao/BPA-SIA'.format(self.user_os)
        self.msg = '--> {} Baixado com Sucesso!\n'.format(self.filename)

        self.download_file(self.ftp_host, "", "", self.remote_dir,
                      self.filename, self.local_dir)

        self.log_status(self.msg)

    def download_SISAIH01(self):
        self.user_os = getpass.getuser()
        self.filename = self.ui.input_SISAIH01.text()
        self.filename = "sisaih01_ver{}.exe".format(
            self.filename.replace('.', ''))
        self.ftp_host = "ftp2.datasus.gov.br"
        self.remote_dir = "/public/sistemas/dsweb/SIHD/Programas/"
        self.local_dir = '/Users/{}/Downloads/Arquivos_Atualizacao/SISAIH01'.format(self.user_os)
        self.msg = '--> {} Baixado com Sucesso!\n'.format(self.filename)
        self.download_file(self.ftp_host, "", "", self.remote_dir,
                      self.filename, self.local_dir)

        self.log_status(self.msg)

    def download_SIHD2(self):
        self.user_os = getpass.getuser()
        self.compt = self.ui.input_CMPT.text()
        self.compt = self.compt.split('/')
        self.versao = self.ui.input_VERSAO.text()
        self.versao = "SIHD2_{}.exe".format(self.versao.replace('.', ''))

        self.ftp_host_1 = "ftp.datasus.gov.br"
        self.ftp_host_2 = "ftp2.datasus.gov.br"
        self.local_dir = '/Users/{}/Downloads/Arquivos_Atualizacao/SIHD2/CMPT {}-{}'.format(
            self.user_os, self.compt[0], self.compt[1])

        self.files = {
            'Fornec': ['/cnes/', 'FORNEC_{}.ZIP'.format(self.compt[1]+self.compt[0])],
            'Import': ['/cnes/', 'IMPORT_{}.ZIP'.format(self.compt[1]+self.compt[0])],
            'TercBR': ['/cnes/', 'TERCEIROSBRASIL24_{}.ZIP'.format(self.compt[1]+self.compt[0])],
            'Install': ['/public/sistemas/dsweb/SIHD/Programas/', self.versao],
            'DSIHD017': ['/public/sistemas/dsweb/SIHD/Programas/DSIHD017/', 
                        'DSIHD017_24_{}.ZIP'.format(self.compt[1]+self.compt[0])]
        }

        for key in self.files.keys():
            if((key == 'Install') or (key == 'DSIHD017')):
                self.download_file(self.ftp_host_2, "", "",
                                   self.files[key][0], self.files[key][1], self.local_dir)
            else:
                self.download_file(self.ftp_host_1, "", "",
                                   self.files[key][0], self.files[key][1], self.local_dir)

            self.msg = '--> {} Baixado com Sucesso!\n'.format(self.files[key][1])
            self.log_status(self.msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = Download_FTP()
    main_win.show()
    sys.exit(app.exec_())
