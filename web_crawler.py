from Spider import domain
from Spider import crawler_manager
import argparse
from urllib import request

"""
    Main file that gathers all of the command line arguments and passes them into a CrawlerManager object.
    Identifies and passes appropriate values to the CrawlerManager taken from the commandline args.
"""


def main():
    parser = argparse.ArgumentParser(description="Web crawler to index a specified number of unique URLs given a starting web page")
    parser.add_argument('url', action="store", help="Start URL must be specified")
    parser.add_argument('-M', action="store", default=100, help="Specify the number of unique URLs to gather. Default is 100", type=int)
    parser.add_argument("-v", action="store_true", help="Enable this flag to print the progress of the crawler")
    parser.add_argument("-o", action="store_true", help="Store output in a local file")
    parser.add_argument("-O", action="store", help="Choose a file directory to store the results.", type=str)
    parser.add_argument("-d", action="store_true", help="Determine if the crawler should limit it's search to only the current domain")

    args = parser.parse_args()
    try:
        request.urlopen(args.url)
    except:
        print("URL entered is not a valid URL, please enter a valid URL of the form https://example.com")
        exit()

    HOMEPAGE = str(args.url)
    DOMAIN_NAME = domain.get_domain_name(HOMEPAGE)
    DOMAIN_FLAG = args.d
    PROJECT_NAME = DOMAIN_NAME
    MAX_URLS = args.M
    NUMBER_OF_THREADS = 1
    VERBOSE_FLAG = args.v
    OUTPUT_FLAG = False
    OUTPUT_FILE = ""

    if args.o:
        OUTPUT_FLAG = True
    if args.O:
        OUTPUT_FLAG = True
        OUTPUT_FILE = args.O

    manager = crawler_manager.CrawlerManager(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME, DOMAIN_FLAG, MAX_URLS, NUMBER_OF_THREADS, VERBOSE_FLAG, OUTPUT_FLAG, OUTPUT_FILE)
    manager.run()


if __name__ == "__main__":
    main()
