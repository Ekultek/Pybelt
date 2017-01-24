import hashlib


class HashCracker(object):

    results = {
        'f8d3b312442a67706057aeb45b983221afb4f035': ['test', 'sha']
    }

    def __init__(self, hash, word, type=None):
        self.hash = hash
        self.word = word
        self.type = type

    def try_all_algorithms(self):
        for alg in hashlib.algorithms_available:
            data = hashlib.new(alg)
            data.update(self.word)
            self.results[data.hexdigest()] = [self.word, alg]
        return self.results

    def verify_hashes(self):
        for h in self.results.keys():
            if self.hash == h:
                return "Hash: {}\nAlgorithm: {}\nPlain Text: {}".format(self.hash,
                                                                        self.results[self.hash][1],
                                                                        self.results[self.hash][0])


print HashCracker("f8d3b312442a67706057aeb45b983221afb4f035", "").verify_hashes()
