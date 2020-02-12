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

def getIndividuals(html):
    a = []
    for i in html.find(lambda tag: tag.name == 'div' and tag.get('class') == ['content']).find_all('a', href=True):
        a.append(i['href'])
    return a

def add_all(url, csvfile):
    html1 = BeautifulSoup(simple_get(url), 'html.parser')
    a = []
    for i in html1.find_all('a', class_ = 'media-content'):
        a.append('http://azpreps365.com' + i['href'])
    for i in a:
        html2 = BeautifulSoup(simple_get(i), 'html.parser')
        surl = 'http://azpreps365.com' + html2.find('div', class_ = 'tabs').find_all('li', class_ = 'menu-item')[1].a['href']
        html3 = BeautifulSoup(simple_get(surl), 'html.parser')
        rurl = 'http://azpreps365.com' + html3.find_all(lambda tag: tag.name == 'li' and tag.get('class') == [''])[-1].a['href']
        print(rurl)
        add_info(rurl, csvfile)
def add_info(url, csvfile):
    htmlf = BeautifulSoup(simple_get(url), 'html.parser')
    urls = getIndividuals(htmlf)
    for sites in urls:
        raw_h = simple_get(sites)
        if raw_h is None:
            print(url + ': Invalid Roster')
            break
        html = BeautifulSoup(raw_h, 'html.parser')
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
        for name, score in zip(a, b):
            score = score.replace('-', ',')
            csvfile.write(f'{player}, {name}, {score}\n')

def date_collect(url, csvfile):
    htmlf = BeautifulSoup(simple_get(url), 'html.parser')
    a = (get_match_links(htmlf))
    for match in a:
        raw_h = simple_get(match)
        if raw_h is None:
            print(url + ': Invalid Stuff')
            break
        html = BeautifulSoup(raw_h, 'html.parser')
        match_collect(html, csvfile)

def match_collect(html, csvfile):
    playerh = []
    playera = []
    scores = []
    singles = True
    for i in html.find_all(lambda tag: tag.name == 'div' and 
                                    tag.get('class') == ['card']):
            count = -1
            for j in i.find_all(lambda tag: tag.name == 'span' and 
                                    tag.get('class') == ['players']):
                a_tags = j.find_all('a')
                h1 = ''
                a1 = ''
                for z in a_tags:
                    count += 1
                    if (singles):
                        if (count % 2 == 0):
                            playerh.append(z.get_text().strip())
                           # print('even')
                        else:
                            playera.append(z.get_text().strip())
                           # print('odd')
                    else:
                        if (count % 4 == 0):
                            h1 = z.get_text().strip() + ', '
                        elif (count % 4 == 1):
                            h1 = h1 + z.get_text().strip()
                            playerh.append(h1)
                            h1 = ''
                        elif (count % 4 == 2):
                            a1 = z.get_text().strip() + ', '
                        else:
                            a1 = a1 + z.get_text().strip()
                            playera.append(a1)
                            a1 = ''
            for j in i.find_all('div', class_ = 'column is-4 has-text-centered set-scores'):
                scores.append(j.get_text().strip())
            singles = False
    for ph, pa, score in zip(playerh, playera, scores):
        score = score.replace('-', ',')
        csvfile.write(f'{ph}, {pa}, {score}\n')
def get_match_links(html):
    a = []
    for i in html.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['result-summary']):
        a.append('http://azpreps365.com' + i.find('a').get('href'))
    return a
