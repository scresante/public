import bs4
import requests
import pickle
import os
from functools import partial
from time import sleep
from sys import exit

getsoup = partial(bs4.BeautifulSoup, features='lxml')

pfile = 'linkstore'

try:
    with open(pfile, 'rb') as fd:
        readlinks = pickle.load(fd)
except: # file is empty or doesn't exist, quickly make it 
    readlinks = set()
    with open(pfile, 'wb') as fd:
        pickle.dump(readlinks, fd)

def check_and_email(title, link):
    if link in readlinks:
        print(f'{link} was already in set, ignoring')
    else:
        #update set of links
        readlinks.add(link)
        print(f'new link: {link}')

def get_links():
    url = 'https://procure.ohio.gov/proc/searchProcOppsResults.asp?t1=ALLITOPPS&OSTAT=All&TITLE=ITOPPS'
    r = requests.get(url)
    soup = getsoup(r.text)
    all_the_a = soup.find_all('a')
    oa_a = [ _ for _ in all_the_a if _.text[0:2]=='0A' ] 
    links = [ a['href'] for a in oa_a ]

    for link in links:
        sleep(4)
        urlbase = 'https://procure.ohio.gov'
        r = requests.get(urlbase + '/' + link)
        soup = getsoup(r.text)
        title = ''
        pdfas = [ _ for _ in soup.find_all('a') if _.text[-3:]=='pdf' ]
        if pdfas:
            pdflink = pdfas[0]['href']
        else:
            pdflink = None
        # this is where stuff happens
        check_and_email(title, pdflink)


if __name__ == "__main__":
    get_links()
    with open(pfile, 'wb') as fd:
        print(f'processing complete, storing {readlinks} to {pfile}')
        pickle.dump(readlinks, fd)
