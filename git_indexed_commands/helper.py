# -*- coding: utf-8 -*-
import os
import subprocess


def index_files(porcelain_output):
    ''' builds list of files for indexing use'''
    return [fpath[2:].strip() for fpath in porcelain_output if fpath[2:].strip() != '##']


def classify_files(porcelain_output):
    ''' builds a dictionary with text for git status output '''
    files_index = index_files(porcelain_output)
    status = {
        'branch': {
            'current': '',
            'remote': '',
            'status': '',
        },
        'staged': {
            'tracked': '',
            'deleted': ''
        },
        'unstaged': {
            'tracked': '',
            'untracked': '',
            'deleted': ''
        },
        'unrecognized': '',
    }
    for fpath in porcelain_output:
        if fpath.startswith(' M'):
            status['unstaged']['tracked'] += '[{}] modified: {}'.format(files_index.index(fpath.split(' ')[2].strip()), fpath.split(' ')[2])
        elif fpath.startswith('M '):
            status['staged']['tracked'] += '[{}] modified: {}'.format(files_index.index(fpath.split(' ')[2].strip()), fpath.split(' ')[2])
        elif fpath.startswith('MM'):
            status['staged']['tracked'] += '[{}] modified: {}'.format(files_index.index(fpath.split(' ')[1].strip()), fpath.split(' ')[1])
            status['unstaged']['tracked'] += '[{}] modified: {}'.format(files_index.index(fpath.split(' ')[1].strip()), fpath.split(' ')[1])
        elif fpath.startswith(' D'):
            status['unstaged']['deleted'] += '[{}] deleted: {}'.format(files_index.index(fpath.split(' ')[2].strip()), fpath.split(' ')[2])
        elif fpath.startswith('D '):
            status['staged']['deleted'] += '[{}] deleted: {}'.format(files_index.index(fpath.split(' ')[2].strip()), fpath.split(' ')[2])
        elif fpath.startswith('??'):
            status['unstaged']['untracked'] += '[{}] {}'.format(files_index.index(fpath.split(' ')[1].strip()), fpath.split(' ')[1])
        elif fpath.startswith('A '):
            status['staged']['tracked'] += '[{}] new file: {}'.format(files_index.index(fpath.split(' ')[2].strip()), fpath.split(' ')[2])
        elif fpath.startswith('AM'):
            status['staged']['tracked'] += '[{}] new file: {}'.format(files_index.index(fpath.split(' ')[1].strip()), fpath.split(' ')[1])
            status['unstaged']['tracked'] += '[{}] modified: {}'.format(files_index.index(fpath.split(' ')[1].strip()), fpath.split(' ')[1])
        elif fpath.startswith('##'):
            pass
            # double hash tags branch information when porcelain is run with -b
            # need to add branch processing here, format is ## current...tracking [status:ahead1/behind2]
        else:
            status['unrecognized'] += '[{}] unrecognized: {}'.format(fpath)
    return status


def build_status_text(porcelain_output):
    ''' combines files classification with git status text templates '''
    status_dict = classify_files(porcelain_output)
    status_text = ''
    templates_path = os.path.join(os.path.dirname(__file__), 'templates')
    if status_dict['staged']['tracked'] or status_dict['staged']['deleted']:
        with open('{}/staged.txt'.format(templates_path)) as staged:
            status_text += staged.read().format(**status_dict)
    if status_dict['unstaged']['tracked'] or status_dict['unstaged']['deleted']:
        with open('{}/unstaged.txt'.format(templates_path)) as unstaged:
            status_text += unstaged.read().format(**status_dict)
    if status_dict['unstaged']['untracked']:
        with open('{}/untracked.txt'.format(templates_path)) as untracked:
            status_text += untracked.read().format(**status_dict)
    if status_dict['unrecognized']:
        with open('{}/unrecognized.txt'.format(templates_path)) as unrecognized:
            status_text += unrecognized.read().format(**status_dict)
    return status_text


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


def get_diff(fpath):
    '''
        Runs git diff for a file and proxies the stdout, just an index wrapper
    '''
    return subprocess.Popen(['git', 'diff {}'.format(fpath),], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
