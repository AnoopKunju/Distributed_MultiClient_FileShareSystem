#Name : Anoop Kunjumon Scariah
#ID: 1001757408
##Server Socket Reference :https://github.com/nikhilroxtomar/Multithreaded-File-Transfer-using-TCP-Socket-in-Python/blob/main/server.py
##video explanation:https://www.youtube.com/watch?v=FQ-scCeKWas
##GUI SERVER reference:https://github.com/effiongcharles/multi_user_chat_application_in_python/blob/1f1dd9211ee79dd747079d26ea450ba9fed73757/server_gui.py#L71

import socket
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox
import pickle

window = tk.Tk()                                        #GUI Window
window.title("Server GUI on File transfer")
host = socket.gethostbyname(socket.gethostname())       #FETCH IP for socket connection
port = 4800                                             #PORT for connection
FORMAT = "utf-8"                                        #format used for encode and decode
register_users = {}                                    #storing list of user active
lexi=""


with open("Lexicon/lexicon.txt","r") as f:      #reading words in lexicon
    lexi += f.read()
lexi = lexi.split(" ")

topFrame = tk.Frame(window)
lbl_title = tk.Label(topFrame, text="Welcome to FILE Transfer").pack(side= tk.LEFT)
btn_start = tk.Button(topFrame, text="Start Server", command=lambda : run_server())
btn_start.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP)

clistFrame = tk.Frame(window)
lbl_clist = tk.Label(clistFrame, text="****************** ACTIVE CLIENT LIST ****************").pack()
clscrollBar = tk.Scrollbar(clistFrame)
clscrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkclist = tk.Text(clistFrame, height=5, width=55)
tkclist.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
clscrollBar.config(command=tkclist.yview)
tkclist.config(yscrollcommand=clscrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clistFrame.pack(side=tk.TOP)

displayFrame = tk.Frame(window)
lbl_dis = tk.Label(displayFrame, text="****************** CLIENT ACTIVITY ****************").pack()
scrollBar = tk.Scrollbar(displayFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(displayFrame, height=10, width=55)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
displayFrame.pack(side=tk.TOP)

LexiFrame = tk.Frame(window)
lbl_lexi = tk.Label(LexiFrame, text="****************** LEXICON ACTIVITY ****************").pack()
lexiscrollBar = tk.Scrollbar(LexiFrame)
lexiscrollBar.pack(side=tk.RIGHT, fill=tk.Y)
lexiDisplay = tk.Text(LexiFrame, height=5, width=55)
lexiDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
lexiscrollBar.config(command=lexiDisplay.yview)
lexiDisplay.config(yscrollcommand=lexiscrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
LexiFrame.pack(side=tk.TOP)


def run_server():
    global host,port

    btn_start.config(state=tk.DISABLED)

    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.insert(tk.END, "\n[STARTED] Server is started")
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #socket connection
    server_socket.bind((host, port))                                    
    server_socket.listen()                                              
    
    tkDisplay.insert(tk.END, "\n[LISTENING] Server is listening")

    threading._start_new_thread(connection_accept, (server_socket, " "))    #starting a new thread for socket to hear so that GUI doesnot get block

def connection_accept(server_socket, m):
    while True:
        conn , address = server_socket.accept()
        thread = threading.Thread(target= handle_client, args=(conn , address)) #starting a new thread so that the active clients can be accepeted full time
        thread.start()
        
def handle_client(conn, addr):
    global lexi
    while True:
        try:
            data = conn.recv(1024).decode(FORMAT)                                   #keep listening for the data receieved from the client 
            data = data.split("@")
            cmd = data[0]
            print("in handel client ",cmd)

            if cmd == "REGISTER":                                     #registration process FLAG 
                if data[1] in register_users.keys():                   #condition for check the exisiting username
                    conn.send("DUPLICATE@Username already Taken".encode(FORMAT))
                    tkDisplay.config(state=tk.NORMAL)
                    tkDisplay.insert(tk.END, "\nUSERNAME ALREADY TAKEN REGISTRATION REJECTED")
                    break
                else:
                    register_users[data[1]] = addr[1]               #storing the username with the port as key
                    tkDisplay.config(state=tk.NORMAL)
                    tkDisplay.insert(tk.END, "\nUSER CONNECTED:" + data[1])
                    # print(",".join(list(register_users.keys())))
                    tkclist.config(state=tk.NORMAL)
                    tkclist.insert(tk.END, "\nCONNECTED USER LIST:"+ ",".join(list(register_users.keys())))
                    conn.send("ACCEPTED@USER".encode(FORMAT))

            elif cmd == "UPLOAD":                               #uploading the file to server
                name = data[1]                                  #name of the file 
                text = data[2]                                  #text of the file, send through the socket
                lexi_string=""
                
                with open("Lexicon/lexicon.txt","r") as f:      #reading words in lexicon
                    lexi_string += f.read()
                
                lexi_string = lexi_string.split(" ")

                while("" in lexi_string) :
                    lexi_string.remove("")

                for word in lexi_string:                               #condition to check if the words in lexicon exisit in file send by client
                    if word in text:
                        text = text.replace(word, "["+word+"]")

                tkDisplay.config(state=tk.NORMAL)
                tkDisplay.insert(tk.END, "\nFILE RECEIVED <<<<<")
                tkDisplay.insert(tk.END, "\nFILE CHECKED against LEXICON")
                tkDisplay.insert(tk.END, "\nFILE SEND BACK TO THE USER >>>")


                send_file = f"FETCH@{name}@{text}"
                conn.send(send_file.encode(FORMAT))             #sending back the marked file with [] on wrong words
            
            elif cmd == "CHANGE":
                if data[1]: 
                    add_word = data[1].split(" ")
                    if len(add_word):                           #if the queue is not empty
                        if set(add_word) & set(lexi):           #check for duplicates in existing lexicon
                            for w in list(set(add_word) & set(lexi)):   #removing the duplicates
                                add_word.remove(w)
                        lexi += add_word
                        # print(lexi)
                        with open("Lexicon/lexicon.txt","w") as f:
                            for w in lexi:
                                f.write(w + ' ')
                        # print(lexi)
                        with open("Lexicon/lexicon_backup.txt","w") as f:
                            for w in lexi:
                                f.write(w + ' ')
                    # print(lexi)
                    conn.send("CLEANQUEUE@".encode(FORMAT))
                    lexiDisplay.config(state=tk.NORMAL)
                    lexiDisplay.insert(tk.END, "\nAdditional words feteched from users")
                    lexiDisplay.insert(tk.END, "\nSERVER Lexicon Updated !!!!")
                
            elif cmd == "DISCONNECT":                           #condition for disconnecting the socket
                # print(register_users)
                for key,val in dict(register_users).items():    #delete the disconnected users from the dit
                    if val == addr[1]:
                        tkDisplay.config(state=tk.NORMAL)
                        tkDisplay.insert(tk.END, "\nCONNECTION DISCONNECTED BY USER:" +key)
                        del register_users[key]
                        tkclist.config(state=tk.NORMAL)
                        tkclist.insert(tk.END, "\nCONNECTED USER LIST:"+ ",".join(list(register_users.keys())))
                conn.send("DISCONNECT@".encode(FORMAT))
                conn.close()                                    #connection close
                
        except Exception as e:
            pass
    
    conn.close()
    
       

window.mainloop()                                           #run GUI
