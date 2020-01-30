from html.parser import HTMLParser
from urllib import parse

"""
    Class to process a given HTML page and gather all of the links contained within the <a> tags href value.
    URLFinder class overrides the handle_starttag function contained in its parent class HTMLParser.
"""


class URLFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = []

    # Overridden method to identify the <a> tags within the HTML and gathers their href values.
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    self.links.append(url)
        self.links = list(dict.fromkeys(self.links))

    # Function to return all of the links gathered.
    def get_links(self):
        return self.links

    def error(self, message):
        pass
