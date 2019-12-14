#!/usr/bin/python3

"""\
NAME
    tilder - Back up files into respective subdirectories

SYNOPSIS
    python tilder.py [-h] [--ts_lev {d,dt,none}] [--ts_pos {bef,aft}]
                     [--nofm] [--nopause]
                     file [file ...]

DESCRIPTION
    Back up your files into respective subdirectories
    with explicit timestamps.

OPTIONS
    -h, --help
        The argparse help message will be displayed.

    --ts_lev {d,dt,none}
        d (default)
            Timestamp up to yyyymmdd
        dt
            Timestamp up to yyyymmdd_hhmm
        none
            No timestamp

    --ts_pos {bef,aft}
        bef
            Timestamping before the filename
        aft (default)
            Timestamping after the filename

    --nofm
        The front matter will not be displayed at the beginning of the program.

    --nopause
        The shell will not be paused at the end of the program.
        Use it for a batch run.

    file ...
        The list of files to be backed up.

EXAMPLES
    python tilder.pl oliver.eps heaviside.dat --nopause
    python tilder.pl bateman.ps --ts_lev=d
    python tilder.pl harry_bateman.ps --ts_lev=none

REQUIREMENTS
    Python 3 (>v3.6)

SEE ALSO
    We also have a file backup assistant written in Perl:
    L<baker|https://github.com/jangcom/baker>
    The main difference between tilder and baker is
    the naming of subdirectories:
    - tilder (Python 3) ... subdirs are suffixed by the tilde (~)
    - baker (Perl 5)    ... subdirs are prefixed by 'bak_'

AUTHOR
    Jaewoong Jang <jangj@korea.ac.kr>

COPYRIGHT
    Copyright (c) 2018-2019 Jaewoong Jang

LICENSE
    This software is available under the MIT license;
    the license information is found in 'LICENSE'.\
"""

import sys
import os
import argparse
import re
import shutil
from datetime import datetime


