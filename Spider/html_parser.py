from html.parser import HTMLParser
from urllib import parse


class URLFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    self.links.append(url)
        self.links = list(dict.fromkeys(self.links))

    def get_links(self):
        return self.links

    def error(self, message):
        pass
