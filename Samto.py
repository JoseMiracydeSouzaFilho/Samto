""" Funcionando na Versão 3.4
     Samto Server - Versão Ok para Anritsu
     Sanctus Benecdictus
"""
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId
from tkinter import *
import threading
import time, queue
import socket, select
import errno
#from msvcrt import getch


class RegisterDataBase (object):

    def __init__(self):
        try:
            client = MongoClient(host="localhost",port = 27017)
            print ('-------MONGODB Conectado com Sucesso  --------------------------')
        except ConnectionFailure :
            sys.stderr.write("Could not connect to Mongo DB: %s")
            sys.exit(1)
        # Get a Databse Handle to a Database named "SAMTO"
        global dbh
        dbh = client['samto']
        # session_id = ObjectId()


class Register_tc_Database (object):

    def __init__(self,setup,engtest,project,binary,passed,tc,start,duration,mode):

        self.setup = setup
        self.engtest = engtest
        self.project = project
        self.binary  = binary
        self.passed  = passed
        self.tc = tc
        self.start = start
        self.duration = duration
        self.mode = mode

        tc_doc = {
            #"session_doc_id": self.ses_id,
            "setup": self.setup,
            "project_ref": [
                {
                    "engtest": self.engtest,
                    "project": self.project,
                    "binary": self.binary,
                    "testcase": self.tc,
                    "passed": self.passed,
                    "start": self.start,
                    "Duration": self.duration,
                    "mode": self.mode
                }
            ]
        }
        dbh.TestCase.insert(tc_doc)
        print("Successfully inserted TC document: %s" % tc_doc)


class Register_maint_Database (object):

    def __init__(self,setup,engtest,start,code,duration):

        maint_doc ={
            "setup": setup,
            "engtest": engtest,
            "start": start,
            "code": code,
            "duration": duration
        }
        dbh.maintenance.insert(maint_doc)


