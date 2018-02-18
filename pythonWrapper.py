import os

def createProject(projectName, projectLocation):	
  os.system('./createAMCProjectTest.sh ' + projectName+ ' ' + projectLocation)
  return

def addQuestion(texFile, projectLocation, projectName):
  os.system('./addAQuestion.sh ' + texFile + ' ' + projectLocation + ' ' + projectName)
  return

def prepareQuestion(projectDir, questionSourceFile):
  os.system('./prepareQuestion.sh ' + projectDir + ' ' + questionSourceFile)
  return

if __name__ == "__main__":
  createProject('pythonTest4', '/home/bill/Documents/AMCScripts')
  addQuestion('/home/bill/MC-Projects/sampleQuestions/simple.tex', '/home/bill/Documents/AMCScripts/', 'pythonTest4')
  prepareQuestion('/home/bill/Documents/AMCScripts/pythonTest4', 'simple.tex')
