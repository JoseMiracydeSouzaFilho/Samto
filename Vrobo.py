# coding: utf-8
# encoding: win-1252

import os
from functools import partial
from tkinter import *
import threading
from time import gmtime, strftime
import socket
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import xml.sax


class CreatedHandler(FileSystemEventHandler):
    patterns = ["*.xml"]

    def on_created(self, event):
        if event.is_directory:
           return

        filepath, ext = os.path.splitext(event.src_path)
        #print(' filepath criado : _-->  ', filepath)
        if 'TestRunReport' in filepath:
            if ext == '.xml' and '-fixed' not in filepath:
                parser = xml.sax.make_parser()
                msg=''
                parser.setContentHandler(getreportXML(msg))
                parser.parse(event.src_path)
                print ('chamou getReport : ', filepath)


class getreportXML(xml.sax.handler.ContentHandler):
    def __init__(self, msg):
        xml.sax.handler.ContentHandler.__init__(self)
        self.prefixo = ''
        self.msg = msg
        togleTagXML("0")

        # É chamado quando uma novo tag é encontrada
    def startElement(self, tag, attr):
        self.prefixo += ' '
        if tag in ['Passed','RunName','Start','Duration']:
            print (self.prefixo +'TAG ->', tag)
            self.msg += tag + ','
            togleTagXML("1")

        # É chamado quando texto é encontrado
    def characters(self, txt):
        if txt.strip():
            if achouTag:
                if "," in txt :
                    s0 = txt.split(",")[0]  # recurso para tirar a virgula do Duration
                    s1 = txt.split(",")[1]
                    txt = s0 + s1
                self.msg+=txt + ','
                print (self.prefixo + 'TXT - >', txt)
                togleTagXML("0")
                if 'Duration' in self.msg:
                    print(" Verificar a ultima virgula na string do Handler : ", self.msg)
                    getMsgXLM(self.msg)

        # É chamado quando o fim de uma tag é encontrada
    def endElement(self, name):
        self.prefixo = self.prefixo[:-2]


def togleTagXML(x):
    if "1" in x:
        global achouTag
        achouTag = True
    elif "0":
        achouTag = False


def getMsgXLM(msg):
    print ('Valor de State :',STATE)
    if STATE != ESTADO_MANUT:    # So transmite para server se o estado nao for igual a Manutenção
        msg = ESTADO_ATIVO + ',' + SETUP +','+ 'EngTest'+',' + ENGTEST + ',' + 'Project' + ',' + PROJECT + ',' + 'Binary'+','\
            + BINARY + ',' + msg + 'Mode of Operation' + ',' + MODE
        print ('String Final para Socket: ', msg)
        envia_msg_Server(msg)


class GuiPart(object):
    def __init__(self, master, get_dataentry, get_maint):
        # self.queue = queue
        self.master = master
        # Inicia Interface Grafica,

        master.title('ROBO CLIENT')

        master.option_add('*Font', 'Arial 10')
        master.option_add('*EntryField.Entry.Font', 'Courier 10')
        master.option_add('*Listbox*Font', 'Courier 10')
        # Defino o tipo de Letra do Menu
        # Desenho o Menu
        self.menubar = Menu(master)
        master.geometry("480x600+300+50")
        self.cmdmenu = Menu(self.menubar)
        self.cmdmenu.add_command(label='Open...', underline=0)
        self.cmdmenu.add('separator')
        self.cmdmenu.add_command(label='Maintenance', underline=0,
                                background='white', activebackground='green',
                                command= get_maint)
        self.menubar.add_cascade(label="File", menu=self.cmdmenu)
        master.config(menu=self.menubar)

        Frame1 = Frame(master,borderwidth=2,relief=GROOVE, highlightthickness=2, highlightbackground="#111")

        Label(Frame1, text = "ENG TEST :").grid(row=0,column=0,padx=5,pady=5,sticky=W)
        self.HOST = StringVar()
        self.HOST.set(IP_Server)
        self.ENGTEST = StringVar()
        Entry(Frame1, textvariable= self.ENGTEST).grid(row=0,column=1,padx=5,pady=5)

        Label(Frame1, text = "PROJECT :").grid(row=1,column=0,padx=5,pady=5,sticky=W)
        self.PORT = IntVar()
        self.PORT.set(21000)
        self.PROJECT = StringVar()
        Entry(Frame1, textvariable=self.PROJECT).grid(row=1,column=1,padx=5,pady=5)

        Label(Frame1, text="BINARY :").grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.BINARY = StringVar()
        Entry(Frame1, textvariable=self.BINARY).grid(row=2, column=1, padx=1, pady=1)

        #Label(Frame1, text="MODE :").grid(row=3, column=0, padx=5, pady=5, sticky=W)
        self.MODE = IntVar()
        #Entry(Frame1, textvariable=self.MODE).grid(row=3, column=1, padx=5, pady=5)
        Radiobutton(Frame1,text=' AUTOMATIC ',value=1,variable=self.MODE,indicatoron=0).grid(row=0, column=2, padx=5, pady=5)
        Radiobutton(Frame1,text=' MANUAL    ', value=2, variable=self.MODE,indicatoron=0).grid(row=1, column=2, padx=5, pady=5)
        self.MODE.set(1)

        Frame1.grid(row=0,column=0,padx=5,pady=5,sticky=W+E)
        Frame3 = Frame(master, borderwidth=2, relief='sunken', highlightthickness=2, highlightbackground="#111")
        self.lbl_Robo = Label(Frame3, relief=RAISED, borderwidth=2, text="     LOG TRACKING from Server    ")
        self.lbl_Robo.grid(row=0, column=0, padx=5, pady=5, sticky=W + E)
        self.Text_Robo = Text(Frame3, width=54, height=20, state=DISABLED)

        self.Text_Robo.config(state=NORMAL)
        self.Text_Robo.insert(END, '-> Robo Client Ready .... \n')
        self.Text_Robo.yview_scroll(1, "pages")
        self.Text_Robo.config(state=DISABLED)

        self.Text_Robo.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        scroll_r1 = Scrollbar(Frame3, command=self.Text_Robo.yview)
        self.Text_Robo.configure(yscrollcommand=scroll_r1.set)
        scroll_r1.grid(row=1, column=2, padx=5, pady=5, sticky=E + S + N)

        Frame3.grid(row=2, column=0, padx=5, pady=5)

        self.bt_start = Button(Frame1, text=' CONFIRM ', bg="#ECE82E", command=get_dataentry)
        self.bt_start.grid(row=2, column=2, rowspan=2, padx=5, pady=5)



