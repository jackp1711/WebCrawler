from Spider import domain
from Spider import crawler_manager


print("Thank you for running the WebCrawler application. Please enter the URL of the website you would like to crawl:")
input1 = input()
HOMEPAGE = str(input1)
DOMAIN_NAME = domain.get_domain_name(HOMEPAGE)
PROJECT_NAME = DOMAIN_NAME

MAX_URLS = 100
NUMBER_OF_THREADS = 1
print("Beginning crawl. Application will gather the first " + str(MAX_URLS) + " urls found")

manager = crawler_manager.CrawlerManager(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME, MAX_URLS, NUMBER_OF_THREADS)
manager.run()