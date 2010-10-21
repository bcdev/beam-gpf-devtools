from optparse import OptionParser
import sys
import batch

if __name__ == "__main__":
    opt_parser = OptionParser(usage="Usage: %prog [options]", version="%prog 0.1")
    opt_parser.add_option("-c", "--config", dest="config_file", default="config.txt",
                      help="use congiguration given in file CONFIG", metavar="CONFIG")
    opt_parser.add_option("-f", "--file", dest="output_file",
                      help="write report to FILE", metavar="FILE")
    opt_parser.add_option("-t", "--timeout", dest="timeout", default=-1, type="int",
                      help="a process is canceld if the time has passed [default: %default]",
                      metavar="MINUTES")
    opt_parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout [default: %default]")

    (options, args) = opt_parser.parse_args()
    
    batch.Executer(options).run()
