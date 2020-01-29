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

            for table in s.find_all('a'):
                if 'nbg' in table.get('class', []):
                    next = table.find_next("a")
                    next_p = next.find_next("p")
                    books_info.append(dict(name=next['title'], src=table.img['src'], href=table['href'],
                                      author='/'.join(next_p.text.split('/')[:3])))
        else:
            print('status_code', r.status_code)
    except RequestException as e:
        print('RequestException', e)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # url = 'https://book.douban.com/top250'
    # fetch_page(url)

    base_url = 'https://book.douban.com/top250'
    all_pages = [base_url + '?start=%d' % (i*25) for i in range(10)]

    books_info = []

    for url in all_pages:
        print('url', url)
        fetch_page_and_parse(url)

    with open('result.md', 'w', encoding='utf-8') as f:
        rank = 0
        for book in books_info:
            rank += 1
            f.write('[%d. %s](%s)\n\n' % (rank, book['name'], book['href']))
            f.write('%s\n\n' % book['author'])
            f.write('<img src="%s" alt="%s" height="343px" width="231px"/>\n\n' % (book['src'], book['name']))
            # f.write('![%s](%s)\n\n' % (book['name'], book['src']))
