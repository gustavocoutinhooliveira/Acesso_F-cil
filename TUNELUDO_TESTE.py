from selenium.webdriver.support.wait import WebDriverWait
from asyncio.windows_events import ERROR_CONNECTION_ABORTED
from tkinter import messagebox
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By # Procurar elementos 
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile #Iniciar Perfil cache limpo
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary  #Apontamento PATH firefox instalado
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from pynput.keyboard import Key, Controller
import re
from tkinter import *
import time
import os
import logging
from datetime import datetime
from sshtunnel import SSHTunnelForwarder
from paramiko import SSHClient
import paramiko
import threading


log = open("log_tuneludo.txt",'a')
ie_options = webdriver.IeOptions()
ie_options.attach_to_edge_chrome = True
ie_options.edge_executable_path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
#Testar modo IE no EDGE, descomentar abaixo


class PlataformaEDI():


    def validate(P):
        ip = re.compile('(^\d{0,3}$|^\d{1,3}\.\d{0,3}$|^\d{1,3}\.\d{1,3}\.\d{0,3}$|^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{0,3}$)')
        if ip.match(P):
            return True
        else:
            return False

    
    janela_principal = Tk()
    janela_principal.title('TUNELUDO')
    mainFont = ('Verdana','10','bold')
    #janela_principal.minsize(width=295, height=135)
    #janela_principal.maxsize(width=295, height=135)

    janela_principal.icosnbitmap('EDI.ico')

    Codigo = StringVar()
    Nome = StringVar()
    IpdoPosto = StringVar()

    #Criando os objetos que estarão na janela...
    #lblCodigo = Label(janela_principal, text="Codigo do cliente: ")
    #lblNome = Label(janela_principal, text="Nome do cliente: ")
    lblIpPosto = Label(janela_principal, text="IP do Posto")
    
    #entCodigo = Entry(janela_principal, textvariable=Codigo,width=25,justify="center")
    #entNome = Entry(janela_principal, textvariable=Nome,width=25,justify="center")

    vcmd = janela_principal.register(validate)
    entIpPosto = Entry(janela_principal, textvariable = IpdoPosto, width = 25, validate = 'key', validatecommand = (vcmd, '%P'))
    entIpPosto      = Entry(janela_principal, textvariable=IpdoPosto)
    #btnIniciar    = Button(janela_principal, text="Executar varios por Lote", bg="red",fg='white')
    btnAcessar    = Button(janela_principal, text="Acessar", bg="black",fg='white')
    
    #lblCodigo.grid(row=0,column=0,sticky=E,padx=5,pady=5)
    #lblNome.grid(row=1,column=0,sticky=E,padx=5,pady=5)
    lblIpPosto.grid(row=2,column=0,sticky=E,padx=5,pady=5)
    #entCodigo.grid(row=0, column=1,sticky=W,padx=5,pady=5)
    #entNome.grid(row=1, column=1,sticky=W,padx=5,pady=5)
    entIpPosto.grid(row=2, column=1,sticky=W,padx=5,pady=5)
    #larguraacima

    #btnIniciar.grid(row=3, column=0, columnspan=1,padx=5,pady=5)
    btnAcessar.grid(row=3, column=1, columnspan=1,padx=5,pady=5)
    #fundoprincipalacima

 


  
