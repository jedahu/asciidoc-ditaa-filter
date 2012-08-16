#! /usr/bin/env python
"""AsciiDoc filter script which runs the ditaa program to
convert ASCII line drawings into a PNG image file.

Requires the ditaa Java package to be present in the filter directory.

Copyright (C) 2011 Henrik Maier. Free use of this software is
granted under the terms of the GNU General Public License (GPL).

Modified by Jeremy Hughes <jed@jedatwork.com> to be an in-process filter.
"""

__version__ = '1.2-jedahu'

import os, sys, tempfile

#
# Configuration constants
#
DITAA_JAR = os.environ.get('DITAA_JAR')

#
# Helper functions and classes
#
class AppError(Exception):
    """Application specific exception."""
    pass



#
# Application init and logic
#
class Application():
    """Application class"""

    def __init__(self,
            lines,
            target=None,
            verbose=False,
            scaling=1.0,
            tabs=8,
            opts=(),
            docdir=None):
        """Process commandline arguments"""
        self.target = target
        self.lines = lines
        self.verbose = verbose
        self.scaling = scaling
        self.tabs = tabs
        self.round_corners = 'round-corners' in opts
        self.no_separation = 'no-separation' in opts
        self.no_shadows = 'no-shadows' in opts
        self.no_antialias = 'no-antialias' in opts
        self.docdir = docdir

    def run(self):
        """Core logic of the application"""
        outfile = os.path.abspath(os.path.join(self.docdir, self.target))
        outdir = os.path.dirname(outfile)
        if not os.path.isdir(outdir):
            raise AppError, 'directory does not exist: %s' % outdir
        temp = None
        try:
            infile = None
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                infile = temp.name
                self.print_verbose("Temporary input file is %s" % infile)
                for line in self.lines:
                    temp.write(line)
                    temp.write('\n')

            options = "--overwrite" # Always set
            if self.verbose:
                options += " -v"
            if self.no_antialias:
                options += " --no-antialias"
            if self.no_separation:
                options += " --no-separation"
            if self.round_corners:
                options += " --round-corners"
            if self.no_shadows:
                options += " --no-shadows"
            if self.scaling:
                options += " --scale %f" % self.scaling
            if self.tabs:
                options += " --tabs %d" % self.tabs
            self.systemcmd('java -jar "%s" "%s" "%s" %s' % (
                      DITAA_JAR, infile, outfile, options))
        finally:
            if temp:
                os.remove(temp.name)

    def systemcmd(self, cmd):
        if not self.verbose:
            cmd += " 2>%s" % os.devnull
        cmd += " >&2" # redirect verbose output to stderr
        self.print_verbose("Exec: %s" % cmd)
        if os.system(cmd):
            raise AppError, "failed command: %s" % cmd

    def print_verbose(self, line):
        if self.verbose:
            sys.stderr.write(line + os.linesep)


def asciidoc_filter(lines, **kwargs):
    if not DITAA_JAR:
        raise AppError, 'DITAA_JAR env var not set.'
    app = Application(lines, **kwargs)
    app.run()
    return [' ']
