""" Wrapper functions that interact with the `auto-multiple-choice` CLI """

from functools import partial
import subprocess
import tempfile
import os
from os import path
import shlex
from shutil import make_archive, rmtree
from typing import List


def run(args: List[str], shell=False):
    print('Running: {}'.format(' '.join(args)))
    if shell:
        # Shell-escape the string to avoid shell injection vulnerabilities
        args = '/bin/sh -c {}'.format(shlex.quote(' '.join(args)))
    subprocess.run(args, shell=shell)


def make_project_dir(temp_dir: str, paths: List[str]):
    os.mkdir(path.join(temp_dir, *paths))


def create_dummy_student_list(projectDir: str):
    students_list_path = path.join(projectDir, 'cr', 'student_names.csv')
    with open(students_list_path, mode='w') as f:
        for i in range(0, 300):
            f.write('Student {}\n'.format(i))

    return students_list_path


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
    run(['auto-multiple-choice', 'meptex', '--src', path.join(projectDir, 'DOC-calage.xy'),
         '--data', path.join(projectDir, 'data')])

def delete_project_directory(projectDir: str):
    ''' Deletes the temporary directory for the project '''

    rmtree(projectDir)

def grade_uploaded_tests(projectDir: str) -> str:
    ''' Given a project directory containing a test that has already been prepared, grades
    all tests in the `scans` subdirectory.  The resulting zooms + crops are zipped up, and
    the path to the created zipfile is returned. '''

    # Analyze tests
    run(['auto-multiple-choice', 'analyse', '--projet', projectDir,
         path.join(projectDir, 'scans', '*')], shell=True)

    # Compute grades
    run(['auto-multiple-choice', 'note', '--data', path.join(projectDir, 'data'),
         '--seuil', '0.15'], shell=True)

    # TODO: Take this as optional input from the user
    students_list_path = create_dummy_student_list(projectDir)

    # Export grades to CSV
    run(['auto-multiple-choice', 'export', '--data', path.join(projectDir, 'data'),
         '--module', 'CSV', '--fich-noms', students_list_path, '-o',
         path.join(projectDir, 'cr', 'GRADES.csv')], shell=True)

    # TODO: Look into automatic association

    # Zip up the directory containing crops and zooms and return it to the user.
    zip_path = path.join(projectDir, 'images')
    make_archive(zip_path, 'zip', path.join(projectDir, 'cr'))

    return path.join(projectDir, 'images.zip')
