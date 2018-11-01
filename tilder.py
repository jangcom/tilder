#!/usr/bin/python3
import sys
from os       import mkdir
from os.path  import isdir, exists
import re # regex
from shutil   import copyfile
from datetime import datetime


#
# Front matter
#
border_len = 70
borders    = {
    '+' : ('+' * border_len),
    '=' : ('=' * border_len),
    '-' : ('-' * border_len),
}
prog_info = {
    'titl'        : 'tilder',
    'expl'        : 'Reimplementation of baker in Python 3',
    'vers'        : 'v1.0.0',
    'date_last'   : '2018-09-12',
    'date_first'  : '2018-06-23',
    'opts'        : { # Command options
        'tstamp_up_to_d' : '-dt=d',
        'no_tstamp'      : '-dt=none',
    },
    'auth'        :  {
        'auth' : 'Jaewoong Jang',
        'posi' : 'PhD student',
        'affi' : 'University of Tokyo',
        'mail' : 'jang.comsci@gmail.com',
    },
    'usage'       : 
"""    NAME
        tilder - Reimplementation of baker in Python 3

    SYNOPSIS
        python3 tilder.py [-dt=key] file ...

    DESCRIPTION
        Back up files into respective subdirectories suffixed by the tilde (~).

    OPTIONS
        -dt=key
            d
                Timestamp reduces from yyyymmdd_hhmm to yyyymmdd.
            none
                Timestamp suppressed.

    EXAMPLES
        python3 tilder.pl oliver.eps heaviside.dat
        python3 tilder.pl bateman.ps -dt=d
        python3 tilder.pl harry_bateman.ps -dt=none

    REQUIREMENTS
        Python 3 (>v3.6)

    SEE ALSO
        python(1)

    AUTHOR
        Jaewoong Jang <jang.comsci@gmail.com>

    COPYRIGHT
        Copyright (c) 2018 Jaewoong Jang

    LICENSE
        This software is available under the MIT license;
        the license information is found in 'LICENSE'."""
}


#
# Filename elements
#
fname_sep   = '_'
path_delim  = '/'
path_of_int = '.'
backup_flag = '~' # Used as the suffix of backup dirs


#
# Timestamp
#
_ymd = datetime.today().strftime("%Y%m%d")
_hms = datetime.today().strftime("%H%M%S") # Capital: zero-padded
_hm  = datetime.today().strftime("%H%M")
datetimes = {
    'none'   : '', # Used for timestamp suppressing
    'ymd'    : _ymd,
    'hms'    : _hms,
    'hm'     : _hm,
    'ymdhms' : _ymd + fname_sep + _hms,
    'ymdhm'  : _ymd + fname_sep + _hm,
};
tstamp_of_int = datetimes['ymdhm'] # Default

# If requested, reduce the datetime element.
for arg in sys.argv:
    if arg == prog_info['opts']['tstamp_up_to_d']:
        tstamp_of_int = datetimes['ymd']
    if arg == prog_info['opts']['no_tstamp']:
        tstamp_of_int = datetimes['none']


#
# Function definitions
#
def show_front_matter(*opts, prog_dict=prog_info):
    """Display the front matter"""
    
    # Determine which fields to print.
    (is_prog, is_auth, is_usage) = '', '', ''
    for opt in list(opts):
        if opt == 'prog' : is_prog  = 1
        if opt == 'auth' : is_auth  = 1
        if opt == 'usage': is_usage = 1
    
    # Top rule
    if is_prog == 1 or is_auth == 1: print(borders['+'])
    
    # Program info, except the usage
    if is_prog == 1:
        print(prog_dict['titl'], (prog_dict['vers'] + ":"), prog_dict['expl'])
        print("Last update: ", prog_dict['date_last'])
    
    # Author info
    if is_auth == 1:
        if is_prog == 1: print("")
        for v in prog_dict['auth'].values(): print(v)
    
    # Bottom rule
    if is_prog == 1 or is_auth == 1: print(borders['+'])
    
    # Program usage
    if is_usage == 1: print(prog_info['usage'])
    
    # Feed a blank line at the end of the front matter.
    print("")


def tilder(*args):
    """Back up files, with timestamps, into respective subdirs."""
    
    fname_old_and_new = {}
    lengthiest = ''
    fname_re   = re.compile(r'(.*)([.]\w+)$')
    for fname_old in sys.argv[1:]:
        if fname_old == prog_info['opts']['tstamp_up_to_d']: continue
        if isdir(fname_old): continue
        if not exists(fname_old): continue
        
        # Find the lengthiest filename to construct a conversion
        if len(fname_old) > len(lengthiest): lengthiest = fname_old
        
        # Dissociate a filename and define a backup filename
        bname     = re.sub(fname_re, r'\1', fname_old)
        ext       = re.sub(fname_re, r'\2', fname_old)
        if tstamp_of_int:
            fname_new = bname + fname_sep + tstamp_of_int
        elif not tstamp_of_int:
            fname_new = bname
        if not ext == fname_old: fname_new = fname_new + ext # For extensionless
        
        # Buffer the old and new fnames as key-val pairs
        subdir = path_of_int + path_delim + fname_old + backup_flag
        fname_old_and_new[fname_old] = [
            subdir,
            subdir + path_delim + fname_new,
        ]
    
    # Back up the designated files following displaying
    if fname_old_and_new:
        print(borders['-'])
        conv = '%-' + str(len(lengthiest)) + 's'
        for k, v in fname_old_and_new.items():
            # Vertically-aligned printing:
            # Use Ruby-like str interpolation to expand a conversion beforehand,
            # and use the conventional (plus, old school) Python str formatting.
            print(f"{conv} => %s" % (k, v[1]))
            
            if not exists(v[0]): mkdir(v[0])
            copyfile(k, v[1])
        print(borders['-'])
    if fname_old_and_new:
        print("Backing up completed.", end=' ')
    if not fname_old_and_new:
        print("None of the designated files found in"
              " [{}{}].".format(path_of_int, path_delim))


def pause_shell(*args):
    """Pause the shell"""
    
    input("Press enter to exit...")


#
# Function calls
#
if   len(sys.argv) < 2:  show_front_matter('usage')
elif len(sys.argv) >= 2: show_front_matter('prog', 'auth'); tilder()
pause_shell()
#eof