class ThreadReception_Server(threading.Thread):

    def __init__(self, conn,text):
        threading.Thread.__init__(self)
        self.connexion = conn  # Socket Robotino
        self.text = text


    def run(self):

        while True:
            try:
                # Recebe msg do Server
                message_rec = self.connexion.recv(1024).decode(encoding='UTF-8')

                if "START" in message_rec:
                    print ('Servidor Ativo')
                if "ACK" in message_rec:
                    print ('Servidor Recebeu os Dados Corretamente')
                else :
                    print ('Servidor  not Recebeu os Dados Corretamente - Reenviar ')

            except socket.error:
                pass


class ThreadedClient(object):
    def __init__(self, master,state):

        self.master = master
        self.estado = state
        # Create the queue
        # self.queue = queue.Queue()
        # Set up the GUI part
        self.gui = GuiPart(self.master, self.get_data_entry,self.get_maint)
        self.robo = Conecta_Server(self.gui.Text_Robo,self.gui.lbl_Robo) #Thread de conexao  com SAMTO server
        self.robo.start()
        self.get_laststate()
        if STATE == ESTADO_DISP:
            self.get_data_entry()

    def get_laststate(self):
        try:
            with open(path_manutfile,'r') as f: # abre o arquivo para le a ultima linha / o ultimo estado resgitrado
                r = f.readlines()
                last_line = r [len(r)-1]
                self.estado = last_line
                global STATE
                STATE = self.estado
                print ('ultima linha ',self.estado)
                f.close()
        except IOError:
            with open(path_manutfile,"a") as f:  # Se o arquivo nao existe cria 1a vez
                f.close()
                with open(path_manutfile, "a") as f:
                    f.write(ESTADO_DISP + '\n')
                    f.close()
                    STATE = ESTADO_DISP
                print(' File manutencao criado e Dado inicial inserido', ESTADO_DISP)

    def get_data_entry(self):
        global ENGTEST, PROJECT, BINARY, MODE, STATE
        STATE = ESTADO_DISP    # tem que avaaliar se o estado anterior era manuten
        envia_msg_Server(STATE)  # Saiu de Manutençao e foi para disp ou Clicou n botao
        with open(path_manutfile, "a") as f:
            f.write(STATE + '\n')
            f.close()
        ENGTEST = self.gui.ENGTEST.get()
        if ENGTEST =="":
            ENGTEST = 'none'
        PROJECT = self.gui.PROJECT.get()
        if PROJECT =="":
            PROJECT = 'none'
        BINARY = self.gui.BINARY.get()
        if BINARY =="":
            BINARY = 'none'
        MODE = str(self.gui.MODE.get())
        if MODE == "1":
            MODE = "AUTO"
        else:
            MODE = "MAN"


        self.gui.Text_Robo.config(state=NORMAL)
        self.gui.lbl_Robo.config(bg='#6EEC78')
        self.gui.Text_Robo.insert (END," \n : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : \n")
        self.gui.Text_Robo.insert (END," Welcome , Session Started for : \n")
        self.gui.Text_Robo.insert(END,ENGTEST + '\n')
        self.gui.Text_Robo.insert(END,PROJECT + '\n')
        self.gui.Text_Robo.insert(END,BINARY + '\n')
        self.gui.Text_Robo.insert(END,MODE + '\n')
        self.gui.Text_Robo.yview_scroll(1, "pages")
        self.gui.Text_Robo.config(state=DISABLED)

        # return [ENGTEST,PROJECT,BINARY,MODE]

    def get_maint(self):
        self.estado = ESTADO_MANUT
        self.gui.Text_Robo.config(state=NORMAL)
        self.gui.lbl_Robo.config(bg='#ECE82E')
        self.gui.Text_Robo.insert(END," \n ################################################ \n")
        self.gui.Text_Robo.insert(END,"             State of Maintenace was activated :")
        self.gui.Text_Robo.insert(END," \n ################################################ \n")
        self.gui.Text_Robo.yview_scroll(1, "pages")
        self.gui.Text_Robo.config(state=DISABLED)

        t1 = Toplevel(self.gui.master,borderwidth=5, bg='white')
        t1.title(" Maintenance ")
        t1.geometry("220x100+800+80")
        Label(t1, text="Enter Maintenance code :").grid(row=0,column=0)
        self.manutext = StringVar()
        self.manutentry = Entry(t1,textvariable=self.manutext).grid(row=1,column=0)
        self.mybutton = Button(t1,text = "OK",bg="#ECE82E",command = partial(self.sendmsg,self.estado)).grid(row=2,column=0, rowspan=2)

    def sendmsg(self,state):   #envia o Estado de manutenção para o Server
        global STATE
        STATE = state
        code = self.manutext.get()
        print(' Digitou o codigo : ',code)
        msg = state + ',' + SETUP + ',' + ENGTEST + ',' + code + ',' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ',' \
              + '1hora'
        envia_msg_Server(msg)
        with open(path_manutfile,"a") as f:
            f.write(state + '\n')
            f.close()