def iniciarUnico():
    Ip_posto = app.IpdoPosto.get()
    #nome_posto = app.Nome.get()
    #Codigo_posto = app.Codigo.get()

    janelinha = Tk()
    janelinha.title('TUNEL FACIL')
    mainFont = ('Verdana','10','bold')
    janelinha.iconbitmap('EDI.ico')

    lblpergunta = Label(janelinha, text="Selecione equipamento que deseja conectar",font=("Verdana"))
    btnHondian   = Button(janelinha, text="Hondian", bg="black",fg='white')
    btnVpar_41    = Button(janelinha, text="VPAR 192.168.X.41", bg="blue",fg='white')
    btnVpar_42    = Button(janelinha, text="VPAR 192.168.X.42", bg="blue",fg='white')
    btnSaturno    = Button(janelinha, text="Saturno", bg="green",fg='white')
    btnPresveic    = Button(janelinha, text="Presveic", bg="red",fg='white', activebackground="white", activeforeground="pink")
    btnConversor   = Button(janelinha, text="Conversor/Sensor", bg="black",fg='white')

    lblpergunta.grid(row=0,column=0,columnspan=3,sticky=N,padx=5,pady=5)
    btnHondian.grid(row=2, column=0, columnspan=1,padx=5,pady=5)
    btnVpar_41.grid(row=2, column=1, columnspan=1,padx=5,pady=5)
    btnVpar_42.grid(row=3, column=1, columnspan=1,padx=5,pady=5)
    btnSaturno.grid(row=2, column=2, columnspan=1,padx=5,pady=5)
    btnPresveic.grid(row=2, column=4, columnspan=1,padx=5,pady=5)
    btnConversor.grid(row=3, column=0, columnspan=1,padx=5,pady=5)
    try:
            class SSH:
                def __init__(self):
                    self.ssh = SSHClient()
                    self.ssh.load_system_host_keys()
                    self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    self.ssh.connect(hostname= str(Ip_posto),port='22',username='pi',password='SemParar')         
            hondian = SSHTunnelForwarder(
                str(Ip_posto),
                ssh_username="pi",
                ssh_password="SemParar",
                remote_bind_address=('192.168.8.1',80),
                local_bind_address=('127.0.0.1',8000)
                )
            
            hondian.start()
    except:
            log.write(datetime.now().strftime('%d/%m/%Y %H:%M:%S') + " Erro na conexão com Hondian: " + str(Ip_posto) + '\n')
            print("Erro na conexão com Hondian" + str(Ip_posto))
            messagebox.showerror('Erro de Conexão','#Hondian possivelmente fora do ar#' + '\n' + str(Ip_posto) + '\n')    
    try:
            class SSH:
                def __init__(self):
                    self.ssh = SSHClient()
                    self.ssh.load_system_host_keys()
                    self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    self.ssh.connect(hostname= str(Ip_posto),port='22',username='pi',password='SemParar')
            descobrir_rede_interna = 'cat /var/abastece/forseti/config.json | grep "ip_local" | cut ' + "-d'" + '"' + "' -f4"

            Ssh = SSH()

            stdin,stdout,stderr = Ssh.ssh.exec_command(descobrir_rede_interna)
            ip_posto = stdout.read()
            ip_posto = ip_posto.split('\n'.encode())    

            ip_posto = str(ip_posto).replace("b","").replace(',',"").replace('[',"").replace(']',"").replace("'","").replace(" ","")    

            ip1 = ip_posto.split('.')

            ip1 = ip1[0] + "." + ip1[1] + "." + ip1[2]

            #ip_posto = ip1            

            vpar1 = SSHTunnelForwarder(
                str(Ip_posto),
                ssh_username="pi",
                ssh_password="SemParar",
                #remote_bind_address=('192.168.212.41',80),
                remote_bind_address=(str(ip1) + '.41',80),
                local_bind_address=('127.0.0.1',8001)
                )
            
            vpar1.start()     
    except:
            log.write(datetime.now().strftime('%d/%m/%Y %H:%M:%S') + " Erro na conexão com Vpar41: " + str(Ip_posto) + '\n')
            print("Erro na conexão com Vpar41" + str(Ip_posto))
            messagebox.showerror('Erro de Conexão','#Vpar41 possivelmente fora do ar#' + '\n' + str(Ip_posto) + '\n')   
    try:
            class SSH:
                def __init__(self):
                    self.ssh = SSHClient()
                    self.ssh.load_system_host_keys()
                    self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    self.ssh.connect(hostname= str(Ip_posto),port='22',username='pi',password='SemParar')
            descobrir_rede_interna = 'cat /var/abastece/forseti/config.json | grep "ip_local" | cut ' + "-d'" + '"' + "' -f4"

            Ssh = SSH()

            stdin,stdout,stderr = Ssh.ssh.exec_command(descobrir_rede_interna)
            ip_posto = stdout.read()
            ip_posto = ip_posto.split('\n'.encode())    

            ip_posto = str(ip_posto).replace("b","").replace(',',"").replace('[',"").replace(']',"").replace("'","").replace(" ","")    

            ip1 = ip_posto.split('.')

            ip1 = ip1[0] + "." + ip1[1] + "." + ip1[2]

            #ip_posto = ip1            

            vpar2 = SSHTunnelForwarder(
                str(Ip_posto),
                ssh_username="pi",
                ssh_password="SemParar",
                #remote_bind_address=('192.168.212.41',80),
                remote_bind_address=(str(ip1) + '.42',80),
                local_bind_address=('127.0.0.1',8002)
                )
            
            vpar2.start()   
    except:
            log.write(datetime.now().strftime('%d/%m/%Y %H:%M:%S') + " Erro na conexão com Vpar42: " + str(Ip_posto) + '\n')
            print("Erro na conexão com Vpar42 " + str(Ip_posto))
            messagebox.showerror('Erro de Conexão','#Vpar42 possivelmente fora do ar#' + '\n' + str(Ip_posto) + '\n')       
    try:
            class SSH:
                def __init__(self):
                    self.ssh = SSHClient()
                    self.ssh.load_system_host_keys()
                    self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    self.ssh.connect(hostname= str(Ip_posto),port='22',username='pi',password='SemParar')
            descobrir_rede_interna = 'cat /var/abastece/forseti/config.json | grep "ip_local" | cut ' + "-d'" + '"' + "' -f4"

            Ssh = SSH()

            stdin,stdout,stderr = Ssh.ssh.exec_command(descobrir_rede_interna)
            ip_posto = stdout.read()
            ip_posto = ip_posto.split('\n'.encode())    

            ip_posto = str(ip_posto).replace("b","").replace(',',"").replace('[',"").replace(']',"").replace("'","").replace(" ","")    

            ip1 = ip_posto.split('.')

            ip1 = ip1[0] + "." + ip1[1] + "." + ip1[2]

            #ip_posto = ip1            

            saturno = SSHTunnelForwarder(
                str(Ip_posto),
                ssh_username="pi",
                ssh_password="SemParar",
                #remote_bind_address=('192.168.212.41',80),
                remote_bind_address=(str(ip1) + '.21',8082),
                local_bind_address=('127.0.0.1',8082)
                )
            
            saturno.start()      
    except:
            log.write(datetime.now().strftime('%d/%m/%Y %H:%M:%S') + " Erro na conexão com Saturno: " + str(Ip_posto) + '\n')
            print("Erro na conexão com Saturno " + str(Ip_posto))
            messagebox.showerror('Erro de Conexão','#Posto possivelmente utiliza SLT ou Saturno está fora do ar#' + '\n' + str(Ip_posto) + '\n')                                                
            
    
