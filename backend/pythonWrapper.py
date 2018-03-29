""" Wrapper functions that interact with the `auto-multiple-choice` CLI """

from functools import partial
from subprocess import run
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

    def create_inner_dir(dirs):
        merged = [project_name] + dirs
        return make_project_dir(temp_dir, merged)

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

    return path.join(temp_dir, project_name)


def prepareQuestion(projectDir, tex_file_path, pdfName):
    # Run the AMC command line to create the subject, correction, and position files
    run(['auto-multiple-choice', 'prepare', '--mode', 's', '--prefix', projectDir,
         tex_file_path, '--out-sujet', 'DOC-subject.pdf', '--out-corrige', 'DOC-correction.pdf',
         '--out-calage', 'DOC-calage.xy'])

    # Extract the scoring data from the source file
    run(['auto-multiple-choice', 'prepare', '--mode', 'b',
         '--prefix', projectDir, tex_file_path, '--data', './data/'])

    # Add data from each working document to the layout database
    run(['auto-multiple-choice', 'meptex', '--src', path.join(projectDir, '$1', 'DOC-calage.xy'),
        '--data', path.join(projectDir, '$1', 'data')])

if __name__ == "__main__":
    project_name = 'pythonTest4'
    project_dir = createProject(project_name)
    addQuestion('simple.tex', project_dir, project_name)
    prepareQuestion(project_dir, project_name, 'simple.tex', 'TheNameOfThePDF')
