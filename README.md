# Web Crawler in Python

Given a URL, the application searches the HTML of given page and identifies all the \<a> tags within them.
The href value of the tags are gathered up until the maximum threshold is reached or all URLs for the domain are found. By default, all of the URLs found will be printed to the terminal, each URL on a separate line. This can be changed
using the flags.

There are a variety of options to alter the functionality of the application, which can be determined using command line
flags, detailed below.

## Getting started
These instructions wil allow you to set up and run the web crawler, as well as altering the options available

###Prerequisites
The python language is required to run this project. There are no other external libraries necessary.

###Installing
Run the following command within the WebCrawler directory.
```
python main.py url [flags]
```
Where URL is the link you would like to start crawling, and the flags are the optional flags detailed below.

### Flags
* -h or --help: Print off descriptions of the necessary parameters and optional flags
* -M M: Set the maximum number of URLs M that the crawler will search for. Default is 100.
* -v: Verbose flag, set to print off status of the crawler. Otherwise, the crawler will print nothing other than the output.
* -o: Write all of the output URLs to a file in the local directory instead of the terminal
* -O O: Write the output to a file specified by O