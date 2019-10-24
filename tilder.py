#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""NAME
    tilder - Back up files into respective subdirectories

SYNOPSIS
    python tilder.py [file ...]
                     [-tstamp=key] [-tstamp_pos=front|rear]
                     [-nofm] [-nopause]

DESCRIPTION
    By emulating baker, the author's Perl program,
    this Python program facilitates backing up files.
    The main difference between the two programs is
    the method of naming subdirectories:
    - tilder (Python 3) ... subdirs are suffixed by the tilde (~)
    - baker (Perl 5)    ... subdirs are prefixed by 'bak_'

OPTIONS
    -tstamp=key (short term: -ts)
        d (default)
            Timestamp up to yyyymmdd
        dt
            Timestamp up to yyyymmdd_hhmm
        none
            No timestamp

    -tstamp_pos=front|rear (short term: -pos, default: rear)

    -nofm
        The front matter will not be displayed at the beginning of the program.

    -nopause
        The shell will not be paused at the end of the program.
        Use it for a batch run.

EXAMPLES
    python tilder.pl oliver.eps heaviside.dat -nopause
    python tilder.pl bateman.ps -tstamp=d
    python tilder.pl harry_bateman.ps -ts=none

REQUIREMENTS
    Python 3 (>v3.6)

AUTHOR
    Jaewoong Jang <jangj@korea.ac.kr>

COPYRIGHT
    Copyright (c) 2018-2019 Jaewoong Jang

LICENSE
    This software is available under the MIT license;
    the license information is found in 'LICENSE'.