def parse_argv(run_opts):
    """Parse sys.argv"""
    #
    # argparse
    #
    parser = argparse.ArgumentParser(
        description="Back up files \
        into respective subdirectories",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # Optional, selection type
    parser.add_argument('--ts_lev',
                        choices=['d', 'dt', 'none'],
                        default='d',
                        help='timestamp level')
    parser.add_argument('--ts_pos',
                        choices=['bef', 'aft'],
                        default='aft',
                        help='timestamp position relative to the filename')
    # Optional, toggle type
    parser.add_argument('--nofm',
                        dest='is_nofm',
                        action='store_true',
                        help='suppress the front matter')
    parser.add_argument('--nopause',
                        dest='is_nopause',
                        action='store_true',
                        help='do not pause the shell at the program end')
    # Positional
    parser.add_argument('file',
                        nargs='+',
                        help='files to be backed up')
    args = parser.parse_args()

    #
    # Actions
    #
    run_opts['ts'] = args.ts_lev
    run_opts['ts_pos'] = args.ts_pos
    run_opts['is_nofm'] = args.is_nofm
    run_opts['is_nopause'] = args.is_nopause
    for f in args.file:
        if os.path.exists(f) and not os.path.isdir(f):
            run_opts['backup_files'].append(f)


def show_front_matter(*opts):
    """Display the front matter."""
    prog_info = opts[0]

    # Determine which fields to print.
    is_prog = is_auth = 0
    for opt in opts[1:]:
        if opt == 'prog':
            is_prog = 1
        if opt == 'auth':
            is_auth = 1

    # Top rule
    if is_prog == 1 or is_auth == 1:
        print('+' * 70)

    # Program info, except the usage
    if is_prog == 1:
        print(prog_info['titl'], '-', prog_info['expl'])
        print(prog_info['titl'], prog_info['vers'],
              '({})'.format(prog_info['date_last']))

    # Author info
    if is_auth == 1:
        if is_prog == 1:
            print('')
        for v in prog_info['auth'].values():
            print(v)

    # Bottom rule
    if is_prog == 1 or is_auth == 1:
        print('+' * 70)


def pause_shell():
    """Pause the shell."""
    input("Press enter to exit...")


def tilder(run_opts):
    """Back up the designated files."""
    # Generate timestamps.
    _ymd = datetime.today().strftime("%Y%m%d")
    _hms = datetime.today().strftime("%H%M%S")  # Capital: zero-padded
    _hm = datetime.today().strftime("%H%M")
    ts_sep = '_'
    datetimes = {
        'none': '',
        'ymd': _ymd,
        'hms': _hms,
        'hm': _hm,
        'ymdhms': _ymd + ts_sep + _hms,
        'ymdhm': _ymd + ts_sep + _hm,
    }
    if re.search(r'(?i)\bd\b', run_opts['ts']):
        ts_of_int = datetimes['ymd']
    if re.search(r'(?i)\bdt\b', run_opts['ts']):
        ts_of_int = datetimes['ymdhm']
    if re.search(r'(?i)\bnone\b', run_opts['ts']):
        ts_of_int = datetimes['none']

    # Filename elements
    fnames_old_and_new = {}
    lengthiest = ''
    path_delim = '\\' if re.search(r'(?i)win32', sys.platform) else '/'
    path_of_int = '.'
    backup_flag = '~'
    fname_re = re.compile(r'(.*)([.]\w+)$')

    # Construct pairs of old and new filenames.
    for fname_old in run_opts['backup_files']:
        # Find the lengthiest filename to construct a conversion.
        if len(fname_old) > len(lengthiest):
            lengthiest = fname_old

        # Dissociate a filename and define a backup filename.
        bname = re.sub(fname_re, r'\1', fname_old)
        ext = re.sub(fname_re, r'\2', fname_old)
        fname_sep = '_' if ts_of_int else ''
        if re.search(r'(?i)(bef|front)', run_opts['ts_pos']):
            fname_new = ts_of_int + fname_sep + bname
        elif re.search(r'(?i)(aft|rear)', run_opts['ts_pos']):
            fname_new = bname + fname_sep + ts_of_int
        if not ext == fname_old:  # For extensionless filenames
            fname_new = fname_new + ext

        # Buffer the old and new filenames as key-val pairs.
        subdir = path_of_int + path_delim + fname_old + backup_flag
        fnames_old_and_new[fname_old] = [
            subdir,
            subdir + path_delim + fname_new,
        ]

    # Back up the designated files following notification.
    if fnames_old_and_new:
        print('-' * 70)
        conv = '%-' + str(len(lengthiest)) + 's'
        for k, v in fnames_old_and_new.items():
            # Vertically-aligned printing:
            # Use Ruby-like str interpolation to expand
            # a conversion beforehand, and use
            # the old-school Python str formatting.
            print(f"{conv} => %s" % (k, v[1]))
            if not os.path.exists(v[0]):
                os.mkdir(v[0])
            shutil.copyfile(k, v[1])
        print('-' * 70)
    if fnames_old_and_new:
        print("Backing up completed.", end=' ')


def outer_tilder():
    """tilder running routine"""
    if len(sys.argv) >= 2:
        prog_info = {
            'titl': 'tilder',
            'expl': 'Back up files into respective subdirectories',
            'vers': 'v1.02',
            'date_last': '2019-12-14',
            'date_first': '2018-06-23',
            'auth': {
                'auth': 'Jaewoong Jang',
                'mail': 'jangj@korea.ac.kr',
            },
        }
        run_opts = {
            'backup_files': [],
            'ts': 'd',
            'ts_pos': 'aft',
            'is_nofm': False,
            'is_nopause': False,
        }

        parse_argv(run_opts)
        if not run_opts['is_nofm']:
            show_front_matter(prog_info, 'prog', 'auth')
        tilder(run_opts)
        pause_shell() if not run_opts['is_nopause'] else print()

    elif len(sys.argv) < 2:
        print(__doc__)
        pause_shell()


if __name__ == '__main__':
    outer_tilder()
