# -*- coding: utf-8 -*-
import subprocess

from .helper import build_status_text, index_files


'''
    index_files(porcelain_output):
        returns list of files
    classify_status_files(porcelain_output):
        returns dictionary which can populate status text
    build_status_text(index_files, status_dict):
        takes the dict and checks certain sections and populates
        status text templates and adds how file is indexed in the list
'''


def get_indexed_files():
    ''' runs git status --porcelain and forwards its output '''
    p = subprocess.Popen(['git', 'status', '--porcelain'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return index_files(p.stdout.readlines())


def get_status():
    ''' runs git status --porcelain and forwards its output '''
    p = subprocess.Popen(['git', 'status', '--porcelain'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return build_status_text(p.stdout.readlines())


def get_branches(args):
    '''
        Runs git branch and extracts local branches list by the command, returns tuple
        with current branch and list of branches
    '''
    if args:
        p = subprocess.Popen(['git', 'branch',]+args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        p = subprocess.Popen(['git', 'branch',]+args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    a = p.stdout.readlines()
    current, branches = None, []
    for line in a:
        if line.startswith('*'):
            current = line.split('*')[1].strip()
        else:
            branches.append(line.strip())
    return current.strip(), branches
