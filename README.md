# Distributed_MultiClient_FileShareSystem
Created a Multiclient File share system using TCP/IP protocols on distributed system architecture  with Back-up server to handle fault tolerant 

Please follow the same file system <br> 
```
+-- ClientRecv
+-- ClientFiles
|   +-- clientfile.txt
|   +-- clientfile.txt
+-- Lexicon
|   +-- Lexicon.txt
+-- GUI_client.py
+-- GUIserver_socket.py
+-- BackUpServer_socket.py

```
The system has a primary server that lets multiple clients connect to it and check for existing users in the network to avoid duplicate users.
After the successful registration process user are allowed to send files over the network using socket programming. The backup server is always running to handle the connection of all the existing users over the network to carry out safe handover on the process to avoid fault and scalability.
