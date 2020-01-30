import threading
from queue import Queue
from Spider import crawler
from Spider import general_functions as gf


class CrawlerManager:

    def __init__(self, project_name, homepage, domain_name, domain_flag, max_urls, thread_number, v_flag, o_flag, o_file):
        self.thread_queue = Queue()
        self.PROJECT_NAME = project_name
        self.HOMEPAGE = homepage
        self.DOMAIN_NAME = domain_name
        self.DOMAIN_FLAG = domain_flag
        self.MAX_URLS = max_urls
        self.NUMBER_OF_THREADS = thread_number
        self.QUEUE_FILE = self.PROJECT_NAME + '/queue.txt'
        self.CRAWLED_FILE = self.PROJECT_NAME + '/crawled.txt'
        self.VERBOSE_FLAG = v_flag
        self.OUTPUT_FLAG = o_flag
        self.OUTPUT_FILE = o_file

        self.visited = []

        self.thread_list = []

        crawler.Crawler(project_name, homepage, domain_name, max_urls)

    def run(self):
        self.thread_queue.put(self.HOMEPAGE)
        self.work()
        self.set_up()
        self.thread_queue.join()
        for t in self.thread_list:
            self.thread_queue.put(None)
            t.join()
        self.finalise()
        gf.remove_files(self.PROJECT_NAME)

    def finalise(self):
        output = self.visited
        if self.OUTPUT_FLAG:
            gf.create_output_file(output, self.CRAWLED_FILE, self.OUTPUT_FILE)
        else:
            gf.print_to_console(output, self.CRAWLED_FILE)

    def set_up(self):
        for _ in range(self.NUMBER_OF_THREADS):
            t = threading.Thread(target=self.work)
            t.start()
            self.thread_list.append(t)

    def work(self):
        while True:
            current_url = self.thread_queue.get()
            if current_url is None:
                break

            links = crawler.Crawler.gather_links(current_url)
            if self.DOMAIN_FLAG:
                links = self.filter_links_by_domain(links)

            if len(links) + len(self.visited) >= self.MAX_URLS:
                self.visited.extend(links[:self.MAX_URLS - len(self.visited)])
                while not self.thread_queue.empty():
                    self.thread_queue.get()
                    self.thread_queue.task_done()
            else:
                for link in links:
                    if len(self.visited) < self.MAX_URLS:
                        self.visited.append(link)
                        self.thread_queue.put(link)

            if self.VERBOSE_FLAG:
                print("Current URL scanned: ", current_url)
                print("Number of sites found so far: ", len(self.visited))
                print("Sites remaining: ", self.MAX_URLS - len(self.visited))

            if len(self.thread_list) is 0:
                self.thread_queue.task_done()
                break
            self.visited = self.filter_links(self.visited)
            self.thread_queue.task_done()

    @staticmethod
    def filter_links(links):
        filtered_links = list()
        for url in links:
            if url in filtered_links:
                continue
            else:
                filtered_links.append(url)
        return filtered_links

    def filter_links_by_domain(self, links):
        filtered_links = list()
        for url in links:
            if self.DOMAIN_NAME in url:
                filtered_links.append(url)
        return filtered_links

    def tear_down(self):
        for _ in self.thread_list:
            self.thread_queue.put(None)
        for t in self.thread_list:
            t.join()
