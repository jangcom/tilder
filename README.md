<?xml version="1.0" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<link rev="made" href="mailto:" />
</head>

<body>



<ul id="index">
  <li><a href="#NAME">NAME</a></li>
  <li><a href="#SYNOPSIS">SYNOPSIS</a></li>
  <li><a href="#DESCRIPTION">DESCRIPTION</a></li>
  <li><a href="#OPTIONS">OPTIONS</a></li>
  <li><a href="#EXAMPLES">EXAMPLES</a></li>
  <li><a href="#REQUIREMENTS">REQUIREMENTS</a></li>
  <li><a href="#AUTHOR">AUTHOR</a></li>
  <li><a href="#COPYRIGHT">COPYRIGHT</a></li>
  <li><a href="#LICENSE">LICENSE</a></li>
</ul>

<h1 id="NAME">NAME</h1>

<pre><code>    tilder - Back up files into respective subdirectories</code></pre>

<h1 id="SYNOPSIS">SYNOPSIS</h1>

<pre><code>    python tilder.py [file ...]
                     [-tstamp=key] [-tstamp_pos=front|rear]
                     [-nofm] [-nopause]</code></pre>

<h1 id="DESCRIPTION">DESCRIPTION</h1>

<pre><code>    By emulating baker, the author&#39;s Perl program,
    this Python program facilitates backing up files.
    The main difference between the two programs is
    the method of naming subdirectories:
    - tilder (Python 3) ... subdirs are suffixed by the tilde (~)
    - baker (Perl 5)    ... subdirs are prefixed by &#39;bak_&#39;</code></pre>

<h1 id="OPTIONS">OPTIONS</h1>

<pre><code>    -tstamp=key (short term: -ts)
        d (default)
            Timestamp up to yyyymmdd
        dt
            Timestamp up to yyyymmdd_hhmm
        none
            No timestamp

    -tstamp_pos=front|rear (short term: -pos, default: rear)</code></pre>

<h1 id="EXAMPLES">EXAMPLES</h1>

<pre><code>    python tilder.pl oliver.eps heaviside.dat -nopause
    python tilder.pl bateman.ps -tstamp=d
    python tilder.pl harry_bateman.ps -ts=none</code></pre>

<h1 id="REQUIREMENTS">REQUIREMENTS</h1>

<pre><code>    Python 3 (&gt;v3.6)</code></pre>

<h1 id="AUTHOR">AUTHOR</h1>

<pre><code>    Jaewoong Jang &lt;jangj@korea.ac.kr&gt;</code></pre>

<h1 id="COPYRIGHT">COPYRIGHT</h1>

<pre><code>    Copyright (c) 2018-2019 Jaewoong Jang</code></pre>

<h1 id="LICENSE">LICENSE</h1>

<pre><code>    This software is available under the MIT license;
    the license information is found in &#39;LICENSE&#39;.</code></pre>


</body>

</html>
