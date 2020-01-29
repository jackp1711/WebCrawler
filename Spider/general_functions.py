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


def create_output_file(file_1, file_2, new_file_name):
    if new_file_name is "":
        new_file_name = 'output_urls.txt'

    output = []
    with open(file_1, 'r') as file1:
        for line in file1:
            line = line.replace('\n', '')
            output.append(line)
    with open(file_2, 'r') as file2:
        for line in file2:
            line = line.replace('\n', '')
            output.append(line)

    write_file(new_file_name, "")
    list_to_file(output, new_file_name)


def print_to_console(file_1, file_2):
    with open(file_1, 'r') as f1:
        for line in f1:
            line = line.replace('\n', '')
            print(line)

    with open(file_2, 'r') as f2:
        for line in f2:
            line = line.replace('\n', '')
            print(line)
