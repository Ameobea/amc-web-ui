import os
import json

def createProject(projectName, projectLocation):	
  os.system('sh createAMCProjectTest.sh ' + projectName+ ' ' + projectLocation + ' ' + getEmptyProjectLcation())
  return

def addQuestion(texFile, projectLocation, projectName):
  os.system('sh addAQuestion.sh ' + texFile + ' ' + projectLocation + ' ' + projectName)
  return

def prepareQuestion(projectDir, questionSourceFile, pdfName):
  os.system('sh prepareQuestion.sh ' + projectDir + ' ' + questionSourceFile +' '+pdfName)
  return

def getDirFromConfig():
  config = open("config.json","r")
#  print(config.read())
  config_json = json.loads(config.read())
  config.close()
#  print(config_json['project_location'])
  return config_json['project_location']

def getSampleTexFileLocation():
  config = open("config.json","r")
  config_json = json.loads(config.read())
  config.close()
  return config_json['sample_tex_files']
  

def getEmptyProjectLcation():
  config = open("config.json","r")
  config_json = json.loads(config.read())
  config.close()
  return config_json['empty_project_location']

if __name__ == "__main__":

  createProject('pythonTest4', getDirFromConfig()+ '/')
  addQuestion(getSampleTexFileLocation() + 'simple.tex', getDirFromConfig(), 'pythonTest4')
  prepareQuestion(getDirFromConfig()+'/'+'pythonTest4', 'simple.tex', 'TheNameOfThePDF')
'''
  createProject('pythonTest4', '/home/bill/Documents/AMCScripts')
  addQuestion('/home/bill/MC-Projects/sampleQuestions/simple.tex', '/home/bill/Documents/AMCScripts/', 'pythonTest4')
  prepareQuestion('/home/bill/Documents/AMCScripts/pythonTest4', 'simple.tex')
'''

