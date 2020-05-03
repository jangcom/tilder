#!/usr/bin/env python3
import os
import re
from datetime import datetime
import shutil
import argparse


def parse_argv():
    """Parse sys.argv"""
    parser = argparse.ArgumentParser(description='File backup assistant')
    parser.add_argument('--ts_lev',
                        choices=['d', 'dt', 'none'],
                        default='d',
                        help='timestamp level')
    parser.add_argument('--ts_pos',
                        choices=['bef', 'aft'],
                        default='aft',
                        help='timestamp position relative to the filename')
    parser.add_argument('--nopause',
                        dest='is_nopause',
                        action='store_true',
                        help='do not pause the shell at the program end')
    parser.add_argument('file',
                        nargs='+',
                        help='files to be backed up')
    return parser.parse_args()


def tilder(args):
    """File backup assistant"""
    # Timestamps
    ymd = datetime.today().strftime('%Y%m%d')
    hms = datetime.today().strftime('%H%M%S')  # Capital: zero-padded
    hm = datetime.today().strftime('%H%M')
    ts = ''
    if re.search(r'(?i)\bd\b', args.ts_lev):
        ts = ymd
    elif re.search(r'(?i)\bdt\b', args.ts_lev):
        ts = ymd + '_' + hm
    fname_sep = '_' if ts else ''

    # Buffering
    f_orig_and_copy = {}
    lengthiest = ''
    fname_re = re.compile(r'(.*)([.]\w+)$')
    for f_orig in args.file:
        if not os.path.exists(f_orig) or os.path.isdir(f_orig):
            continue
        if len(f_orig) > len(lengthiest):
            lengthiest = f_orig  # Will be used as a conversion

        # Filenaming
        bname = re.sub(fname_re, r'\1', f_orig)
        ext = re.sub(fname_re, r'\2', f_orig)
        f_copy = None
        if re.search(r'(?i)bef', args.ts_pos):
            f_copy = ts + fname_sep + bname
        elif re.search(r'(?i)aft', args.ts_pos):
            f_copy = bname + fname_sep + ts
        if not ext == f_orig:  # For extensionless
            f_copy = f_copy + ext

        # Buffer the original and copy files as key-val pairs.
        subdir = './' + f_orig + '~'
        f_orig_and_copy[f_orig] = [subdir, subdir + '/' + f_copy]

    # Flushing
    if f_orig_and_copy:
        print('-' * 70)
        conv = '%-{}s'.format(len(lengthiest))
        for k, v in f_orig_and_copy.items():
            print(f'{conv} => %s' % (k, v[1]))
            if not os.path.exists(v[0]):
                os.mkdir(v[0])
            shutil.copyfile(k, v[1])
        print('-' * 70)
        print('File backup completed.', end=' ')
    else:
        print('Files not found.')


if __name__ == '__main__':
    args = parse_argv()
    tilder(args)
    if not args.is_nopause:
        input('Press enter to exit...')
