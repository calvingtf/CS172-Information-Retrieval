# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.

import argparse
from parsing import process_commands
from parsing import set_write
from parsing import process_query

parser = argparse.ArgumentParser(description='Text retrieval program')
parser.add_argument("query", type=str, metavar="Query_File_Path", action="store", nargs = 1, help="File path to the query file")
parser.add_argument("output", type=str, metavar="Output_File_Path", action="store", nargs = 1, help="File path to the output file")
parser.add_argument("--write", action="store_true", dest="write",help="Saves system library to disk")
args = parser.parse_args()

if args.write is True:
    set_write()
    
process_query(args.query, args.output)

# if args.term is not None and args.doc is not None:
    # process_commands(term=args.term, doc=args.doc)
# elif args.doc is not None:
    # process_commands(doc=args.doc)
# elif args.term is not None:
    # process_commands(term=args.term)

# if args.term is None and args.doc is None and args.write is None:
    # # print help if no args
    # parser.print_help()
    
# Documentation: https://docs.python.org/3/library/argparse.html