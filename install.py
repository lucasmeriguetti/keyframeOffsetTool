import os
import maya.mel as mel
import maya.cmds as cmds

def onMayaDroppedPythonFile(*args):
	Install()

class Install(object):
	def __init__(self, modVersion = 1.0, scripts = True):
		self.mayaPath = None 
		self.currDirPath = None
		self.modulesPath = None
		self.modName = None
		self.modVersion = modVersion
		self.scripts = scripts

		self.getMayaRootPath()
		self.getCurrentDirectoryPath()
		self.createModulesFolder()
		self.writeModuleFile()

	def writeModuleFile(self):
		#check for modules folder 
		currDirPathInvertSlash = self.currDirPath.replace("\\", "/")

		modString = "+ {} {} {}".format(self.modName, self.modVersion, currDirPathInvertSlash)
		
		if self.scripts:
			modString = "{}\nscripts: {}".format(modString, currDirPathInvertSlash)

		filePath = os.path.join(self.modulesPath, "{}.mod".format(self.modName))
		with open(filePath, "w") as f:
			f.write(modString)

		print(filePath)

	def createModulesFolder(self):
		self.modulesPath = os.path.join(self.mayaPath, "modules")
		if os.path.exists(self.modulesPath):
			print("Modules folder exists.")
			return

		print("Creating Modules folder")
		os.makedirs(self.modulesPath)

	def getMayaRootPath(self):
		paths = mel.eval("getenv MAYA_APP_DIR;").split("/")
		self.mayaPath = os.path.join(paths[0], os.sep, *paths[1:])

	def getCurrentDirectoryPath(self):
		paths = os.path.dirname(os.path.realpath(__file__)).split("\\")
		self.modName = paths[-1]
		self.currDirPath = os.path.join(paths[0], os.sep, *paths[1:])



