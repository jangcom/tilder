@echo off

rem Do not name this batch file as 'pod2html';
rem otherwise, the pod2html executable will not be run correctly.

pod2html --infile=tilder.pod --outfile=tilder.html
