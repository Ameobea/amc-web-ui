from functools import partial
import tempfile
import os
from os import path
import json
from typing import List

def make_project_dir(temp_dir: str, paths: List[str]):
  os.mkdir(path.join(temp_dir, *paths))

def createProject(project_name: str):
  """ Creates a new project in a temporary directory and returns the path to the
  created directory. """

  temp_dir = tempfile.mkdtemp()

  # Set up the directory with the AMC project structure
  create_dir = partial(make_project_dir, temp_dir)
  create_dir([project_name])

  def create_inner_dir(dirs): return make_project_dir(
      temp_dir, [project_name, *dirs])
  create_inner_dir(['cr'])
  create_inner_dir(['cr', 'corrections'])
  create_inner_dir(['cr', 'corrections', 'jpg'])
  create_inner_dir(['cr', 'corrections', 'pdf'])
  create_inner_dir(['cr', 'diagnostic'])
  create_inner_dir(['cr', 'zooms'])
  create_inner_dir(['data'])
  create_inner_dir(['exports'])
  create_inner_dir(['scans'])
  create_inner_dir(['copies'])

  return temp_dir

def addQuestion(texFile, projectLocation, projectName):
  os.system('sh addAQuestion.sh ' + texFile + ' ' + projectLocation + ' ' + projectName)

def prepareQuestion(projectDir, questionSourceFile, pdfName):
  os.system('sh prepareQuestion.sh ' + projectDir + ' ' + questionSourceFile + ' ' + pdfName)

def getEmptyProjectLcation():
  config = open("config.json","r")
  config_json = json.loads(config.read())
  config.close()
  return config_json['empty_project_location']

if __name__ == "__main__":
  project_name = 'pythonTest4'
  project_dir = createProject(project_name)
  addQuestion('simple.tex', project_dir, project_name)
  prepareQuestion(project_dir, project_name, 'simple.tex', 'TheNameOfThePDF')

'''
  createProject('pythonTest4', '/home/bill/Documents/AMCScripts')
  addQuestion('/home/bill/MC-Projects/sampleQuestions/simple.tex', '/home/bill/Documents/AMCScripts/', 'pythonTest4')
  prepareQuestion('/home/bill/Documents/AMCScripts/pythonTest4', 'simple.tex')
'''

