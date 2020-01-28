import threading
from queue import Queue
from Spider import crawler
from Spider import domain
from Spider import general_functions as gf

PROJECT_NAME = 'YCombinator'
HOMEPAGE = "https://news.ycombinator.com/"
DOMAIN_NAME = domain.get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
MAX_URLS = 100
NUMBER_OF_THREADS = 5
thread_queue = Queue()
crawler.Crawler(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME, MAX_URLS)


def create_jobs():
    for link in gf.file_to_set(QUEUE_FILE):
        thread_queue.put(link)
    thread_queue.join()
    crawl()


def create_crawlers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        url = thread_queue.get()
        crawler.Crawler.crawl_page(threading.current_thread().name, url)
        thread_queue.task_done()


def crawl():
    total_links = gf.get_number_of_urls_in_file(QUEUE_FILE) + gf.get_number_of_urls_in_file(CRAWLED_FILE)
    if total_links >= MAX_URLS:
        pass

    queued_links = gf.file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + " links remaining in the queue")
        create_jobs()


create_crawlers()
crawl()
