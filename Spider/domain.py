from urllib.parse import urlparse

"""
    Set of functions to determine the high level domain name of a given URL.
"""


def get_domain_name(url):
    try:
        results = get_sub_domain(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''


def get_sub_domain(url):
    try:
        return urlparse(url).netloc
    except:
        return ''
