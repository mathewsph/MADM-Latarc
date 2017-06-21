import socket
import ast
import time
import os

HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 15000            # Porta que o Servidor esta
#a = open("host_data.txt","r")
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)
print 'Para sair use CTRL+X\n'
#msg = a.read()
while True:
    a = open("host_data.txt","r")
    msg = a.read()
#    if msg[0] != "(":
    msg = msg.replace("BSSID:","")
    msg = msg.replace("SA:","")
    msg_split = msg.split()
    try:
      cmd = os.popen("ifconfig|grep " + msg_split[1]+"|cut -d ' ' -f1 ")
      scan = open(msg_split[3] + "_scan.txt","r")
      scan = scan.read()
      cmd = cmd.read()
      msg = msg + cmd
      msg = msg.replace('\n',' ')
      msg = msg + '\n' + scan
      print msg
#      print scan
      tcp.send (msg)
      time.sleep(1)
      response = tcp.recv(1024)
      response_archive = open("response.txt","w")
      response_archive.write(response)
      response_archive.close()
      print response
    except IndexError:
       cmd = ' '
       msg = msg
       print msg
       tcp.send (msg)
       time.sleep(1)
tcp.close()
