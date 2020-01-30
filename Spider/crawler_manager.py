import threading
from queue import Queue
from Spider import crawler
from Spider import general_functions as gf

"""
    CrawlerManager is a class that aims to manage how many URLs are searched for and stops all processes when the
    desired number is reached.
    Determine the output type of the program. Default will print to the console, but an output file can be written
    Controls the options given by the flags from the command line.
"""


class CrawlerManager:

    def __init__(self, project_name, homepage, domain_name, domain_flag, max_urls, v_flag, o_flag, o_file):
        self.queue = Queue()
        self.PROJECT_NAME = project_name
        self.HOMEPAGE = homepage
        self.DOMAIN_NAME = domain_name
        self.DOMAIN_FLAG = domain_flag
        self.MAX_URLS = max_urls
        self.QUEUE_FILE = self.PROJECT_NAME + '/queue.txt'
        self.CRAWLED_FILE = self.PROJECT_NAME + '/crawled.txt'
        self.VERBOSE_FLAG = v_flag
        self.OUTPUT_FLAG = o_flag
        self.OUTPUT_FILE = o_file

        self.visited = []
        self.crawled = []

        crawler.Crawler(project_name, homepage, domain_name, max_urls)

    # Run function places the first item in the queue and begins the process of searching through the first URL
    # The first item is the URL passed through by the user when initially calling the program
    def run(self):
        self.queue.put(self.HOMEPAGE)
        self.work()
        self.finalise()
        gf.remove_files(self.PROJECT_NAME)

    # Function to transform the list of URLs into the designated output type.
    def finalise(self):
        output = self.visited
        if self.OUTPUT_FLAG:
            gf.create_output_file(output, self.OUTPUT_FILE)
        else:
            gf.print_to_console(output)

    # Main work function that takes URLs from the queue and processes them, retrieving the pages URLs.
    # While loop breaks when either the queue is empty, or the desired number of URLs are found, exiting the function.
    def work(self):
        while True:
            current_url = self.queue.get()
            if current_url is None:
                break

            if current_url in self.crawled:
                while current_url in self.crawled:
                    current_url = self.queue.get()

            links = crawler.Crawler.gather_links(current_url)

            # If the domain flag is set, all links that do not have the domain of the input URL will be discarded.
            if self.DOMAIN_FLAG:
                links = self.filter_links_by_domain(links)

            links = self.filter_links(links)

            if len(links) + len(self.visited) >= self.MAX_URLS:
                self.visited.extend(links[:self.MAX_URLS - len(self.visited)])
                while not self.queue.empty():
                    self.queue.get()
                    self.queue.task_done()
                self.print_status(current_url)
                break
            else:
                for link in links:
                    if len(self.visited) < self.MAX_URLS:
                        if link not in self.visited:
                            self.visited.append(link)
                            self.queue.put(link)
            self.print_status(current_url)

            self.crawled.append(current_url)
            self.queue.task_done()

    # Function that, If the verbose flag is set, the status of the process after each page crawled will
    # be printed to the console.
    def print_status(self, current_url):
        if self.VERBOSE_FLAG:
            print("Current URL scanned: ", current_url)
            print("Number of sites found so far: ", len(self.visited))
            print("Sites remaining: ", self.MAX_URLS - len(self.visited))

    # Method to ensure that removes all duplicate links from the input list and returns a list of unique URLs.
    def filter_links(self, links):
        filtered_links = list()
        for url in links:
            if url in filtered_links or url in self.visited:
                continue
            else:
                filtered_links.append(url)
        return filtered_links

    # Function to filter the input list of links by the domain name.
    def filter_links_by_domain(self, links):
        filtered_links = list()
        for url in links:
            if self.DOMAIN_NAME in url:
                filtered_links.append(url)
        return filtered_links
