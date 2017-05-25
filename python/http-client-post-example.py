#!/usr/bin/python
from random import randint
from json import loads
from time import time,sleep
import urllib.parse
import urllib.request
import urllib.error
class spamPoll:
    logfile = 'post.log'
    lastres = ''
    def __init__(self):
        pass
    def post(self,ans='idk'):
        resp = str(self.parse(self.send(ans)))
        t=time()
        if self.lastres != resp:
            print("%.1f: %s" % (t, resp))
            self.writelog(t,resp)
        else:
            print('.', end='', flush=True)
        self.lastres = resp
    def writelog(self,t,resp):
        logfile = 'post.log'
        f = open(self.logfile, mode='a')
        f.write( str(t) + ': ' + resp + '\n')
        f.close()
    def send(self,answer):
        answers = {'idk':"C789C5A2-2870-0001-4B901E201E8E10AB", 'no':'C789C5A1-8370-0001-62F65000AC3718EB','yes':'C789C5A0-BAF0-0001-AE6F118AE68EC600'}
        try:
            data = {'format':'json','action':'poll:vote','answer':answers[answer] }
        except KeyError:
            data = {'format':'json','action':'poll:vote','answer':answer }
        url = 'http://www.richmond.com/news/local/city-of-richmond/poll-should-richmond-remove-its-confederate-monuments/poll_70452265-9c50-587f-886e-10bcb46dd990.html'

        data = urllib.parse.urlencode(data)
        data = data.encode('ascii')
        with urllib.request.urlopen(url, data) as f:
            return f.read().decode('utf-8')
    def parse(self,j):
        res = loads(j)['results']
        return [ (q['text'],q['votes']) for q in res.values() ]
if __name__ == "__main__":
    s = spamPoll()
    while True:
        try:
            s.post()
            sleep(randint(3,6))
        except urllib.error.HTTPError:
            print('error occurred, sleeping')
            sleep(30)
