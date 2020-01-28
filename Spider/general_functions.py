import requests
import os


def create_project_dir(directory):
    if not os.path.exists(directory):
        print("Creating directory " + directory)
        os.makedirs(directory)


def create_data_files(domain_name, base_url):
    queue = domain_name + '/queue.txt'
    crawled = domain_name + '/crawled.txt'

    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')


def write_file(file_name, data):
    f = open(file_name, 'w')
    f.write(data)
    f.close()


def add_url_to_file(file_name, url):
    with open(file_name, 'a') as file:
        file.write(url + '\n')


def delete_contents(file_name):
    with open(file_name, 'w'):
        pass


def file_to_set(file_name):
    results = []
    with open(file_name, 'rt') as file:
        for line in file:
            results.append(line.replace('\n', ''))
    return results


def list_to_file(url_list, file_name):
    delete_contents(file_name)
    for url in sorted(url_list):
        add_url_to_file(file_name, url)


def get_number_of_urls_in_file(file_name):
    link_numb = len(open(file_name).readlines())
    return link_numb
