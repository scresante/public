#!/usr/bin/python
## This script downloads every image from the nasa image of the day archive
## to use, run python getapod.py

## requires beautifulsoup, to install
## pip install BeautifulSoup
from bs4 import BeautifulSoup as bs
import os
import re
import urllib

# require magic for filetype ident
import magic

class fIdent:
    mym = False
    def __init__(self):
        self.mym = self.build_magic()
    def build_magic(self):
        try:
          mymagic = magic.open(magic.MAGIC_MIME_TYPE)
          mymagic.load()
        except AttributeError,e:
          mymagic = magic.Magic(mime=True)
          mymagic.file = mymagic.from_file
        return(mymagic)
    def type(self,fname):
        return self.mym.file(fname)

f = fIdent()

if not os.path.isdir('images'):
    os.mkdir('images')

frontpage = urllib.urlopen('http://apod.nasa.gov/apod/archivepix.html')
h = frontpage.read()
base_url = 'http://apod.nasa.gov/apod/'
links = []
images = []

for q in re.findall(r'<a href="ap.{6}\.html', h):
    links.append(base_url + q.split('"')[1])

def getimage(url):
    s = bs(urllib.urlopen(url).read())
    print '---------'
    print os.path.basename(url)
    alinks = s.find_all('a');
    for alink in alinks:
        try:
            if 'jpg' in alink.attrs['href']:
                src = alink.attrs['href']
                fpath = 'images/' + os.path.basename(src)
                if not os.path.isfile(fpath):
                    urllib.urlretrieve(base_url+src, fpath)
                    if f.type(fpath).split('/')[0] != 'image':
                        print('%s is not an image' % fpath)
                        os.unlink(fpath)
                    else:
                        print('downloaded %s' % fpath)
                else:
                    print('%s already exists' % fpath)
        except KeyError, AttributeError:
            print 'no image found'
        #except:
            #print 'other error'
def makelist(url):
    s = bs(urllib.urlopen(url).read())
    print url
    try:
        img = s.find('img').attrs['src']
        fpath = 'images/' + os.path.basename(img)
        if not os.path.isfile(fpath):
            return base_url+img
        else:
            return
    except:
        return

def cleandir(dirname = 'images/'):
    crem =0
    for fpath in os.listdir(dirname):
        fpath = os.path.join(dirname, fpath)
        #print('name: %s  _  type: %s' % (fpath, f.type(fpath))) 
        if f.type(fpath).split('/')[0] != 'image':
            crem += 1
            print('%s is not image, delete' % fpath)
            os.unlink(fpath)
        elif os.stat(fpath).st_size < 120000:
            print('%s is too small (<120K)' % fpath)
            os.unlink(fpath)
            crem += 1
    print('removed %s files' % crem)

# limiter for partial redownload, set last to ap #
last = '101392'
last = False
if last:
    fin=[links.index(q) for q in links if q.find(last) != -1 ][0]
    links = links[fin+1:]

if __name__ == '__main__':
    for link in links:
        getimage(link)
    cleandir()
