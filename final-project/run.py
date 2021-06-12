import argparse
import glob
import os

from wikipedia_crawler import WikipediaCrawler

parser = argparse.ArgumentParser(description='Wikipedia Crawler')
parser.add_argument('depth', type=int, action="store", nargs = 1, help='a number for how deep the crawler should go')
parser.add_argument('--url', dest="source", type=str, default=None, help='starting url to crawl (if not given, sources.txt is used)')
parser.add_argument('--dir', dest="directory", type=str, default="data", help='folder to store pages')
parser.add_argument('--pages', dest="pages", type=int, default = -1, help='total number of pages to crawl',)
parser.add_argument('--clean', action="store_true", dest="clean", help='cleans the folder of all .json files before crawling')
args = parser.parse_args()

path = os.getcwd()
newpath = path + "/" + str(args.directory)

# Making the data folder
if not os.path.exists(newpath):
    os.mkdir(args.directory + "/")

if args.clean is True:
    files = glob.glob(args.directory + "/*")
    for f in files:
        os.remove(f)

if args.source is None:
    sources = []
    with open("sources.txt", "r", encoding='utf-8') as source_file:
        for line in source_file:
            sources.append(line.strip("\n"))
else:
    sources = [args.source]

crawler = WikipediaCrawler(args.directory, args.depth[0], args.pages)
for source_url in sources:
    pages = crawler.crawl(source_url)
    
# Documentation: https://docs.python.org/3/library/argparse.html