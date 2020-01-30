from Spider import general_functions as gf
from Spider import html_parser as parser
from urllib.request import urlopen


class Crawler:

    project_name = ''
    base_url = ''
    domain_name = ''

    queue_file = ''
    crawled_file = ''

    links_found = []
    set_crawled = []

    number_of_urls_crawled = ''
    max_urls = 0

    overflow_flag = False

    def __init__(self, project_name, base_url, domain_name, max_urls):
        Crawler.project_name = project_name
        Crawler.base_url = base_url
        Crawler.domain_name = domain_name
        Crawler.max_urls = max_urls

        Crawler.queue_file = Crawler.project_name + '/queue.txt'
        Crawler.crawled_file = Crawler.project_name + '/crawled.txt'

        self.boot()

    @staticmethod
    def boot():
        gf.create_project_dir(Crawler.project_name)
        gf.create_data_files(Crawler.project_name, Crawler.base_url)
        Crawler.set_crawled = gf.file_to_set(Crawler.crawled_file)

    @staticmethod
    def gather_links(url):
        html_string_format = ''
        try:
            response = urlopen(url)
            if 'text/html' in response.getheader('Content-Type'):
                html_byte_format = response.read()
                html_string_format = html_byte_format.decode("utf-8")

            link_searcher = parser.URLFinder(Crawler.base_url, url)
            link_searcher.feed(html_string_format)
        except:
            print('Error: cannot crawl ' + url)
            return set()

        return link_searcher.get_links()