class GuiPart(object):
    def __init__(self, master, queue, startCommand, endCommand):
        self.queue = queue

        # Inicia Interface Grafica,

        master.title('SAMTO SERVER')

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
        self.cmdmenu.add_command(label='Quit', underline=0,
                                 background='white', activebackground='green',
                                 command=endCommand)
        self.menubar.add_cascade(label="File", menu=self.cmdmenu)
        master.config(menu=self.menubar)

        Frame1 = Frame(master,borderwidth=2,relief=GROOVE, highlightthickness=2, highlightbackground="#111")

        Label(Frame1, text = "IP SAMTO:").grid(row=0,column=0,padx=5,pady=5,sticky=W)
        self.HOST = StringVar()
        self.HOST.set(IP_Server)
        Entry(Frame1, textvariable= self.HOST).grid(row=0,column=1,padx=5,pady=5)

        Label(Frame1, text = "PROJECT :").grid(row=1,column=0,padx=5,pady=5,sticky=W)
        self.PORT = IntVar()
        self.PORT.set(21001)
        Entry(Frame1, textvariable= self.PORT).grid(row=1,column=1,padx=5,pady=5)

        Frame1.grid(row=0,column=0,padx=5,pady=5,sticky=W+E)

        Frame2 = Frame(master,borderwidth=2,relief=GROOVE, highlightthickness=2, highlightbackground="#111")

        self.lbl_anritsu_lte_3_att= Label(Frame2,relief=RAISED, borderwidth=2, text = "ANRITSU LTE 3 ATT")
        self.lbl_anritsu_lte_3_att.grid(row=0,column=0,padx=5,pady=5,sticky=W)
        self.lbl_anite_lte_1_sp= Label(Frame2,relief=RAISED, borderwidth=2, text = "  ANITE LTE 1 SP   ")
        self.lbl_anite_lte_1_sp.grid(row=1,column=0,padx=5,pady=5,sticky=W)
        self.lbl_rs_lte_pqa = Label(Frame2, relief=RAISED, borderwidth=2, text="  R&S LTE 1  PQA   ")
        self.lbl_rs_lte_pqa.grid(row=2, column=0, padx=5, pady=5, sticky=W)

        # self.lbl_galileo1 = Label(Frame2,width =10, height =1)
        # self.lbl_galileo1.grid(row=1,column=0,padx=5,pady=5,sticky=E)

        self.lbl_anritsu_lte_2_tmo = Label(Frame2,relief=RAISED, borderwidth=2, text = "ANRITSU LTE 2 TMO")
        self.lbl_anritsu_lte_2_tmo.grid(row=0,column=1,padx=5,pady=5,sticky=W)
        self.lbl_anite_lte_1_rio= Label(Frame2,relief=RAISED, borderwidth=2, text = " ANITE LTE 1 RIO  ")
        self.lbl_anite_lte_1_rio.grid(row=1,column=1,padx=5,pady=5,sticky=W)
        self.lbl_rs_lte_iot = Label(Frame2, relief=RAISED, borderwidth=2, text="  R&S LTE 2  IOT  ")
        self.lbl_rs_lte_iot.grid(row=2, column=1, padx=5, pady=5, sticky=W)

        #self.lbl_galileo2 = Label(Frame2,width =10, height =1,state=DISABLED)
        #self.lbl_galileo2.grid(row=1,column=1,padx=5,pady=5,sticky=E)

        self.lbl_anritsu_lte_1_att = Label(Frame2, relief=RAISED, borderwidth=2, text="ANRITSU LTE 1 ATT")
        self.lbl_anritsu_lte_1_att.grid(row=0, column=2, padx=5, pady=5, sticky=W)
        self.lbl_anite_3g_bsb = Label(Frame2, relief=RAISED, borderwidth=2, text=" ANITE 3G Brasilia  ")
        self.lbl_anite_3g_bsb.grid(row=1, column=2, padx=5, pady=5, sticky=W)
        self.lbl_rs_lte_ims = Label(Frame2, relief=RAISED, borderwidth=2, text="  R&S LTE 3  IMS  ")
        self.lbl_rs_lte_ims.grid(row=2, column=2, padx=5, pady=5, sticky=W)

        Frame2.grid(row=1,column=0,padx=5,pady=5)

        Frame3 = Frame(master,borderwidth=2,relief='sunken', highlightthickness=2, highlightbackground="#111")
        self.lbl_Robo = Label(Frame3,relief=RAISED, borderwidth=2, text = "     LOG TRACKING from Robots     ")
        self.lbl_Robo.grid(row=0,column=0,padx=5,pady=5,sticky=W+E)
        self.Text_Robo = Text(Frame3,width =60, height =20,state=DISABLED)

        self.Text_Robo.config(state=NORMAL)
        self.Text_Robo.insert(END,'-> Server Stand by Press START .... ' + '\n')
        self.Text_Robo.yview_scroll(1,"pages")
        self.Text_Robo.config(state=DISABLED)

        self.Text_Robo.grid(row=1,column=0,padx=5,pady=5,sticky=W)
        scroll_r1 = Scrollbar(Frame3, command = self.Text_Robo.yview)
        self.Text_Robo.configure(yscrollcommand = scroll_r1.set)
        scroll_r1.grid(row=1,column=2,padx=5,pady=5,sticky=E+S+N)

        Frame3.grid(row=2,column=0,padx=5,pady=5)

        self.circleCanvas = Canvas(Frame1,width=50, height=50)
        self.circleCanvas.grid(row=0, column=3,rowspan=2, padx=5, pady=10)
        self.redCircle()

        self.bt_start = Button(Frame1, text=' START ',bg="#ECE82E",command = startCommand)
        self.bt_start.grid(row=0,column=2,rowspan=2,padx=5,pady=5)


    def redCircle(self):
        self.circleCanvas.create_oval(10, 10, 40, 40, width=0, fill='red')

    def greenCircle(self):
        self.circleCanvas.create_oval(10, 10, 40, 40, width=1, fill='green')
        self.bt_start.config(state = DISABLED,relief=SUNKEN)

    def processIncoming(self):
        """ Verifica se tem ha algum dado na Queue a cada 200ms e faz a tratativa -  . """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do whatever is needed.
                print (msg +'\n')
                s0 = msg.split(",")[0]

                if s0 == ESTADO_ATIVO:
                    setup = msg.split(",")[1]    # setup
                    engtest = msg.split(",")[2]    # EngTEst
                    dt_engtest = msg.split(",")[3]    # Dado de EngTest
                    project = msg.split(",")[4]    # Project
                    dt_project = msg.split(",")[5]    # Dados de project
                    binary = msg.split(",")[6]    # Binary
                    dt_binary = msg.split(",")[7]    # Dados de Binary
                    passed = msg.split(",")[8]    # Passed veredicto
                    dt_passed = msg.split(",")[9]    # Dado de Passed True or False
                    tc = msg.split(",")[10]  # Test case
                    dt_tc = msg.split(",")[11]  # Descrição do TC
                    start = msg.split(",")[12]  # start Time
                    dt_start = msg.split(",")[13]  # Dado do Start Time / hora inicial
                    duration = msg.split(",")[14]  # Duration
                    dt_duration = msg.split(",")[15]  # Time of duration TC
                    modo = msg.split(",")[16]    # mode of operation
                    dt_modo = msg.split(",")[17]  # mode auto or man
                    ip = msg.split(",")[18]   #Ip address
                    Register_tc_Database(setup, dt_engtest, dt_project, dt_binary, dt_passed, dt_tc, dt_start,
                                         dt_duration, dt_modo)
                    print(" ---------------      Registrou no banco o Test Case ----------------------------")
                    self.lbl_Robo.config(bg='#ECE82E')
                    self.Text_Robo.config(state=NORMAL)
                    self.Text_Robo.insert(END, msg + '\n')
                    self.Text_Robo.insert(END, '-----------------------------------------------------------------------' + '\n')
                    self.Text_Robo.yview_scroll(1, "pages")
                    self.Text_Robo.config(state=DISABLED)

                elif s0 == ESTADO_DISP:
                    s1 = msg.split(",")[1]
                    print(" Setup avaliable ...",s1)
                    ip = msg.split(",")[2]
                    if ip == IP_ANRITSU_LTE_3_ATT :
                        self.lbl_anritsu_lte_3_att.config(bg='#6EEC78') # Tratativa do Status de conexao robo

                    elif ip == IP_ANRITSU_LTE_2_TMO :
                        self.lbl_anritsu_lte_2_tmo.config(bg='#6EEC78')

                    elif ip == IP_ANRITSU_LTE_1_ATT :
                        self.lbl_anritsu_lte_1_att.config(bg='#6EEC78')

                    elif ip == IP_ANITE_LTE_1_RIO :
                        self.lbl_anite_lte_1_rio.config(bg='#6EEC78')
                    elif ip == IP_ANITE_LTE_1_SP :
                        self.lbl_anite_lte_1_sp.config(bg='#6EEC78')
                    elif ip == IP_ANITE_3G_BSB :
                        self.lbl_anite_3g_bsb.config(bg='#6EEC78')
                    self.Text_Robo.config(state=NORMAL)
                    self.Text_Robo.insert(END, '[+]****** Samto is Conected with : ' + s1 + ',' + ip + '\n')
                    #self.Text_Robo.insert(END, '[+]****** Setup is Avaliable ' + s1 + ',' + ip + '\n')
                    #self.Text_Robo.insert(END, msg + '\n')
                    self.Text_Robo.yview_scroll(1, "pages")
                    self.Text_Robo.config(state=DISABLED)

                elif s0 == ESTADO_MANUT:
                    self.Text_Robo.config(state=NORMAL)
                    self.Text_Robo.insert(END, 'Setup below in Maintenance ...' + '\n')
                    self.Text_Robo.insert(END, msg + '\n')
                    self.Text_Robo.yview_scroll(1, "pages")
                    self.Text_Robo.config(state=DISABLED)
                    print(" Setup in Maintenance ...")
                    setup = msg.split(",")[1]  # setup
                    engtest = msg.split(",")[2]
                    start = msg.split(",")[3]
                    code = msg.split(",")[4]
                    duration = msg.split(",")[5]
                    ip = msg.split(",")[6]
                    Register_maint_Database(setup,engtest,start,code,duration)
                    print(" ---------------      Registrou no banco a Manutenção  ----------------------------")
                    if ip == IP_ANRITSU_LTE_3_ATT:
                        self.lbl_anritsu_lte_3_att.config(bg='red')   #muda a cor do label caso o robo seja desconectado
                    elif ip == IP_ANRITSU_LTE_2_TMO:
                        self.lbl_anritsu_lte_2_tmo.config(bg='red')
                    elif ip == IP_ANRITSU_LTE_1_ATT:
                        self.lbl_anritsu_lte_1_att.config(bg='red')

                elif s0 == SOCKET_DISCONECTADO:
                    s1 = msg.split(",")[1]  # IP
                    if s1 == IP_ANRITSU_LTE_3_ATT:
                        self.lbl_anritsu_lte_3_att.config(bg='#CCC9C1')   #muda a cor do label caso o robo seja desconectado
                    elif s1 == IP_ANRITSU_LTE_2_TMO:
                        self.lbl_anritsu_lte_2_tmo.config(bg='#CCC9C1')
                    elif s1 == IP_ANRITSU_LTE_1_ATT:
                        self.lbl_anritsu_lte_1_att.config(bg='#CCC9C1')
                    self.Text_Robo.config(state = NORMAL)
                    self.Text_Robo.insert(END,'Conection was lost with Robot :    ' + s1 + '\n')
                    self.Text_Robo.yview_scroll(1, "pages")
                    self.Text_Robo.config(state=DISABLED)

                elif s0 == MENSAGEM_LOG:
                    s1 = msg.split(",")[1]
                    self.Text_Robo.config(state = NORMAL)
                    self.Text_Robo.insert(END, s1 + '\n')
                    self.Text_Robo.yview_scroll(1, "pages")
                    self.Text_Robo.config(state=DISABLED)

            except queue.Empty:
                # just on general principles, although we don't expect this
                # branch to be taken in this case, ignore this exception!
                pass


