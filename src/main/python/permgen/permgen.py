#############################################################################
# permgen.py: Main code that calls Executer.run().
#
# Author: Marco Peters, Norman Fomferra
############################################################################# #

from optparse import OptionParser
import sys
import batch

if __name__ == "__main__":
    opt_parser = OptionParser(usage="Usage: %prog [options]", version="%prog 0.1")
    opt_parser.add_option("-c", "--config", dest="config_file", default="config.txt",
                      help="Use congiguration given in the file CONFIG", metavar="CONFIG")
    opt_parser.add_option("-f", "--file", dest="output_file",
                      help="Write the final report to FILE", metavar="FILE")
    opt_parser.add_option("-t", "--timeout", dest="timeout", default=100000, type="int",
                      help="Kill any single process taking longer than MINUTES [default: %default]",
                      metavar="MINUTES")
    opt_parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="Don't print status messages to stdout [default: %default]")

    (options, args) = opt_parser.parse_args()
    
    batch.Executer(options).run()
