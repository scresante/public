import os
d = 'media/Incoming'
extensionList = ['.mp4', '.avi', '.mkv', '.flv']
def findExt(extList):
    for path,dirs,files in os.walk(d):
        for f in files:
            extension = os.path.splitext(f)[1]
            for ext in extList:
                if extension == ext:
                    print path,f

def listExt(here):
    extlist = {}
    for path,dirs,files in os.walk(here):
        for f in files:
            ext = os.path.splitext(f)[1]
            if not extlist.has_key(ext):
                extlist[ext] = 1
            else:
                extlist[ext] += 1
    return sorted(extlist.items(), key=lambda x: x[1], reverse=True)
    #return extlist