class ThreadedClient(object):
    """
      Lanço o main e a worker thread. peridicCall e endApp residem na GUI
    """
    def __init__(self, master):
        """
        inicio o GUI e as Threadas assincronas . aqui é o main() que sera usada pelo GUI
        Daqui em diante outras threads serão abertas.
        .
        """

        self.master = master

        # Create the queue
        self.queue = queue.Queue()
        # Set up the GUI part
        self.gui = GuiPart(self.master, self.queue, self.startApplication, self.endApplication)

        """
            # Set up  thread para fazer  I/O assincrono
            # Outras threads podem tambem ser criadas se for o caso de expandir o projeto --> Previsão futura
            # Inicio a chamada peridica dentro da GUI  p/ checar a fila
            # self.periodicCall()
        """
    def periodicCall(self):
         # """ Check a cada 200 ms  se ha algo novo na fila. """
        self.master.after(200, self.periodicCall)
        self.gui.processIncoming()

        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            print ("passou aqui .... FIM" )
            import sys
            self.master.destroy()
            sys.exit(0)

    def workerThread1(self):

        #Aqui é onde manuseio o I/O Assincrono. faço uso da SELECT . Importante lembrar que
        #a Thread ganha o controle regularmente.

        print("Awating Robot connections .......\n")
        self.gui.Text_Robo.config(state=NORMAL)
        self.gui.Text_Robo.insert(END, " SAMTO main Worker Thread was started......." + '\n')
        self.gui.Text_Robo.insert(END, " Awating Robot connections .......\n" + '\n')
        self.gui.Text_Robo.yview_scroll(1, "pages")
        self.gui.Text_Robo.config(state=DISABLED)

        while self.running:
            print("........ Worker Thread was started .................")
            input = [self.tcpsock_g]
            inputready,outputready,exceptready = select.select(input,[],[])

            for s in inputready:
                if s == self.tcpsock_g :
                    (conn, (ip, port)) = self.tcpsock_g.accept()
                    c = recebe_msg_robo(conn, ip, port, self.queue)

                    if ip == IP_ANRITSU_LTE_3_ATT :
                        self.gui.lbl_anritsu_lte_3_att.config(bg='#6EEC78') # Tratativa do Status de conexao robo

                    elif ip == IP_ANRITSU_LTE_2_TMO :
                        self.gui.lbl_anritsu_lte_2_tmo.config(bg='#6EEC78')

                    elif ip == IP_ANRITSU_LTE_1_ATT :
                        self.gui.lbl_anritsu_lte_1_att.config(bg='#6EEC78')

                    elif ip == IP_ANITE_LTE_1_RIO :
                        self.gui.lbl_anite_lte_1_rio.config(bg='#6EEC78')
                    elif ip == IP_ANITE_LTE_1_SP :
                        self.gui.lbl_anite_lte_1_sp.config(bg='#6EEC78')
                    elif ip == IP_ANITE_3G_BSB :
                        self.gui.lbl_anite_3g_bsb.config(bg='#6EEC78')

                    c.start()
                    self.threads.append(c)
        self.tcpsock_g.close()

        for c in self.threads:
            c.join()


    def startApplication(self):

        self.running = True
        self.tcpsock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpsock_g.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpsock_g.bind((str(self.gui.HOST.get()),int(self.gui.PORT.get())))
        self.tcpsock_g.listen(10)
        self.threads = []

        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()
        self.gui.greenCircle()

        self.periodicCall()
        # pega_msgrobotino("X") # Por Default considera-se que o Robotino esta Parado e Stand by

    def endApplication(self):
        self.running = False

