#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016-2018   Kuldeep S. Meel
# Copyright (C) 2018        Mate Soos
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.


from __future__ import with_statement  # Required in 2.5
from __future__ import print_function

import sys
import os
import time
import optparse


def parseOutput(fileName):
    f = open(fileName, 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        if (line.strip().startswith('v')):
            return line
    return ''


usage = "usage: %prog [options] <input.cnf>"
desc = """Gives the minimal independent set of the file.

If both --useind is set and --firstinds are specified, the union of both independent supports is considered

If --useind is set but there is no independent support in input file, and --firstinds is not specified, all variables are considered
"""


def set_up_parser():
    parser = optparse.OptionParser(usage=usage, description=desc)
    parser.add_option("--timeout", metavar="TOUT", dest="timeout", type=int,
                      default=3000, help="timeout for iteration in seconds (default: %default seconds)")
    parser.add_option("--logging", action="store_true", default=False,
                      dest="logging", help="To log more")
    parser.add_option("--output", dest="outputfile", type=str, default=None,
                      help="Output file destination. Default is 'inputfile.ind'")
    parser.add_option("--log", dest="logfile", type=str, default="log.txt",
                      help="Log file destination. Deafult : %default")
    parser.add_option("--max", dest="maxiters", type=int, default=1,
                      help="up to 'max' number of minimal independent supports will be generated. Default: %default")
    parser.add_option("--firstinds", dest="firstinds", type=int,
                      default=1000000000,
                      help="between 1 and number of variables. Indicates that variables 1 to firstinds should be used as an independent support. Default: uses all variables")
    parser.add_option("--useind", dest="useind", action="store_true",
                      default=False,
                      help="use independent support provided in input file")
    parser.add_option("--verbose", "-v", action="store_true", default=False,
                      dest="verbose", help="Print more output")
    return parser


def defaultParams():
    # timeout, logging, log, max, useInd, firstinds
    return 3000, 0, 'log.txt', 1, 'false', 0

# action=0 -> print help
# action=1 -> couldn't understand argument. error will pass the string
# action=2 -> no inputfile
# action=3 -> input file not last in argument list. Fail gracefully with error to avoid confusion with old style of arguments
# action=4 -> all set. go.


if __name__ == "__main__":
    parser = set_up_parser()
    (options, args) = parser.parse_args()
    inputfile = args[0]
    extension = inputfile[-4:]
    if options.outputfile is not None:
        outputfile = options.outputfile
    else:
        outputfile = inputfile + ".ind"

    options.timeout += 10

    maxiters = options.maxiters
    if options.firstinds < 1:
        print("firstinds has to be greater than 1")
        exit(-1)

    timeTaken = time.time()
    if extension == '.cnf':
        gmusFile = inputfile[:-4] + '.gcnf'
        tempOutFile = inputfile[:-4] + '.tcnf'
    else:
        gmusFile = outputfile + '.gcnf'
        tempOutFile = outputfile + '.tcnf'

    f = open(outputfile, 'w')
    f.close()
    if options.logging == 1:
        f = open(options.logfile, 'w')
        f.close()
    cmd = "./togmus %s %s %s %s" % (inputfile, gmusFile, options.useind,
                                    options.firstinds)
    os.system(cmd)
    timeTaken = timeTaken - time.time()

    # run maxiters iterations
    indMap = {}
    maxTry = 10
    attempts = 0
    i = 0
    while i < maxiters:
        timeTaken = time.time()
        cmd = "muser2 -v 0 -grp -comp -minisats -order 4 -T %s %s > %s" % (
            options.timeout, gmusFile, tempOutFile)
        os.system(cmd)

        indvars = parseOutput(tempOutFile)
        indvars = indvars.strip().lstrip(" v ")
        if indvars not in indMap:
            indMap[indvars] = 1
        else:
            attempts += 1
            if (attempts >= maxTry):
                break
            else:
                continue

        timeTaken = time.time() - timeTaken
        if options.outputfile is not None:
            f = open(outputfile, 'a')
            f.write(indvars)
            f.close()
            if options.logging == 1:
                f = open(options.logfile, 'a')
                f.write(str(i) + ':' + str(i + attempts) +
                        ':' + str(timeTaken) + '\n')
                f.close()
        else:
            print("c ind %s" % indvars)
            print("num independent vars:", len(indvars.split())-1)
        i += 1

    os.unlink(tempOutFile)
    os.unlink(gmusFile)
