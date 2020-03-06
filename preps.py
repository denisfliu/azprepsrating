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
    winner = []
    for i in html.select('div[class*="column is-4 has-text-centered team is-winner"]'):
        winner.append((i["class"][-1]))
    for i in html.find_all(lambda tag: tag.name == 'div' and 
                                    tag.get('class') == ['card']):
            count = -1
            for j in i.select('div[class*="column is-4 has-text-centered team"]'):
                count += 1
                for k in j.find_all(lambda tag: tag.name == 'span' and 
                                    tag.get('class') == ['players']):
                    a_tags = k.find_all('a')
                    if not a_tags:
                        print("Forfeit???")
                    z = ''
                    for stuff in a_tags:
                        if z == '':
                            z = stuff.get_text().strip()
                        else:
                            z = z + ',' + stuff.get_text().strip()
                    if (count % 2 == 0):
                        playerh.append(z)
                    else:
                        playera.append(z)
            num = 0
            for j in i.find_all('div', class_ = 'column is-4 has-text-centered set-scores'):
                try:
                    if (winner[num] == 'is-away'):
                        scores.append(j.get_text().strip())
                    else:
                        scores.append(reverse_order(j.get_text().strip()))
                    num += 1
                except IndexError:
                    print(':(')
            singles = False
    for ph, pa, score in zip(playerh, playera, scores):
        score = score.replace('-', ',')
        csvfile.write(f'{ph}, {pa}, {score}\n')
def reverse_order(score):
    arr = score.split(',')
    if (len(arr) < 3):
        return ','.join(arr)[::-1]
    else:
        return arr[0][::-1] + ', ' + arr[1][::-1] + ', ' + '-'.join(arr[2].split('-')[::-1])
def get_match_links(html):
    a = []
    for i in html.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['result-summary']):
        a.append('http://azpreps365.com' + i.find('a').get('href'))
    return a
