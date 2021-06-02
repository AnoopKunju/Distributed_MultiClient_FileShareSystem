#Name : Anoop Kunjumon Scariah
#ID: 1001757408
#GUI reference : https://github.com/effiongcharles/multi_user_chat_application_in_python/blob/1f1dd9211ee79dd747079d26ea450ba9fed73757/client_gui.py#L119
#Client Socket reference: https://github.com/nikhilroxtomar/Multithreaded-File-Transfer-using-TCP-Socket-in-Python/blob/main/client.py
#sleep logic: https://www.codegrepper.com/code-examples/python/python+loop+every+60+seconds

import tkinter as tk
from tkinter import messagebox
import threading
import os
import socket
import time

window = tk.Tk()
window.title("Client File Transfer")
username = ""
filename = ""
host = socket.gethostbyname(socket.gethostname())
port = 4800
FORMAT = "utf-8"
lexi_queue = []
lexi_string = ''
backup_flag = 0
logout_flag = 0

topFrame = tk.Frame(window)
lbl_usernm = tk.Label(topFrame, text="Enter User Name & connect:").pack(side= tk.LEFT)
ent_usernm = tk.Entry(topFrame)
ent_usernm.pack(side=tk.LEFT)
btn_register = tk.Button(topFrame, text="Register & Connect", command=lambda : connect())
btn_register.pack(side=tk.LEFT)
btn_logout = tk.Button(topFrame, text="Disconnect", command=lambda : logout())
btn_logout.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP)

displayFrame = tk.Frame(window)
lbl_dis = tk.Label(displayFrame, text="****************** MESSAGE FROM SERVER ****************").pack()
scrollBar = tk.Scrollbar(displayFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(displayFrame, height=10, width=55)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
displayFrame.pack(side=tk.TOP)

lexiFrame = tk.Frame(window)
lbl_lexi = tk.Label(lexiFrame, text="****************** ADD WORD TO LEXICON ****************").pack()
lbl_lexiword= tk.Label(lexiFrame, text="Enter Word for queue:").pack(side= tk.LEFT)
ent_lexi = tk.Entry(lexiFrame)
ent_lexi.pack(side=tk.LEFT)
btn_sendlexi = tk.Button(lexiFrame, text="Insert Word", command=lambda : insert_word())
btn_sendlexi.pack(side=tk.LEFT)
ent_lexi.config(state = tk.DISABLED)
btn_sendlexi.config(state = tk.DISABLED)
lexi_Display = tk.Text(lexiFrame, height=1, width=40)
lexi_Display.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 5))
scrollBar_lexi = tk.Scrollbar(lexiFrame)
scrollBar_lexi.pack(side=tk.RIGHT, fill=tk.Y)
scrollBar_lexi.config(command=lexi_Display.yview)
lexi_Display.config(yscrollcommand=scrollBar_lexi.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
lexiFrame.pack(side=tk.TOP,padx=(15, 0))

bottomFrame = tk.Frame(window)
lbl_fil = tk.Label(bottomFrame, text="****************** FILENAME ****************").pack()
lbl_filename= tk.Label(bottomFrame, text="Enter filename (include .txt):").pack(side= tk.LEFT)
ent_filename = tk.Entry(bottomFrame)
ent_filename.pack(side=tk.LEFT)
btn_sendfile = tk.Button(bottomFrame, text="Send File", command=lambda : send_file())
btn_sendfile.pack(side=tk.RIGHT)
ent_filename.config(state = tk.DISABLED)
btn_sendfile.config(state = tk.DISABLED)
bottomFrame.pack(side=tk.BOTTOM,padx=(15, 0))


def connect():
    global username
    if len(ent_usernm.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="Username cannot be blank")
    else:
        username = ent_usernm.get()
        connect_to_server(username)

def connect_to_server(name):
    global host,port,client_socket, backup_flag, logout_flag
    try:
        # print(host,port)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #connecting to socket
        client_socket.connect((host, port))
        
        if backup_flag == 0:
            print("in regiter logotuitb")
            cmd = "REGISTER" +"@"+ name
            client_socket.send(cmd.encode(FORMAT))
            logout_flag = 0

            ent_usernm.config(state=tk.DISABLED)
            btn_register.config(state=tk.DISABLED)
            
            ent_filename.config(state = tk.NORMAL) #text box for file name enable is enabled 
            btn_sendfile.config(state = tk.NORMAL) #button for send file enable is enabled

            ent_lexi.config(state = tk.NORMAL) #text box for adding lexicon word to queue is enbaled
            btn_sendlexi.config(state = tk.NORMAL) #button for inserting it to queu8e in enabled
        else:
            # print("befoer connect the backup")
            cmd = "CONNECTBACKUP" +"@"+ name
            client_socket.send(cmd.encode(FORMAT))

        threading._start_new_thread(receive_msg_server, (client_socket, "m")) # starting thread for receiving the data
        threading._start_new_thread(send_lexi, (client_socket, " ")) #thread to handel the sending of lexicon words
    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + host + " on port: " + str(port) + " Server may be Unavailable. Try again later")

