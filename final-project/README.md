# CS172 - FINAL PROJECT 

## Team members

- Aden Ghadimi
- Calvin TszFung Ng
- Kevin Ni
______________________________________________________


## Collaboration Details


### Part 1 - Crawler
The overview of our system, 
(A) Architecture:


Features - 




(B)


(C)

#### Crawler Set up Instructions

Step 1: Clone the repository.

> $git clone <repository url>

Step 2: Check Python Version. More information can be found [here](https://www.python.org/download/releases/3.0/)

> $python --version

Step 3: Install the packages.

> $pip install -r requirements.txt

Step 4: Run the crawler with a specified depth level by typing `py run.py [#]`
Run `py run.py -h` to pull up a help GUI of possible commmands.
Possible flags are:
> --url

> --dir

> --pages

> --clean

#### How to run the crawler
The main command to run is `py run.py`

Depth - This number will determine how nested the crawler should go.
> If 0 is given, only the starting pages will be crawled

> If 1 is given, only the starting pages and the links on those pages will be crawled.

> If 2 is given, only the starting pages and 2 links in will be crawled.

> If -1 is given, there will be no maximum depth. WARNING: This is highly discouraged

Help - Will display the help message with descriptions on all the flags

URL - Starting URL to crawl from. If this is not provided, sources.txt will automatically be used. Sources.txt can contain a URL on each new line, and the crawler will crawl through each.

Directory - This will determine the name for the folder where the .json files are stored in. If none is given, the name `data` is automatically set.

Pages - This will set the total number of pages to crawl. If none is provided, -1 will be set and there will be no maximum.

Clean - This is a flag that does not take in a value. If this flag is provided, the crawler will first clean the folder marked for the .json files before repopulating it.

### Part 2 - Indexer


Note: 


Requirements



#### Steps to view the website

