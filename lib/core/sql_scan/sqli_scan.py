import urllib2
import random
from urlparse import urlparse
from bs4 import BeautifulSoup
from lib.core.settings import RANDOM_COMMON_COLUMN
from lib.core.settings import SQLI_ERROR_REGEX


class SQLiScanner(object):

    """ Scan a URL for SQL injection possibilities. """

    vulnerable = False

    def __init__(self, url):
        self.url = url
        self.int = random.randint(1, 13)
        self.error_syntax = ["'", "--", ';', '"', "/*", "'/*", "'--", '"--', "';", '";', '`',
                             " AND %i=%i" % (self.int, self.int),
                             " OR %i=%i" % (self.int, self.int),
                             " union false {}".format(RANDOM_COMMON_COLUMN.strip()),
                             " UNION {}".format(RANDOM_COMMON_COLUMN.strip())]

    @staticmethod
    def obtain_inject_query(url):
        return urlparse(url).query

    def add_injection_syntax_to_url(self):
        results = set()
        for syntax in self.error_syntax:
            results.add(self.url + syntax)

        return results

    def sqli_search(self):
        """ Search for SQL injection in the provided URL[error based injection] """
        while self.vulnerable is not True:
            for url in self.add_injection_syntax_to_url():
                query = self.obtain_inject_query(url)
                data = urllib2.urlopen(url).read()
                soup = [BeautifulSoup(data, 'html.parser')]
                for html in soup:
                    for regex in SQLI_ERROR_REGEX:
                        if regex.findall(str(html)):
                            self.vulnerable = True
                            return "%s appears to have a SQL injection vulnerability at %s" % (
                                    self.url, query)
        if self.vulnerable is False:
            return "%s is not vulnerable to SQL injection." % self.url