"""


#
# Imports
#
import sys
from os import mkdir
from os.path import isdir, exists
import re
from shutil import copyfile
from datetime import datetime


#
# Function definitions
#
def parse_argv(cmd_opts, run_opts):
    """Program arguments parser"""
    
    for arg in list(sys.argv[1:]):
        # Files to be backed up
        if exists(arg) and not isdir(arg):
            run_opts['backup_fnames'].append(arg)
        
        # Timestamp level
        if re.search(cmd_opts['tstamp'], arg):
            run_opts['tstamp'] = re.sub(cmd_opts['tstamp'], '', arg)
        
        # Timestamp position
        if re.search(cmd_opts['tstamp_pos'], arg):
            run_opts['tstamp_pos'] = re.sub(cmd_opts['tstamp_pos'], '', arg)
        
        # The front matter won't be displayed at the beginning of the program.
        if re.search(cmd_opts['nofm'], arg):
            run_opts['is_nofm'] = 1
        
        # The shell won't be paused at the end of the program.
        if re.search(cmd_opts['nopause'], arg):
            run_opts['is_nopause'] = 1


def show_front_matter(*args):
    """Display the front matter."""
    
    prog_info = args[0]
    
    # Determine which fields to print.
    (is_prog, is_auth) = '', ''
    for arg in list(args[1:]):
        if arg == 'prog':
            is_prog = 1
        if arg == 'auth':
            is_auth = 1
    
    # Top rule
    if is_prog == 1 or is_auth == 1:
        print("+" * 70)
    
    # Program info, except the usage
    if is_prog == 1:
        print(
            prog_info['titl'],
            "-",
            prog_info['expl'],
        )
        print(
            prog_info['titl'],
            prog_info['vers'],
            "(%s)" % prog_info['date_last'],
        )
    
    # Author info
    if is_auth == 1:
        if is_prog == 1:
            print("")
        for v in prog_info['auth'].values():
            print(v)
    
    # Bottom rule
    if is_prog == 1 or is_auth == 1:
        print("+" * 70)


def pause_shell():
    """Pause the shell."""
    
    input("Press enter to exit...")


def tilder(run_opts):
    """Back up the designated files."""
    
    # Generate a timestamp.
    _ymd = datetime.today().strftime("%Y%m%d")
    _hms = datetime.today().strftime("%H%M%S") # Capital: zero-padded
    _hm = datetime.today().strftime("%H%M")
    tstamp_sep = '_'
    datetimes = {
        'none': '', # Used for timestamp suppressing
        'ymd': _ymd,
        'hms': _hms,
        'hm': _hm,
        'ymdhms': _ymd + tstamp_sep + _hms,
        'ymdhm': _ymd + tstamp_sep + _hm,
    }
    tstamp_of_int = datetimes['ymd']
    if re.search(r'(?i)\bdt\b', run_opts['tstamp']):
        tstamp_of_int = datetimes['ymdhm']
    if re.search(r'(?i)\bnone\b', run_opts['tstamp']):
        tstamp_of_int = ''
    
    # Filename elements
    fname_old_and_new = {}
    lengthiest = ''
    path_delim = '\\' if re.search(r'(?i)win32', sys.platform) else '/'
    path_of_int = '.'
    backup_flag = '~'
    fname_re = re.compile(r'(.*)([.]\w+)$')
    
    # Construct pairs of old and new filenames.
    for fname_old in run_opts['backup_fnames']:
        # Find the lengthiest filename to construct a conversion.
        if len(fname_old) > len(lengthiest):
            lengthiest = fname_old
        
        # Dissociate a filename and define a backup filename.
        bname = re.sub(fname_re, r'\1', fname_old)
        ext = re.sub(fname_re, r'\2', fname_old)
        fname_sep = '_' if tstamp_of_int else ''
        if re.search(r'(?i)front', run_opts['tstamp_pos']):
            fname_new = tstamp_of_int + fname_sep + bname
        elif re.search(r'(?i)rear', run_opts['tstamp_pos']):
            fname_new = bname + fname_sep + tstamp_of_int
        if not ext == fname_old: # For extensionless filenames
            fname_new = fname_new + ext
        
        # Buffer the old and new filenames as key-val pairs.
        subdir = path_of_int + path_delim + fname_old + backup_flag
        fname_old_and_new[fname_old] = [
            subdir,
            subdir + path_delim + fname_new,
        ]
    
    # Back up the designated files following notification.
    if fname_old_and_new:
        print("-" * 70)
        conv = '%-' + str(len(lengthiest)) + 's'
        for k, v in fname_old_and_new.items():
            # Vertically-aligned printing:
            # Use Ruby-like str interpolation to expand
            # a conversion beforehand, and use the conventional
            # (plus, old school) Python str formatting.
            print(f"{conv} => %s" % (k, v[1]))
            if not exists(v[0]):
                mkdir(v[0])
            copyfile(k, v[1])
        print("-" * 70)
    if fname_old_and_new:
        print("Backing up completed.", end=' ')
    if not fname_old_and_new:
        print(
            "\n"
            + "-" * 70
            + "\n> None of the designated files found in"
            + " [{}{}].\n".format(path_of_int, path_delim)
            + "> Type 'python tilder.py' to check its man page.\n"
            + "-" * 70
        )


def outer_tilder():
    """tilder running routine"""
    
    if len(sys.argv) >= 2:
        prog_info = {
            'titl': 'tilder',
            'expl': 'Back up files into respective subdirectories',
            'vers': 'v1.02',
            'date_last': '2019-10-24',
            'date_first': '2018-06-23',
            'auth': {
                'auth': 'Jaewoong Jang',
#                'posi': '',
#                'affi': '',
                'mail': 'jangj@korea.ac.kr',
            },
        }
        cmd_opts = { # Command-line opts
            'tstamp': re.compile(r'(?i)-?-(?:t(?:ime)?stamp|ts|dt)\s*=\s*'),
            'tstamp_pos': re.compile(r'(?i)-?-(?:t(?:ime)?stamp_)?pos\s*=\s*'),
            'nofm': re.compile(r'(?i)-?-nofm\b'),
            'nopause': re.compile(r'(?i)-?-nopause\b'),
        }
        run_opts = { # Program run opts
            'backup_fnames': [],
            'tstamp': 'd', # d, dt, none
            'tstamp_pos': 'rear', # front, rear
            'is_nofm': 0,
            'is_nopause': 0,
        }
        
        # ARGV parsing
        parse_argv(cmd_opts, run_opts)
        
        # Notification - beginning
        if not run_opts['is_nofm']:
            show_front_matter(prog_info, 'prog', 'auth')
        
        # Main
        tilder(run_opts)
        
        # Notification - end
        pause_shell() if not run_opts['is_nopause'] else print()
        
    elif len(sys.argv) < 2:
        print(__doc__)
        pause_shell()


#
# Function calls
#
if __name__ == '__main__':
    outer_tilder()


#eof