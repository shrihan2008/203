import socket
from threading import Thread
from tkinter import *

nickname=input("Choose your nickname ")

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_adress="127.0.0.1"
port=5000
client.connect((ip_adress,port))

print("Connected to server")

class GUI:
    def __init__(self):
        self.Window=Tk()
        self.Window.withdraw()
        self.login=Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False,height=False)
        self.login.configure(width=400,height=400)
        self.pls=Label(self.login,
                            text="Login to continue",
                            justify=CENTER,
                            font="arial"
                            )
        self.pls.place(relheight=0.15,relx=0.2,rely=0.07)
        self.labelName=Label(self.login,text="Name = ",font="arial 12")
        self.labelName.place(relheight=0.2,relx=0.1,rely=0.2)


        self.entryName=Entry(self.login,font=12)
        self.entryName.place(relheight=0.12,relwidth=0.4,relx=0.35,rely=0.2)
        self.entryName.focus()
        self.go=Button(self.login,
                            text="continue",font="arial 12",command=lambda : self.goahead(self.entryName.get()))
        self.go.place(relx=0.4,rely=0.55)


        self.Window.mainloop()



    def goahead(self,name):
        self.login.destroy()
        self.name=name
        rcv=Thread(target=self.receive)
        rcv.start()
        

    def layout(self,name):
        self.name=name
        self.Window.deiconify()
        self.Window.title("Chat Room")
        self.Window.resizable(width=False,height=False)
        self.Window.configure(width=470,height=550,bg="grey")
        self.labelHead=Label(self.Window,bg="grey",text=self.name,font=("helvetica",15), pady=5,fg="orange")
        self.labelHead.place(relwidth=1,relheight=2)
        self.line=Label(self.Window,width=450,bg="grey")
        self.line.place(relwidth=1,relheight=0.012)
        self.textcons=Text(self.Window,width=20,height=2,bg="grey",fg="orange",font=("helvetica",12) ,padx=5 ,pady=5)
        self.textcons.place(relheight=0.745,relwidth=1,rely=0.08)

        self.labelBottom=Label(self.Window,bg="orange",fg="grey",height=80)
        self.labelBottom.place(relwidth=1,rely=0.825)
        self.entryMessage=Entry(self.labelBottom,bg="grey",fg="orange",font=("helvetica",12))
        self.entryMessage.place(relwidth=0.74,relheight=0.06,rely=0.008,relx=0.011)
        self.entryMessage.focus()

        selfButtonMessage=Button(self.labelBottom,text="Send",font=("helvetica",12) ,width=20,bg="green",command=lambda:self.sendButton(self.entryMessage.get))
        selfButtonMessage.place(relx=0.77,rely=0.008,relheight=0.06,relwidth=0.22)

        self.textcons.config(cursor="Arrow")
        scrollbar=Scrollbar(self.textcons)
        scrollbar.place(relheight=1,relx=0.974)
        scrollbar.config(command=self.textcons.yview)

        self.textcons.config(state=DISABLED)

    def sendButton(self,msg):
        self.textcons.config(state=DISABLED)
        self.msg=msg
        self.entryMessage.delete(0,END)
        snd=Thread(target=self.write)
        snd.start()


    def showMessage(self,msg):
        self.textcons.config(state=NORMAL)
        self.textcons.insert(END,msg+"\n\n")
        self.textcons.config(state=DISABLED)
        self.textcons.see(END)

    def receive(self):
          while True:
            try:
                message=client.recv(2048).decode("utf-8")
                if message=="NICKNAME":
                    client.send(nickname.encode("utf-8"))
                else:
                    self.showMessage(message)
            
            except:
                    print("ERRROROROR FOUND")
                    client.close()
                    break
                
    def write(self):
        self.textcons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode("utf-8"))
            self.showMessage(message)
            break

                




g=GUI()
        
        

