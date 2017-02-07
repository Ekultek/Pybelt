import hashlib
from lib.core.settings import LOGGER
from lib.core.settings import HASH_TYPE_REGEX


class HashChecker(object):

    def __init__(self, check_hash):
        self.hash = check_hash
        self.found = False
        self.hash_type = None

    def obtain_hash_type(self):
        for alg in HASH_TYPE_REGEX.keys():
            if HASH_TYPE_REGEX[alg].match(self.hash):
                LOGGER.info("Possible hash type: {}".format(alg.upper()))
                return
        LOGGER.error("Unable to verify hash type for {}\nSupported hash types: {}".format(
                     self.hash, hashlib.algorithms_available))