def send_lexi(client_socket, m):
    # print("in send lexi thread")
    while True:
        try:
            time.sleep(60 - time.time()% 60)    #login to make client to wait for 60 Sec
            cmd = "CHANGE"
            send_data = f"{cmd}@{lexi_string}"
            client_socket.send(send_data.encode(FORMAT))
        except Exception as e:
            pass

def receive_msg_server(client_sck,m):
    global lexi_string, host,port,client_socket, logout_flag
    failure_flag = 0
    while True:
        try:
            data = client_sck.recv(1024).decode(FORMAT) #fetching data from server socket
            data = data.split("@")                      #spliting the data on  @
            cmd = data[0]
            if cmd == "DUPLICATE":              #codition for USERNAME TAKEN
                tk.messagebox.showerror(title="ERROR!!!", message= 'Username already Taken. Please use a different USERNAME and Register')
                ent_usernm.config(state=tk.NORMAL)
                btn_register.config(state=tk.NORMAL)
                client_sck.close()              #close the connnection
                logout_flag = 1
                break
            elif cmd == "BACKUPACCEPTED":
                tkDisplay.config(state=tk.NORMAL)
                tkDisplay.insert(tk.END, "\nCONNECTION SUCCESSFULL ON BACKUP SERVER")
            elif cmd == "ACCEPTED":             #condition for REGISTRATION done
                tkDisplay.config(state=tk.NORMAL)
                tkDisplay.insert(tk.END, "\nCONNECTION SUCCESSFULL")
            elif cmd =="FETCH":                 #FEtching the file from server
                name, text = data[1], data[2]
                filepath = os.path.join("ClientRecv", name)
                with open(filepath, "w") as f:
                    f.write(text)
                tkDisplay.config(state=tk.NORMAL)
                tkDisplay.insert(tk.END, "\nFILE IS BEEN RECEIVED CHECK [ClientRecv] FOLDER <<<<")
            elif cmd == "CLEANQUEUE":
                lexi_string = ''
                lexi_Display.delete("1.0","end")
                lexi_Display.insert(tk.END, "Server fetech done-- Queue cleared")
            elif cmd == "DISCONNECT":
                failure_flag = 1
                client_socket.close()
        except Exception as e: #look for main server failure
            if logout_flag == 0 and failure_flag == 0:
                tk.messagebox.showerror(title="ERROR!!!", message="Server may be Unavailable at" + host + " on port: " + str(port) + "Connecting to backup server")
                break
            else:
                pass

    if logout_flag == 0: #check if the disconnection is due to logout or not
        connect_backup_server()
    
def connect_backup_server():
    global host,port,client_socket, username, backup_flag
    backup_flag = 1
    logout_flag = 0
    host = socket.gethostbyname(socket.gethostname())
    port = 4500
    # print(username)
    connect_to_server(username) #connect to the backup server

def send_file():
    global filename, client_socket
    if len(ent_filename.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="Filename cannot be blank")
    else:
        filename = ent_filename.get()
    
    path = "ClientFiles/" + filename
    
    with open(f"{path}","r") as f:          #sending file over the socket
        text = f.read()
    filename = path.split("/")[-1]
    cmd = "UPLOAD"
    send_data = f"{cmd}@{filename}@{text}"
    
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.insert(tk.END, "\nFILE SEND TO SERVER SUCCESSFULL >>>>>")
    
    client_socket.send(send_data.encode(FORMAT))       #socket send the file 

def insert_word():
    global client_socket, lexi_string
    
    if len(ent_lexi.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="word cannot be blank")
    else:
        lexi_word = ent_lexi.get()      #fetching word from GUI
        ent_lexi.delete(0,"end") 
        if not lexi_string:             # to check if queue is not emptpy
            lexi_string = lexi_word
        else:
            lexi_string +=" "+ lexi_word

        lexi_Display.config(state=tk.NORMAL)
        if len(lexi_string) > 1:
            lexi_Display.delete("1.0","end")

        lexi_Display.insert(tk.END, "Updated Queue:"+ str(list(lexi_string.split(" "))))
        
def logout():
    global client_socket, logout_flag 
    client_socket.send("DISCONNECT@".encode(FORMAT))        #disconnect from the socket
    # client_socket.close()
    print("before logo",logout_flag)
    logout_flag = 1
    print("After logo",logout_flag)
    ent_usernm.config(state=tk.NORMAL)
    btn_register.config(state=tk.NORMAL)
    tkDisplay.insert(tk.END, "\nCONNECTION DISCONNECTED SUCCESSFULLY")
    ent_filename.config(state = tk.DISABLED)
    btn_sendfile.config(state = tk.DISABLED)
    ent_lexi.config(state = tk.DISABLED)
    btn_sendlexi.config(state = tk.DISABLED)

    

window.mainloop()
