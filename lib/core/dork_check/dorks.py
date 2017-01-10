from lib.core import settings
from google import search
from lib.core.settings import LOGGER


class DorkScanner(object):

    """ Check your Google dorks to see if they actually will find sites that you want """

    def __init__(self, dork):
        self.dork = dork
        self.searchEngine = 'http://google.com'

    def connect_to_search_engine(self):
        """ Connect to Google and search for URLS """
        res = []
        limit = 100
        found = 0
        index = search(self.dork)
        while limit != 0:
            res.append(next(index))
            limit -= 1
            found += 1
        return res

    def check_urls_for_queries(self):
        """ The returned URLS will be run through a query regex to see if they have a query parameter
            http://google.com <- False
            http://example.com/php?id=2 <- True """
        filename = settings.create_random_filename()
        LOGGER.info("File being saved to: {}".format(filename))
        with open("{}\\{}.txt".format(settings.DORK_SCAN_RESULTS_PATH, filename), "a+") as results:
            for url in self.connect_to_search_engine():
                match = settings.QUERY_REGEX.match(url)  # Match by regex for anything that has a ?<PARAM>= in it
                if match:
                    results.write(url + "\n")
        amount_of_urls = len(open(settings.DORK_SCAN_RESULTS_PATH + "\\" + filename + ".txt", 'r').readlines())
        success_rate = ((amount_of_urls // 10) + 1) * 10
        return "Found a total of {} usable links with query (GET) parameters, urls have been saved to {}\\{}.txt. " \
               "This Dork has a success rate of {}%".format(amount_of_urls, settings.DORK_SCAN_RESULTS_PATH, filename,
                                                            success_rate)
