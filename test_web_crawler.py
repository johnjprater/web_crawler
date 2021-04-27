''' Quick test on a local cafe's website. Will break when they update it... '''
from web_crawler import WebCrawler
from time import perf_counter
from pprint import pformat
from urllib.parse import urlparse


if __name__=='__main__':
    # Some of these are useful for testing
    urls = [
        # 'https://news.ycombinator.com/',
        # 'https://www.google.com',
        'https://coffeeology.me.uk/',
        # 'https://www.example.com',
        # 'https://www.python.org',
        # 'https://http.cat'
    ]
    url = 'https://coffeeology.me.uk/'

    # start = perf_counter()

    webpage_structure = WebCrawler().crawl_domain(url)

    # # Start of some kind of unit test
    domain = urlparse(url).netloc
    set_of_links = set()
    for _, link_set in webpage_structure.items():
        set_of_links = set_of_links.union({x for x in link_set if domain in x})
    for link in set_of_links:
        assert link in webpage_structure.keys()

    assert set(webpage_structure.keys()) == {
        'coffeeology.me.uk/',
        'coffeeology.me.uk/account',
        'coffeeology.me.uk/account/login',
        'coffeeology.me.uk/account/register',
        'coffeeology.me.uk/cart',
        'coffeeology.me.uk/collections',
        'coffeeology.me.uk/collections/all',
        'coffeeology.me.uk/collections/all.atom',
        'coffeeology.me.uk/collections/coffeology-coffee-beans',
        'coffeeology.me.uk/collections/coffeology-coffee-beans.atom',
        'coffeeology.me.uk/collections/coffeology-coffee-beans.oembed',
        'coffeeology.me.uk/collections/equipment',
        'coffeeology.me.uk/collections/equipment.atom',
        'coffeeology.me.uk/collections/equipment.oembed',
        'coffeeology.me.uk/collections/merchandising',
        'coffeeology.me.uk/collections/merchandising.atom',
        'coffeeology.me.uk/collections/merchandising.oembed',
        'coffeeology.me.uk/pages/coffeeology',
        'coffeeology.me.uk/pages/coffeeology-london-locations',
        'coffeeology.me.uk/pages/contacts',
        'coffeeology.me.uk/search'
    }
