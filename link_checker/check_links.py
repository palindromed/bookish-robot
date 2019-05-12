import os, codecs
from bs4 import BeautifulSoup
import markdown
import requests


def get_filenames(dir_path):
    return os.listdir(dir_path)


def read_md_file(file_path):
    with codecs.open(file_path, mode="r", encoding="utf-8") as f:
        text = f.read()
    return text


def md_to_html(md_string):
    return markdown.markdown(md_string)


def html_parse(html, tag):
    output = set()
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find_all(tag)
    for link_tag in tags:
        link = link_tag.get("href")
        if link[:4] == "http":
            output.add(link)
    return output


def test_link_get(link):
    r = requests.get(link)
    return r.status_code


def main(dir_path):
    final_links = set()
    file_list = get_filenames(dir_path)
    for md_file in file_list:
        text = read_md_file(dir_path + md_file)
        html = md_to_html(text)
        links = html_parse(html, "a")
        final_links = final_links | links
    for link in final_links:
        status = test_link_get(link)
        if status > 203:
            print(link, status)
        else:
            print("Good link: {}, {}".format(link, status))


if __name__ == "__main__":
    dir_path = ""
    main(dir_path)
