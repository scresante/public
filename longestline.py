#!/usr/bin/python
from sys import argv
fname=argv[1]
with open(fname, 'r') as f:
    pf = f.readlines()
    longestlinenum = sorted( [ (i, len(v)) for (i,v) in enumerate(pf) ], key=lambda x:x[1], reverse=True)[0]
    #del(pf[longestlinenum[0]])
    print('line #'+str(longestlinenum[0])+' of length '+str(longestlinenum[1]))
    #f.seek(0)
    #f.writelines(pf)
    #f.truncate()
#with open(fname, 'r+') as f:
    #pf = f.readlines()
    #longestlinenum = sorted( [ (i, len(v)) for (i,v) in enumerate(pf) ], key=lambda x:x[1], reverse=True)[0]
    #del(pf[longestlinenum[0]])
    #print('removed line #'+str(longestlinenum[0])+' of length '+str(longestlinenum[1]))
    #f.seek(0)
    #f.writelines(pf)
    #f.truncate()


# Various methods that didn't work too well
#longestline = ( [ i for (i,v) in enumerate(pf) if v==max(pf) ] )

#longestline = (pf.index(max(pf)))

#from itertools import count
#longestline = (max(zip(pf,count()))[1])

#longestline = (sorted( [ (len(l),l) for l in pf ], reverse=True)[0])
# longestlinenum = (sorted( [ (len(v),i+1) for (i,v) in enumerate(pf) ], reverse=True)[0])[1]
    #longestlines = (sorted( [ (i, len(v)) for (i,v) in enumerate(pf) ], key=lambda x:x[1], reverse=True)[0:10])
    #print(longestlines)
    #for i in longestlines:
        #pf[i[0]]=''
