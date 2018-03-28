from os import listdir
from urllib.parse import urlparse, urlunparse, parse_qs
import re
import os
import collections
import shutil
import cgi
import json
import requests
import rfc6266


Media = collections.namedtuple('Media', 'url unix_time')

def get_post_file(post):
    if 'file' in post:
        return Media(
            url=post['file'].get('url_private_download'),
            unix_time=int(float(post['ts']))
        )

def get_post_attachments(post):
    if 'attachments' in post:
        return [
            Media(
                url=attachment.get('image_url'),
                unix_time=int(float(post['ts']))
            ) for attachment in post['attachments']
        ]

def collect_medias_from_file(file_path):
    with open(file_path, 'r', encoding='utf8') as f:
        d = json.loads(f.read())
        medias = []
        for post in d:
            post_file = get_post_file(post)
            medias += [post_file] if post_file is not None else []
            attachments = get_post_attachments(post)
            medias += attachments if attachments is not None else []
    return medias

def collect_medias_from_directory(directory):
    json_files = listdir(directory)
    directory_medias = []
    for json_file in json_files:
        urls = collect_medias_from_file(directory + json_file)
        directory_medias += urls if urls is not None else []
    return directory_medias

def strip_url_queries(url):
    u = urlparse(url)
    u = u._replace(query=None)
    return urlunparse(u)

def get_url_queries(url):
    u = urlparse(url)
    queries = parse_qs(u.query)
    return queries

def get_filename_from_request(r):
    filename = rfc6266.parse_requests_response(r).filename_unsafe
    extention = re.search('\.\w\w\w$', filename)
    if extention:
        return filename
    else:
        try:
            value, params = cgi.parse_header(r.headers['Content-Disposition'])
            return params.get('filename') or params.get('filename*').replace("UTF-8''", '')
        except KeyError:
            assert get_url_queries(r.url), 'No filename could be extracted'
            url = strip_url_queries(r.url)
            r = requests.get(url, stream=True)
            return get_filename_from_request(r)

def download_media(media, download_directory):
    r = requests.get(media.url, stream=True)
    assert r.status_code == requests.codes.ok, r.status_code
    filename = get_filename_from_request(r)
    full_path = download_directory + filename
    print(f'Downloading {media.url} to {full_path}')
    with open(full_path, 'wb') as f:
        for chunk in r:
            f.write(chunk)
    os.utime(full_path, (media.unix_time, media.unix_time))

def download_all(directory, download_directory):
    directory_medias = collect_medias_from_directory(directory)
    failed_urls = []
    for media in directory_medias:
        if media.url:
            try:
                download_media(media, download_directory)
            except (AssertionError, requests.exceptions.ConnectionError) as e:
                failed_urls += [(media.url, str(e))]
    if failed_urls:
        print(f'Failed urls: {failed_urls}')

download_all('c:\\users\\adam\\Downloads\\slack_export\\training\\', \
             'c:\\users\\adam\\Downloads\\slack_export_extraction\\training\\')