class Conecta_Server(threading.Thread):
    def __init__(self,text,lbl):
        threading.Thread.__init__(self)
        self.text = text
        self.lbl = lbl

    def run(self):
        global CONECTA_SERVER
        global SOCKET_ROBO

        while 1:
            if CONECTA_SERVER == False:
                try:
                    server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_Socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                    server_Socket.connect((IP_Server, PORT_SERVER))
                    # Conversa com  (server ): Lança uma thread para pegar as  messages
                    th_R = ThreadReception_Server(server_Socket,self.text)
                    th_R.start()
                    print("[+] Nova Thread Iniciada para Robo:  "+IP_Server+":"+str(PORT_SERVER))
                    CONECTA_SERVER = True
                    SOCKET_ROBO = server_Socket
                    self.lbl.config(bg='#6EEC78')
                    self.text.config(state=NORMAL)
                    self.text.insert(END, ' ------------------------------------------------------------------------\n')
                    self.text.insert(END, 'SAMTO Server is Connected ....\n')
                    self.text.insert(END, ' ------------------------------------------------------------------------\n')
                    self.text.yview_scroll(1, "pages")
                    self.text.config(state=DISABLED)

                except socket.error:
                    print('Error','The connection with server has failed .')
                    self.text.config(state=NORMAL)
                    self.text.insert(END, 'The connection with server has failed.... Trying \n')
                    self.text.yview_scroll(1, "pages")
                    self.text.config(state=DISABLED)
                    CONECTA_SERVER = False


class envia_msg_Server(object):
    def __init__(self,message):
        self.msg = message
        #self.txt = text
        if CONECTA_SERVER == True:
            try:
                SOCKET_ROBO.send(bytes(self.msg,"UTF8"))
                print ('Mensagem enviada para SERVER :',self.msg)
            except socket.error:
                print ('Mensagem nao enviada para SERVER :',self.msg)
                pass


if __name__ == "__main__":
    ESTADO_ATIVO = "TESTING"
    ESTADO_MANUT = "MAINTENANCE"
    ESTADO_DISP = "AVALIABLE"
    MESAGEM_LOG = 'LOG'

    #IP_Server = '105.112.146.197'
    IP_Server = '127.0.0.1'
    PORT_SERVER = 21000
    CONECTA_SERVER = False


    msgfinal = ''
    SETUP = 'ANRITSU_LTE_1_ATT'
    event_handler = CreatedHandler()
    observer = Observer()
    pathline = "/home/jmiracy/RTDTests"
    path_manutfile = '/home/jmiracy/Samto/maintenance.txt'
    observer.schedule(event_handler, pathline, True)
    observer.start()

    root = Tk()
    client = ThreadedClient(root,ESTADO_DISP)
    root.mainloop()