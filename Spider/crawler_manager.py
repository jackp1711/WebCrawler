import threading
from queue import Queue
from Spider import crawler
from Spider import general_functions as gf
import sys


class CrawlerManager:

    def __init__(self, project_name, homepage, domain_name, max_urls, thread_number, v_flag, o_flag, o_file):
        self.thread_queue = Queue()
        self.PROJECT_NAME = project_name
        self.HOMEPAGE = homepage
        self.DOMAIN_NAME = domain_name
        self.MAX_URLS = max_urls
        self.NUMBER_OF_THREADS = thread_number
        self.QUEUE_FILE = self.PROJECT_NAME + '/queue.txt'
        self.CRAWLED_FILE = self.PROJECT_NAME + '/crawled.txt'
        self.VERBOSE_FLAG = v_flag
        self.OUTPUT_FLAG = o_flag
        self.OUTPUT_FILE = o_file

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
            if not crawler.Crawler.overflow_flag:
                break

    def crawl(self):
        total_links = gf.get_number_of_urls_in_file(self.QUEUE_FILE) + gf.get_number_of_urls_in_file(self.CRAWLED_FILE)
        if total_links + 1 >= self.MAX_URLS:
            self.finalise()
            sys.exit()
        else:
            queued_links = gf.file_to_set(self.QUEUE_FILE)
            if len(queued_links) > 0:
                print(str(len(queued_links)) + " links remaining in the queue")
                self.create_jobs()

    def finalise(self):
        if self.OUTPUT_FLAG:
            print(self.OUTPUT_FILE)
            gf.create_output_file(self.QUEUE_FILE, self.CRAWLED_FILE, self.OUTPUT_FILE)
        else:
            gf.print_to_console(self.QUEUE_FILE, self.CRAWLED_FILE)
