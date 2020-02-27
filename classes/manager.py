import os
import sys



class MANAGER():
	def __init__(self):
		self.file = None
		self.folder = None

	def setFolder(self, folder):
		self.folder = folder
		self.file = None

	def chooseFile(self, name):
		self.file = name

	def readFolder(self):
		try:
			return os.listdir(self.folder)
		except Exception as e:
			return e

	def readFile(self):
		try:
			file = open(self.folder + self.file, 'r')
			return file.readlines()
		except Exception as e:
			return e