import sys

from key.keys import *
from amazon.api import AmazonAPI

if (len(sys.argv) < 1):
    print "need to supply a file name"
    sys.exit(-1)
fname = sys.argv[1]
f = open(fname, 'r')
for l in f:
    


amazon = AmazonAPI(AMAZON_ACCESS_KEY_ID, AMAZON_SECRET_ACCESS_KEY, AMAZON_ASSOC_TAG, MaxQPS=0.9)
product = amazon.lookup(ItemId='B00EOE0WKQ')
print product.title
print product.price_and_currency
print product.ean
print product.large_image_url
