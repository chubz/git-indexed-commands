# -*- coding: utf-8 -*-
import argparse
import subprocess

from git_indexed_commands import util


def git_istatus(args):
    if args.short:
        for i, fpath in enumerate(util.get_indexed_files()):
            print '{} {}'.format(i, fpath)
    else:
        print util.get_status()


def git_istatus_main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        '--short',
        action='store_true',
        help='get simple indexed output'
    )
    args = parser.parse_args()
    git_istatus(args)


def git_iadd(args):
    files = util.get_indexed_files()
    if args.index[0] == '.':
        subprocess.Popen(['git', 'add', '.'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print 'added: {}'.format(files)
    else:
        for i in args.index:
            try:
                subprocess.Popen(['git', 'add', files[int(i)]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print 'added: {}'.format(files[int(i)])
            except TypeError:
                print 'Oh fishy fishy fish ...'


def git_iadd_main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'index',
        metavar='I',
        nargs='+',
        help='an zero index of file to add or adding all with .',
        choices=[str(i) for i in range(0, len(util.get_indexed_files()))]+['.']
    )
    args = parser.parse_args()
    git_iadd(args)


def git_icheckout(args):
    files = util.get_indexed_files()
    for i in args.index:
        try:
            subprocess.Popen(['git', 'checkout', files[int(i)]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print 'checking out file: {}'.format(files[int(i)])
        except TypeError:
            print 'cannot support this '


def git_icheckout_main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'index',
        metavar='i',
        nargs='+',
        type=int,
        help='an zero index of file to add',
        choices=[i for i in range(0, len(util.get_indexed_files()))]
    )
    args = parser.parse_args()
    git_icheckout(args)


def git_idiff(args):
    files = util.get_indexed_files()
    for i in args.index:
        try:
            p = subprocess.Popen(['git', 'diff', files[int(i)]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print p.stdout.read()
        except TypeError:
            print 'Oh fishy fishy fish ...'


def git_idiff_main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'index',
        metavar='I',
        nargs='+',
        help='an zero index of file to add or all',
        choices=[str(i) for i in range(0, len(util.get_indexed_files()))]+['.']
    )
    args = parser.parse_args()
    git_idiff(args)
