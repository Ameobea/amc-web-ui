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
    ''' Runs the provided command in the system.  The command should be split at spaces and
    provided as a list of individual words.

    If `shell` is set to `True`, the command will be executed using `sh -c {command}` and
    escaped for the shell. '''

    print('Running: {}'.format(' '.join(args)))
    if shell:
        # Shell-escape the string to avoid shell injection vulnerabilities
        args = '/bin/sh -c {}'.format(shlex.quote(' '.join(args)))
    subprocess.run(args, shell=shell)


def make_project_dir(temp_dir: str, paths: List[str]):
    os.mkdir(path.join(temp_dir, *paths))


def create_dummy_student_list(project_dir: str):
    ''' Creates a CSV file in the provided project directory containing a dummy list of student
    names.  AMC's `note` command requires a CSV file like this, so we generate this one if
    the user doesn't provide a student list of their own. '''

    students_list_path = path.join(project_dir, 'cr', 'student_names.csv')
    with open(students_list_path, mode='w') as student_list_file:
        for i in range(0, 300):
            student_list_file.write('Student {}\n'.format(i))

    return students_list_path


def create_project(project_name: str):
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


def prepare_question(project_dir, tex_file_path):
    ''' Given a project directory set up with the correct directory structure for AMC and a TeX
    file containing the quiz to be generated, generates the quiz and extracts layout information
    that can later be used for grading. '''

    # Run the AMC command line to create the subject, correction, and position files
    run(['auto-multiple-choice', 'prepare', '--mode', 's', '--prefix', project_dir,
         tex_file_path, '--out-sujet', 'DOC-subject.pdf', '--out-corrige', 'DOC-correction.pdf',
         '--out-calage', 'DOC-calage.xy'])

    # Extract the scoring data from the source file
    run(['auto-multiple-choice', 'prepare', '--mode', 'b',
         '--prefix', project_dir, tex_file_path, '--data', './data/'])

    # Add data from each working document to the layout database
    run(['auto-multiple-choice', 'meptex', '--src', path.join(project_dir, 'DOC-calage.xy'),
         '--data', path.join(project_dir, 'data')])

def delete_project_directory(project_dir: str):
    ''' Deletes the temporary directory for the project '''

    rmtree(project_dir)

def grade_uploaded_tests(project_dir: str) -> str:
    ''' Given a project directory containing a test that has already been prepared, grades all
    tests in the `scans` subdirectory.  The resulting zooms + crops are zipped up, and the path to
    the created zipfile is returned. '''

    # Analyze tests
    run(['auto-multiple-choice', 'analyse', '--projet', project_dir,
         path.join(project_dir, 'scans', '*')], shell=True)

    # Compute grades
    run(['auto-multiple-choice', 'note', '--data', path.join(project_dir, 'data'),
         '--seuil', '0.15'], shell=True)

    # TODO: Take this as optional input from the user
    students_list_path = create_dummy_student_list(project_dir)

    # Export grades to CSV
    run(['auto-multiple-choice', 'export', '--data', path.join(project_dir, 'data'),
         '--module', 'CSV', '--fich-noms', students_list_path, '-o',
         path.join(project_dir, 'cr', 'GRADES.csv')], shell=True)

    # TODO: Look into automatic association

    # Zip up the directory containing crops and zooms and return it to the user.
    zip_path = path.join(project_dir, 'images')
    make_archive(zip_path, 'zip', path.join(project_dir, 'cr'))

    return path.join(project_dir, 'images.zip')
