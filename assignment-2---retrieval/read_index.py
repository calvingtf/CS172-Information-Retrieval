# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.

import argparse
from parsing import process_commands
from parsing import set_write

parser = argparse.ArgumentParser(description='Text retrieval program')
parser.add_argument("--doc", action="store", dest="doc", nargs = 1, help="Lists document information")
parser.add_argument("--term", action="store", dest="term", nargs = 1, help="Lists term information")
parser.add_argument("--write", action="store_true", dest="write",help="Saves system library to disk")
args = parser.parse_args()

if args.write is True:
    set_write()

if args.term is not None and args.doc is not None:
    process_commands(term=args.term, doc=args.doc)
elif args.doc is not None:
    process_commands(doc=args.doc)
elif args.term is not None:
    process_commands(term=args.term)

if args.term is None and args.doc is None and args.write is None:
    # print help if no args
    parser.print_help()
    
# Documentation: https://docs.python.org/3/library/argparse.html