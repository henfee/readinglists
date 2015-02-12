import re
import string
import sys
sys.path.append('/Users/exu/PlayGround/readinglists/')

from key.keys import *
from amazon.api import AmazonAPI
from html2text import html2text

pattern = re.compile("https?://.*amazon.com/gp/product/([0-9]+)/.*")
amazon = AmazonAPI(AMAZON_ACCESS_KEY_ID, AMAZON_SECRET_ACCESS_KEY, AMAZON_ASSOC_TAG, MaxQPS=0.9)

def uprint(s):
    print s.encode('utf-8')

def get_asin(url):
    global pattern
    m = pattern.match(url)
    if m and len(m.groups()) > 0:
        return m.groups()[0]

def read_file():
    if (len(sys.argv) < 1):
        print "Please provide a file that includes a list of Amazon links."
        sys.exit(-1)
    fname = sys.argv[1]
    f = open(fname, 'r')
    products = []
    for l in f.readlines():
        product = amazon.lookup(ItemId=get_asin(l))
        products.append([product.title, product.editorial_review, product.large_image_url, product.offer_url])
        print "Got product", product.title
    return products

rtitle = re.compile('(.*)(\(.*\))')
def normalize_title(title):
    """ Book titles are long. We crop out the last part that is in (part)"""
    splits =  re.findall(rtitle, title)
    if splits:
        new_title = splits[0][0]
    else:
        new_title = title
    return new_title

def sanitize_text(t):
    s = html2text(t)
    s = string.replace(s, "'", "&rsquo;")
    s = string.replace(s, "**", "*")
    return s

if __name__ == '__main__':
    import os.path
    import cPickle
    pickle_file = 'products.pickle'
    products = None
    if os.path.isfile(pickle_file):
        products = cPickle.load(open(pickle_file, 'r'))
    else:
        products = read_file()    
        f = open(pickle_file, "wb")
        cPickle.dump(products, f)
    for product in products:
        title = normalize_title(product[0])
        uprint(title)
        print '=' * len(title)
        review = sanitize_text(product[1])
        uprint(review)
        print

