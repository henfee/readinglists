import sys
sys.path.append('/Users/exu/PlayGround/readinglists/')

from key.keys import *
from amazon.api import AmazonAPI


import re
pattern = re.compile("https?://.*amazon.com/gp/product/([0-9]+)/.*")

amazon = AmazonAPI(AMAZON_ACCESS_KEY_ID, AMAZON_SECRET_ACCESS_KEY, AMAZON_ASSOC_TAG, MaxQPS=0.9)

def get_asin(url):
    global pattern
    m = pattern.match(url)
    if m and len(m.groups()) > 0:
        return m.groups()[0]

def read_file():
    if (len(sys.argv) < 1):
        print "need to supply a file name"
        sys.exit(-1)
    fname = sys.argv[1]
    f = open(fname, 'r')
    for l in f.readlines()[:4]:
        product = amazon.lookup(ItemId=get_asin(l))
        print product.title

if __name__ == '__main__':
    read_file()
