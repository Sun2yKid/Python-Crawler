import requests
from requests.exceptions import RequestException

from bs4 import BeautifulSoup


def fetch_page(url):
    filename = 'result.html'
    try:
        headers = {'user-agent': 'my-app/0.0.2'}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:  # requests.codes.ok
            with open(filename, 'wb') as fd:
                for chunk in r.iter_content(chunk_size=128):
                    fd.write(chunk)
        else:
            print('status_code', r.status_code)
    except RequestException as e:
        print('RequestException', e)
    except Exception as e:
        print(e)


def fetch_page_and_parse(url):
    headers = {'user-agent': 'my-app/0.0.1'}
    try:
        global films_info
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            s = BeautifulSoup(r.text, "lxml")
            a_tag = s.ol.find_all('a')
            for i in range(0, len(a_tag), 2):
                name = a_tag[i].img.get('alt')
                href = a_tag[i].get('href')
                src = a_tag[i].img.get('src')
                roles = a_tag[i].find_next("p")
                films_info.append(dict(name=name, href=href, src=src, roles=' '.join(roles.text.split())))
        else:
            print('status_code', r.status_code)
    except RequestException as e:
        print('RequestException', e)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # url = 'https://movie.douban.com/top250'
    # fetch_page(url)

    base_url = 'https://movie.douban.com/top250'
    all_pages = [base_url + '?start=%d' % (i*25) for i in range(10)]

    films_info = []

    for url in all_pages:
        print('url', url)
        fetch_page_and_parse(url)

    with open('result.md', 'w', encoding='utf-8') as f:
        rank = 0
        for film in films_info:
            rank += 1
            f.write('[%02d. %s](%s)\n\n' % (rank, film['name'], film['href']))
            f.write('%s\n\n' % film['roles'])
            f.write('![%s](%s)\n\n' % (film['name'], film['src']))
