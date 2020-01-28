import threading
from queue import Queue
from Spider import crawler
from Spider import general_functions as gf


class CrawlerManager:

    def __init__(self, project_name, homepage, domain_name, max_urls, thread_number):
        self.thread_queue = Queue()
        self.PROJECT_NAME = project_name
        self.HOMEPAGE = homepage
        self.DOMAIN_NAME = domain_name
        self.MAX_URLS = max_urls
        self.NUMBER_OF_THREADS = thread_number
        self.QUEUE_FILE = self.PROJECT_NAME + '/queue.txt'
        self.CRAWLED_FILE = self.PROJECT_NAME + '/crawled.txt'

        crawler.Crawler(project_name, homepage, domain_name, max_urls)

    def run(self):
        self.create_crawlers()
        self.crawl()

    def create_jobs(self):
        for link in gf.file_to_set(self.QUEUE_FILE):
            self.thread_queue.put(link)
        self.thread_queue.join()
        self.crawl()

    def create_crawlers(self):
        for _ in range(self.NUMBER_OF_THREADS):
            t = threading.Thread(target=self.work)
            t.daemon = True
            t.start()

    def work(self):
        while True:
            url = self.thread_queue.get()
            crawler.Crawler.crawl_page(threading.current_thread().name, url)
            self.thread_queue.task_done()

    def crawl(self):
        total_links = gf.get_number_of_urls_in_file(self.QUEUE_FILE) + gf.get_number_of_urls_in_file(self.CRAWLED_FILE)
        if total_links >= self.MAX_URLS:
            pass

        queued_links = gf.file_to_set(self.QUEUE_FILE)
        if len(queued_links) > 0:
            print(str(len(queued_links)) + " links remaining in the queue")
            self.create_jobs()
