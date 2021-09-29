# -*- coding: utf-8 -*-
# Criado por: Willamy Domingos
# ------------------------------------------------------------------------

import os
from ftplib import FTP
import getpass

def verifica_dir(directorio):
    if not (os.path.isdir(directorio)):
        os.makedirs(directorio)
    return

def download_file(ftp_host, username, password, remote_dir, filename, local_dir):
    ftp = FTP(ftp_host, username, password)
    ftp.login()
    ftp.cwd(remote_dir)
    
    # Download do arquivo
    verifica_dir(local_dir)
    print('\n--> Baixando Arquivo {} ...'.format(filename))
    local_filename = os.path.join(r"{}".format(local_dir), filename)
    lf = open(local_filename, "wb")
    ftp.retrbinary("RETR " + filename, lf.write, 8*1024)
    lf.close()
    return

def download_BPA():
    filename = input("[BPA] - Nome do Arquivo (Ex. BDSIA202109a.exe): ")
    ftp_host = "arpoador.datasus.gov.br"
    remote_dir = "/siasus/sia/"
    local_dir = '/Users/{}/Downloads/Arquivos_Atualizacao/BPA'.format(user_os)
        
    download_file(ftp_host, "", "", remote_dir, filename, local_dir)
    print('--> {} Baixado com Sucesso!\n'.format(filename))

def download_SISAIH01():
    filename = input("[SISAIH01] - Versão do Arquivo (Ex. 19.10): ")
    filename = "sisaih01_ver{}.exe".format(filename.replace('.', ''))
    ftp_host = "ftp2.datasus.gov.br"
    remote_dir = "/public/sistemas/dsweb/SIHD/Programas/"
    local_dir = '/Users/{}/Downloads/Arquivos_Atualizacao/SISAIH01'.format(user_os)

    download_file(ftp_host, "", "", remote_dir, filename, local_dir)
    print('--> {} Baixado com Sucesso!\n'.format(filename))

def download_SIHD2():
    compt = input("[SIHD2] - Competência MES/ANO (Ex. 08/2021): ")
    compt = compt.split('/')
    versao = input('[SIHD2] - Versão do Arquivo (Ex. 17.40): ')
    versao = "SIHD2_{}.exe".format(versao.replace('.', ''))
            
    ftp_host_1 = "ftp.datasus.gov.br"
    ftp_host_2 = "ftp2.datasus.gov.br"
    local_dir = '/Users/{}/Downloads/Arquivos_Atualizacao/SIHD2'.format(user_os)
    
    files = {
        'Fornec': ['/cnes/', 'FORNEC_{}.ZIP'.format(compt[1]+compt[0])],
        'Import': ['/cnes/', 'IMPORT_{}.ZIP'.format(compt[1]+compt[0])],
        'TercBR': ['/cnes/', 'TERCEIROSBRASIL24_{}.ZIP'.format(compt[1]+compt[0])],
        'Install': ['/public/sistemas/dsweb/SIHD/Programas/', versao],
        'DSIHD017': ['/public/sistemas/dsweb/SIHD/Programas/DSIHD017/', 'DSIHD017_24_{}.ZIP'.format(compt[1]+compt[0])]
    }
    
    for key in files.keys():
        if((key == 'Install') or (key == 'DSIHD017')):
            download_file(ftp_host_2, "", "", files[key][0], files[key][1], local_dir)
        else:
            download_file(ftp_host_1, "", "", files[key][0], files[key][1], local_dir)
        print('--> {} Baixado com Sucesso!'.format(files[key][1]))

if __name__ == '__main__':
    
    user_os = getpass.getuser()

    print('''\t
        #########  DOWNLOAD DOS ARQUIVOS DOS SISTEMAS  #########
        ________________ Selecione uma Opção ___________________

        Opção 01 - Baixar Todos os Arquivos (BPA/SISAIH01/SIHD2)
          
        Opção 02 - Tabelas do SIA/BPA
        Opção 03 - Arquivo do SISAIH01
        Opção 04 - Arquivos do SIHD2

        Opção 99 - Sair do Programa
        ________________________________________________________\n\n''')
        
    while(True):
        opcao = input("\t--> Informe sua Opção: ")
        
        if((opcao == '1') or (opcao == '01')):
            download_BPA()
            download_SISAIH01()
            download_SIHD2()

        elif((opcao == '2') or (opcao == '02')):
            download_BPA()

        elif((opcao == '3') or (opcao == '03')):
            download_SISAIH01()

        elif((opcao == '4') or (opcao == '04')):
            download_SIHD2()

        elif(opcao == '99'):
            break
        
        else:
            print('\t>> Informe uma Opção Válida!')