'''
    ------ Tratativa de Mensagens Recebidas do Robo  ------------------
    ------ Recebe as mensagens adiciona o ip do socket  e poe na fila (queue) para tratativa
    ------ nenhuma decisão é tomada aqui
'''


class recebe_msg_robo(threading.Thread):

    def __init__(self, conn, ip, port, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.ip = ip
        self.port = port
        self.conn = conn
        self.size = 1024

        print("[+] New Thread started for Robot :  "+ip+":"+str(port))

    def run(self):

        while True:
            try:
                data = self.conn.recv(self.size).decode()  # decode Adequação da String para retirar b'

            except socket.error as error:
                print("A Thread has been closed for this IP,", self.ip)
                msg = SOCKET_DISCONECTADO + "," + self.ip # Neste caso o Robo foi fechado abruptamente (ungracefull)
                self.queue.put(msg)
                return False

            if not data:
                print("Robot Lost connection with server ....", self.ip) # Neste caso o robo e desconectado normalmente n implementado
                msg2 = "" + "," + self.ip
                self.queue.put(msg2)
                break
            msg = str(data) + "," + self.ip
            self.queue.put(msg)         # Poe na Fila o valor lido do robo / recebeu normal



root = Tk()
ESTADO_ATIVO = "TESTING"
ESTADO_MANUT = "MAINTENANCE"
ESTADO_DISP = "AVALIABLE"
MENSAGEM_LOG = "LOG"
SOCKET_DISCONECTADO = ""
#IP_ANRITSU_LTE_3_ATT = '105.112.152.51'
IP_ANRITSU_LTE_3_ATT= '127.0.0.1'
IP_ANRITSU_LTE_1_ATT = '105.112.152.24'
IP_ANRITSU_LTE_2_TMO = '105.112.152.25'
IP_ANITE_LTE_1_SP = '105.112.152.14'
IP_ANITE_LTE_1_RIO = '105.112.152.10'
IP_ANITE_3G_BSB = '105.112.152.12'
IP_RS_LTE_1_PQA = '105.112.152.21'
IP_RS_LTE_2_IOT = '105.112.152.22'
IP_RS_LTE_3_IMS = '105.112.152.23'

#IP_Server = '105.112.146.197'
IP_Server = '127.0.0.1'
RegisterDataBase()
client = ThreadedClient(root)
root.mainloop()