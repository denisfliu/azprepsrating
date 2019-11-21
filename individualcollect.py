#!/usr/bin/env python
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup 

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def get_doubles_partner(str):
    word_list = str.split(' ')
    if len(word_list) > 3:
        return word_list[-2] + ' ' + word_list[-1]
    return ''
'''
def get_name(str):
    word_list = str.split(' ')
    return word_list[:2]
'''
def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

if __name__ == "__main__":
    while True:
        print('Enter individual url or enter 0 to stop: ')
        url = input()
        if url == '0':
            break
        else:
            raw_html = simple_get(url)
            html = BeautifulSoup(raw_html, 'html.parser')
            player = html.find('h4', class_ = 'title is-3').get_text().strip()
            a = []
            b = []
            for i in html.find_all(lambda tag: tag.name == 'div' and 
                                        tag.get('class') == ['card']):
                dubs = get_doubles_partner(i.find('div', class_ = 'card-header-title').get_text().strip())
                for j in i.find_all(lambda tag: tag.name == 'div' and 
                                        tag.get('class') == ['column']):
                    a_tags = j.select('a')
                    a.append(dubs + ', ' + ', '.join([k.get_text().strip().replace('											', '').replace('\n', ' ') for k in a_tags[:len(a_tags) - 1]]))
                for j in i.find_all('div', class_ = 'column is-3 result'):
                    b.append(j.get_text().strip())
            
            '''
            for i, p in enumerate(html.select('p')):
                a.append(p.text)  
            del a[0:16]
            scores = []
            for i in html.find_all('div', class_ = 'column is-3 result'):
                scores.append(i.get_text())
            index = 0
            for i in range(0, len(a)):
                if i % 4 == 3:
                    a.insert(i, scores[index])
                    index = index + 1
            '''
            with open('data.csv', 'a') as csvfile:
                for name, score in zip(a, b):
                    score = score.replace('-', ',')
                    csvfile.write(f'{player}, {name}, {score}\n')  