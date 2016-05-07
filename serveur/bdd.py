#! /usr/bin/python
#-*-coding:utf-8-*-

import mysql.connector

class BDD():
	"""acces à la base de données"""
	def __init__(self, host, base, user, pwd):
		""""""
		self.host = host
		self.base = base
		self.user = user
		self.pwd = pwd
		self.running = False

	def connect(self):
		"""connexion à la base de données"""
		try:
			self.conn = mysql.connector.connect(host=self.host, user=self.user, password=self.pwd, database=self.base)
			self.cursor = self.conn.cursor()
			self.running = True

		except Exception:
			self.running = False

	def insert_journal(self, msg, typ):
		"""inserer un truc dans la base de données"""
		if self.running == True:
			req = "INSERT INTO journal(motif, type_journal) VALUES(%s,%s)" %(msg, typ)
			self.cursor.execute(req)

	def select_journal(self):
		"""requete de type select dans la base de donnees"""
		if self.running == True:
			req = "SELECT * FROM journal"
			self.cursor.execute(req)
			return self.cursor.fetchall()
		else:
			return []

	def close(self):
		if self.running == True:
			self.running = False
			self.cursor.close()