#def teste():
    def Hondian():
        #threading.Thread(target=iniciarUnico).start()
        
            
            
        
            driver = webdriver.Edge()

            
            driver.get('http://127.0.0.1:8000')
            
            
            
            #time.sleep(3)
            try:

                WebDriverWait(driver, timeout=120).until(lambda d: d.find_element(By.XPATH,'//*[@id="login_user"]/div[2]/input')).click()
                WebDriverWait(driver, timeout=120).until(lambda d: d.find_element(By.XPATH,'//*[@id="login_user"]/div[2]/input')).send_keys('admin')
                WebDriverWait(driver, timeout=120).until(lambda d: d.find_element(By.XPATH,'//*[@id="login_passwd"]/div[2]/input')).click()
                WebDriverWait(driver, timeout=120).until(lambda d: d.find_element(By.XPATH,'//*[@id="login_passwd"]/div[2]/input')).send_keys('@bast3ce')
                WebDriverWait(driver, timeout=120).until(lambda d: d.find_element(By.XPATH,'//*[@id="contents1"]/form/div/input')).click()
                Hondian.after(0.1)
                
                
                time.sleep(300)
                

            except:
                def _waitForAlert(driver):
                 return WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert = _waitForAlert(driver)
                value = alert.text
                print(value)
                alert.accept()
                WebDriverWait(driver, timeout=120).until(lambda d: d.find_element(By.XPATH,'//*[@id="login_user"]/div[2]/input')).click()
                WebDriverWait(driver, timeout=120).until(lambda d: d.find_element(By.XPATH,'//*[@id="login_user"]/div[2]/input')).send_keys('abastece')
                WebDriverWait(driver, timeout0=120).until(lambda d: d.find_element(By.XPATH,'//*[@id="login_passwd"]/div[2]/input')).click()
                WebDriverWait(driver, timeout=120).until(lambda d: d.find_element(By.XPATH,'//*[@id="login_passwd"]/div[2]/input')).send_keys('@bast3ce')
                WebDriverWait(driver, timeout=120).until(lambda d: d.find_element(By.XPATH,'//*[@id="contents1"]/form/div/input')).click()

    def Vpar_41():
        #threading.Thread(target=iniciarUnico).start()
        

                try:
                    internet_explorer = webdriver.Ie(options=ie_options)
                    internet_explorer.get('http://127.0.0.1:8001')
                    WebDriverWait(internet_explorer, timeout=12).until(lambda d: d.find_element(By.ID,'username')).click()
                    WebDriverWait(internet_explorer, timeout=12).until(lambda d: d.find_element(By.ID,'username')).send_keys('oi')
                    WebDriverWait(internet_explorer, timeout=12).until(lambda d: d.find_element(By.ID,'password')).click()
                    WebDriverWait(internet_explorer, timeout=12).until(lambda d: d.find_element(By.ID,'password')).send_keys('oi')
                    WebDriverWait(internet_explorer, timeout=12).until(lambda d: d.find_element(By.ID,'password')).send_keys(Keys.RETURN)
                    Hondian.after(0.1)
                except:
                    WebDriverWait(internet_explorer, timeout=12).until(lambda d: d.find_element(By.ID,'username')).click()
                    WebDriverWait(internet_explorer, timeout=12).until(lambda d: d.find_element(By.ID,'username')).send_keys('oi')
                    WebDriverWait(internet_explorer, timeout=12).until(lambda d: d.find_element(By.ID,'password')).click()
                    WebDriverWait(internet_explorer, timeout=12).until(lambda d: d.find_element(By.ID,'password')).send_keys('oi')
                    WebDriverWait(internet_explorer, timeout=12).until(lambda d: d.find_element(By.ID,'password')).send_keys(Keys.RETURN)
                    Hondian.after(0.1)


    def Vpar_42():
        #threading.Thread(target=iniciarUnico).start()
        

            
            try:
                internet_explorer = webdriver.Ie(options=ie_options)
                internet_explorer.get('http://127.0.0.1:8002')
                WebDriverWait(internet_explorer, timeout=12).until(lambda d: d.find_element(By.ID,'username')).click()
                WebDriverWait(internet_explorer, timeout=12).until(lambda d: d.find_element(By.ID,'username')).send_keys('oi')
                WebDriverWait(internet_explorer, timeout=12).until(lambda d: d.find_element(By.ID,'password')).click()
                WebDriverWait(internet_explorer, timeout=12).until(lambda d: d.find_element(By.ID,'password')).send_keys('oi')
                WebDriverWait(internet_explorer, timeout=12).until(lambda d: d.find_element(By.ID,'password')).send_keys(Keys.RETURN)
                Hondian.after(0.1)
            except:
                WebDriverWait(internet_explorer, timeout=12).until(lambda d: d.find_element(By.ID,'username')).click()
                WebDriverWait(internet_explorer, timeout=12).until(lambda d: d.find_element(By.ID,'username')).send_keys('oi')
                WebDriverWait(internet_explorer, timeout=12).until(lambda d: d.find_element(By.ID,'password')).click()
                WebDriverWait(internet_explorer, timeout=12).until(lambda d: d.find_element(By.ID,'password')).send_keys('oi')
                WebDriverWait(internet_explorer, timeout=12).until(lambda d: d.find_element(By.ID,'password')).send_keys(Keys.RETURN)
                Hondian.after(0.1)    

        
    def Presveic():
        #threading.Thread(target=iniciarUnico).start()
        Hondian.after(0.1)
        log.write(datetime.now().strftime('%d/%m/%Y %H:%M:%S') + " Erro na configuração do posto: " + str(Ip_posto) + '\n')
        print("Erro na configuração do posto: " + str(Ip_posto))
        messagebox.showerror('Erro de Conexão','#Posto possivelmente fora do ar#' + '\n' + str(Ip_posto) + '\n')         
    def Saturno():
        #threading.Thread(target=iniciarUnico).start()
        

            log.write(datetime.now().strftime('%d/%m/%Y %H:%M:%S') + " Abrindo pagina da internet " + '\n')
            print(" Abrindo pagina da internet " + str(Ip_posto))
            

            driver = webdriver.Edge()

            driver.get('http://127.0.0.1:8082')
            
            #login 
            WebDriverWait(driver, timeout=15).until(lambda d: d.find_element(By.ID,'username')).click()
            WebDriverWait(driver, timeout=15).until(lambda d: d.find_element(By.ID,'username')).send_keys('admin')
            WebDriverWait(driver, timeout=15).until(lambda d: d.find_element(By.ID,'password'))
            WebDriverWait(driver, timeout=15).until(lambda d: d.find_element(By.ID,'password')).send_keys('admin')        
            WebDriverWait(driver, timeout=15).until(lambda d: d.find_element(By.XPATH,'//*[@id="root"]/div/div/div/form/div[3]/div/button')).click()
            
            log.write(datetime.now().strftime('%d/%m/%Y %H:%M:%S') + " Login Realizado " + '\n')
            print(" Login Realizado " + str(Ip_posto))
            
            log.write(datetime.now().strftime('%d/%m/%Y %H:%M:%S') + " Acessando Instalação Inicial " + '\n')
            print(" Acessando Instalação Inicial " + str(Ip_posto))
            Hondian.after(0.1)

            try:
                log.write(datetime.now().strftime('%d/%m/%Y %H:%M:%S') + " Tentando por SLT Instalação Inicial " + '\n')
                print(" Tentando por SLT Instalação Inicial " + str(Ip_posto))
                WebDriverWait(driver, timeout=120).until(lambda d: d.find_element(By.PARTIAL_LINK_TEXT,'Inicial')).click()
            except:
                log.write(datetime.now().strftime('%d/%m/%Y %H:%M:%S') + " Tentando por Saturno 3.3.10 " + '\n')
                print(" Tentando por Saturno 3.3.10 " + str(Ip_posto))
                WebDriverWait(driver, timeout=2).until(lambda d: d.find_element(By.PARTIAL_LINK_TEXT,'Saturno')).click()
        
            
        
    def Conversor():
        #threading.Thread(target=iniciarUnico).start()
        log.write(datetime.now().strftime('%d/%m/%Y %H:%M:%S') + " Erro na configuração do posto: " + str(Ip_posto) + '\n')
        print("Erro na configuração do posto: " + str(Ip_posto))
        messagebox.showerror('Erro de Conexão','#Posto possivelmente fora do ar#' + '\n' + str(Ip_posto) + '\n')        
        Hondian.after(0.1)

    btnHondian.configure(command=Hondian)
    btnVpar_41.configure(command=Vpar_41)
    btnVpar_42.configure(command=Vpar_42)
    btnSaturno.configure(command=Saturno)
    btnPresveic.configure(command=Presveic)
    btnConversor.configure(command=Conversor)

app = None
app = PlataformaEDI

def Sobre():
   messagebox.showinfo('Configurador EDI Estacione','#Desenvolvido pela equipe de Sustentação Abastece#\n\n1.Opção LOTE utiliza o estacionamentos.txt de parâmetro desta maneira:\n\n02451,02451 - V4 NUC AUTO POSTO SHELL,172.25.116.210\n\n2.Programa está orientado para ser executado em qualquer situação, nao limitado somente a clientes novos;\n\nQualquer dúvida conte conosco!')
      
menubar = Menu(PlataformaEDI.janela_principal)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label = "Sobre", command = Sobre)
menubar.add_cascade(label = "Detalhes", menu = helpmenu)

PlataformaEDI.janela_principal.config(menu = menubar)


#app.btnIniciar.configure(command=iniciar)
app.btnAcessar.configure(command=iniciarUnico)

PlataformaEDI.janela_principal.mainloop()
