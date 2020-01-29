# Web Crawler in Python

### Description
Given a URL, the application searches the HTML of given page and identifies all the \<a> tags within them.
The href value of the tags are gathered up until the maximum threshold is reached or all URLs for the domain are found. By default, all of the URLs found will be printed to the terminal, each URL on a separate line. This can be changed
using the flags.

There are a variety of options to alter the functionality of the application, which can be determined using command line
flags, detailed below.

### Flags
* -h or --help: Print off descriptions of the necessary parameters and optional flags
* -M M: Set the maximum number of URLs M that the crawler will search for. Default is 100.
* -v: Verbose flag, set to print off status of the crawler. Otherwise, the crawler will print nothing other than the output.
* -o: Write all of the output URLs to a file in the local directory instead of the terminal
* -O O: Write the output to a file specified by O.
* -t T: Number of threads used to run the application. Default is 1. Set for 5+ if a large number of URLs are to be searched for
