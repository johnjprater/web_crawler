import gevent
# I think the idea here is to patch functions and classes in the standard library with 'cooperative'
# counterparts.
from gevent import monkey
monkey.patch_all()

# lightweight library for http requests amongst other things
import requests
from collections import defaultdict
import re

# For parsing urls cleanly
from urllib.parse import urlparse


class WebCrawler():
    ''' simple web crawler '''

    def __init__(self):
        self.webpage_structure = defaultdict(set)

    def crawl_domain(self, url):
        ''' TODO '''
        greenlet = gevent.Greenlet.spawn(self._crawl_page, url)
        # Wait for the greenlet spawned above to finish. This inculdes all of the greenlets spawned
        # by this, because of the joinall below
        gevent.wait([greenlet])
        return self.webpage_structure

    def _crawl_page(self, url):
        ''' The idea is to recursively crawl a new page on the domain as soon as its identified '''
        url_domain = urlparse(url).netloc
        url_path = urlparse(url).path
        domain_and_path = url_domain + url_path

        # Make an http request to the given url. There are a variety of cases, like an image for
        # example, where we won't get a 200 response. We assume that this isn't a valid page and
        # record the hyperlinks leading from this page as an empty set
        r = requests.get(url)

        # Usually 200 but any http code with the first digit equal to 2 should be fine.
        if str(r.status_code).startswith('2'):
            page_content = r.text
            # Look for hyperlinks in the HTML using a basic regex
            hyperlinks = re.findall('href="(.*?)"', page_content)
            greenlet_list = []
            for hyperlink in hyperlinks:
                hyperlink_domain = urlparse(hyperlink).netloc
                hyperlink_path = urlparse(hyperlink).path
                if not hyperlink_domain:
                    hyperlink_domain = url_domain
                    # Sometimes the / is missing
                    if not hyperlink_path.startswith('/'):
                        hyperlink_path = '/' + hyperlink_path
                
                new_domain_and_path = hyperlink_domain + hyperlink_path
                self.webpage_structure[domain_and_path].add(new_domain_and_path)

            # All hyperlinks we find in the domain are asyncronously crawled once we've finished
            # looking through the page
            for new_domain_and_path in self.webpage_structure[domain_and_path]:
                hyperlink = f'https://{new_domain_and_path}'
                hyperlink_domain = urlparse(hyperlink).netloc
                if (
                    hyperlink_domain == url_domain and
                    new_domain_and_path not in self.webpage_structure
                ):
                    greenlet_list.append(gevent.Greenlet.spawn(self._crawl_page, hyperlink))
            # Wait for all of the greenlets spawned above to finish before allowing the current
            # greenlet to finish
            gevent.joinall(greenlet_list)
        else:
            self.webpage_structure[url_domain + url_path] = set()

if __name__=='__main__':
    url = 'https://news.ycombinator.com/'

    webpage_structure = WebCrawler().crawl_domain(url)

    string_to_print = ''
    for src_page, linked_pages in webpage_structure.items():
        # Don't add lots of new lines when linked_pages is the empty set
        if linked_pages:
            for dst_page in linked_pages:
                string_to_print += f'{src_page} -> {dst_page}\n'
            string_to_print += '\n'

    print(string_to_print)
