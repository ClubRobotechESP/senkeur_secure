#! /usr/bin/python
#-*-coding:utf-8-*-

from socket import *
from threading import *
from time import *
from serial import *
from bdd import *

"""

AUTHOR: Abdoulaye KAMA <abdoulayekama@gmail.com>
PROJECT: senkeur_secure
DESCRIPTION: serveur principal du projet

"""

class Server:
	"""Serveur principal."""
	def __init__(self, port=20089, serial_port = "/dev/ttyACM0", host = "localhost", user="abdoulaye", pwd="kamstelecom", base = "senkeur_secure"):
		self.server_socket = socket(AF_INET, SOCK_STREAM)
		self.port = port
		self.serial_port = serial_port
		self.serial_serv = ""
		self.bdd_serv = ""
		self.running = True
		self.host = host
		self.user = user
		self.base = base
		self.pwd = pwd
		self.bdd_serv = BDD(host=self.host, base=self.base, user=self.user, pwd=self.pwd)

	def start_server(self):
		"""demarrer le serveur principal"""
		

		try:
			self.serial_serv = ThreadSerial(self.serial_port)
		except:
			self.alerte("Impossible de lire sur le port serie!")

		try:
			self.bdd_serv.connect()
		except:
			self.alerte("Impossible de se connecter à la base de données...")

		try:
				
			self.server_socket.bind(("127.0.0.1", self.port))
			self.server_socket.listen(5)

			self.running = True
			
			self.alerte("Demarrage du serveur...\nAttente de requêtes sur le port %s..." %(self.port))
			
			#while True:
			while self.running == True:
					self.server_socket.settimeout(1)
					try:
						connex, addr = self.server_socket.accept()
						ThreadClient(connex, self)
						self.alerte("nouvelle connexion : %s %s \n" %(addr))
					except error:
						a=9
				#	if self.running == False:
				#		break
			#sys.exit()
		except Exception:
			if self.running == True:
				self.alerte("La liaison du socket à l'adresse choisie a échoué!")
			else:
				self.alerte("Serveur arreté...")

		#self.server_socket.close()
		#sys.exit()

	def stop_server(self):
		try:
			if self.running == True:
				self.running = False
				self.alerte("Arret du serveur!")
				self.serial_serv.toStop()
				
			else:
				self.alerte("ERROR:Le serveur est deja arreté!")
		except:
			self.alerte("Tentative d'arret du serveur echouée!")

	def alerte(self, message, to=""):
		"""notifier un message"""
		if to == "":
			print "alerte -> ",message,"\n"


class AccessServer(Thread):
	def __init__(self, serveur):
		Thread.__init__(self)
		self.serveur = serveur
		self.start()
	def run(self):
		while self.serveur.running == True:
				connex, addr = self.serveur.server_socket.accept()
				ThreadClient(connex, self.serveur)
				self.serveur.alerte("nouvelle connexion : %s %s \n" %(addr))



class ThreadClient(Thread):
	"""Classe permettant l'envoie et la reception de donnees par socket avec une application client"""

	def __init__(self, client_socket, serveur = ""):
		Thread.__init__(self)
		self.serveur = serveur
		self.client_socket = client_socket
		self.running = True
		self.start()

	def run(self):
		while self.running == True:
			msg = self.client_socket.recv(1024)
			self.serveur.alerte("RECEIV->%s" %msg)
			self.analyse(msg)
			#if self.running == False:
				#break
			sleep(2)
			msg = self.serveur.serial_serv.recvdatas()
			if msg != "":
				self.envoie(msg)
			else:
				self.envoie("Probleme de connexion. Veuillez ressayer svp!")

		#liberation des ressources de la socket
		self.envoie("BYE")
		sleep(1)
		self.client_socket.close()

	def envoie(self, msg):
		"""envoyer un message"""
		self.client_socket.send(msg)
		self.serveur.alerte("SEND->%s" %msg)

	def analyse(self, msg):
		"""interpreteur: analyse le message recu de l'application cliente et execute la commande correpondante!
		Si le message ne correpond à aucune commande, il le notifie!"""
		
		if msg.upper() == "ADMINOFF": #allumer le serveur
			self.serveur.stop_server()

		if msg.upper() == "ADMINON": #demarrer le serveur
			self.serveur.start_server() 

		elif msg.upper() == "LAMPE 1":	#allumer les lampes
			self.serveur.serial_serv.senddatas('11')

		elif msg.upper() == "LAMPE 0": 	#eteindre les lampes
			self.serveur.serial_serv.senddatas('10')

		elif msg.upper() == "LAMPE 2": 	#statut les lampes
			self.serveur.serial_serv.senddatas('12')

		elif msg.upper() == "PORTE 1": 	#ouvrir les portes
			self.serveur.serial_serv.senddatas('21')

		elif msg.upper() == "PORTE 0": 	#fermer les portes
			self.serveur.serial_serv.senddatas('20')

		elif msg.upper() == "PORTE 2": 	#statut des portes
			self.serveur.serial_serv.senddatas('22')

		elif msg.upper() == "ALARME 0": #arreter l'arme
			self.serveur.serial_serv.senddatas('30')

		elif msg.upper() == "ALARME 1": #declecnher l'arme
			self.serveur.serial_serv.senddatas('31')

		elif msg.upper() == "PWD 1234":
			self.serveur.serial_serv.senddatas('1234')

		elif msg.upper() == "QUIT" or msg.upper() == "BYE":
			self.running = False

		else:
			self.serveur.alerte("ERROR->commande inconnue") 
			self.running = False
			


class ThreadSerial(Thread):
	"""
	Classe serial pour lire ou ecrire sur le port serie
	"""
	def __init__(self, port="/dev/ttyACM0", baudrate=9600, timetoread=1, timeout=1):
		Thread.__init__(self)
		try:
			self.sserie = Serial(port=port, baudrate=baudrate)
			self.running = True
		except Exception:
			self.running = False

		self.dataInQueeud = False
		self.timetoread = timetoread #periodicite de lecture du port
		self.datas = "" #les donnees lus
		self.dataToSend = ""  #les donneees à envoyer
		self.start() #demarrer le thread
		
	def run(self):
		"""lecture continue du port série. Lorsqu'il y'a quelque chose à lire, il lie puis envoie les donnees"""
		while self.running == True:
			while self.sserie.inWaiting() > 0:
				self.datas = self.sserie.readline()
#			sleep(self.timetoread) #pause

			if self.dataToSend != "": #envoie s'il y'a quelques a envoyer
				self.sserie.write("%s"%(self.dataToSend))
				self.sserie.flush()
				self.dataToSend = ""



	def recvdatas(self):
		"""reception des donnees"""
		if self.running == True:
			res = self.datas
			self.datas = ""
			return res
		else:
			return ""

	def senddatas(self, data = ""):
		"""envoie de donnees"""
		if self.running == True:
			self.dataToSend = data

	def toStop(self):
		"""serveur arrete"""
		if self.running == True:
			self.sserie.close()
			self.running = False


