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
        # self.crawl_page('First crawler', Crawler.base_url)

    @staticmethod
    def boot():
        gf.create_project_dir(Crawler.project_name)
        gf.create_data_files(Crawler.project_name, Crawler.base_url)
        # Crawler.links_found = gf.file_to_set(Crawler.queue_file)
        Crawler.set_crawled = gf.file_to_set(Crawler.crawled_file)

    @staticmethod
    def crawl_page(crawler_name, current_url):
        print("Crawling...")
        if Crawler.overflow_flag:
            pass
        elif current_url not in Crawler.set_crawled:
            print(crawler_name + ' crawling ' + current_url)
            Crawler.add_links_queue(Crawler.gather_links(current_url))
            Crawler.set_crawled.append(current_url)
            # Crawler.cap_at_max_urls()
            # Crawler.update_files()

            return Crawler.links_found

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

    @staticmethod
    def add_links_queue(set_of_links):
        for url in set_of_links:
            if url in Crawler.links_found or Crawler.set_crawled:
                continue
            if Crawler.domain_name not in url:
                continue
            Crawler.links_found.append(url)

    @staticmethod
    def cap_at_max_urls():
        total_links = len(Crawler.links_found) + gf.get_number_of_urls_in_file(Crawler.crawled_file)
        # if total_links > Crawler.max_urls:
        #     Crawler.links_found = []
        #     Crawler.set_crawled = []
        #     Crawler.overflow_flag = True
        #
        # elif total_links + len(Crawler.set_crawled) >= Crawler.max_urls:
        #     Crawler.links_found = []
        #     Crawler.overflow_flag = True
        #
        # elif total_links + len(Crawler.set_crawled) + len(Crawler.links_found) > Crawler.max_urls:
        #     acceptable_amount = Crawler.max_urls - total_links - len(Crawler.set_crawled)
        #     Crawler.reduce_set_size(acceptable_amount)
        #     Crawler.overflow_flag = True
        if total_links > Crawler.max_urls:
            print(gf.get_number_of_urls_in_file(Crawler.queue_file))
            Crawler.reduce_set_size(Crawler.max_urls - gf.get_number_of_urls_in_file(Crawler.queue_file))
            Crawler.overflow_flag = True

    @staticmethod
    def reduce_set_size(size_required):
        new_set = []
        for x in range(size_required):
            new_set.append(Crawler.links_found[x])
        Crawler.links_found = new_set

    @staticmethod
    def update_files():
        # gf.list_to_file(Crawler.links_found, Crawler.queue_file)
        gf.list_to_file(Crawler.set_crawled, Crawler.crawled_file)
