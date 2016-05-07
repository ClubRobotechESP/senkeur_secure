#! /usr/bin/python
#-*- coding:utf-8 -*-

import threading, socket, sys

class Client:
	def __init__(self, server='127.0.0.1', port=20089):
		self.status="horsline"
		self.addr=server
		self.port=port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


	def start(self):
		try:
			print "connexion au serveur %s..." %(self.port)
			self.sock.connect((self.addr, self.port))
			ClientReceiver(self.sock)
			while True:
				msg = raw_input("")
				self.sock.send(msg)
				if msg == '' or msg.upper() == "QUIT":
					break
		except socket.error:
			print "La liaison du socket à l'adresse choisie a échoué."
		sys.exit()
		
	#def envoie(self, msg):

class ClientReceiver(threading.Thread):
	def __init__(self, sock):
		threading.Thread.__init__(self)
		self.sock = sock
		self.start()
	def run(self):
		while True:
			msg = self.sock.recv(1024)
			print "serveur>:", msg
			if msg == '' or msg.upper() == "QUIT" or msg.upper() == "BYE":
				break
		
		self.sock.close()

if __name__=="__main__":
	cl = Client()
	cl.start()