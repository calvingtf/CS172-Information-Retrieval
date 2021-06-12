import json

# Class for one WikipediaPage
class WikipediaPage:

    # Initialization
    def __init__(self, url):
        self.url = url
        self.title = []
        self.html = ""
        self.table_of_contents = []
        self.graphics = []
        self.paragraphs = []
        self.links = []

    # Writes to a json file
    def store(self, directory):
        
        
        # File name can't contain spaces, / \ : * ? " < > |
        file_name = self.title.replace(" ", "_")
        file_name = file_name.replace("/", "_")
        file_name = file_name.replace("\\", "_")
        file_name = file_name.replace(":", "_")
        file_name = file_name.replace("*", "_")
        file_name = file_name.replace("?", "_")
        file_name = file_name.replace('"', "_")
        file_name = file_name.replace("<", "_")
        file_name = file_name.replace(">", "_")
        file_name = file_name.replace("|", "_")
        
        with open(directory + "/" + file_name + '.json', 'w', encoding='utf-8') as file:
            body = self.__dict__
            json.dump(body, file, indent=4, ensure_ascii=False)

def extract_wiki_page(url):
    return url.split("/")[-1]