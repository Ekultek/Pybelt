import urllib


def tamper_payload(payload):
    """ Encode a payload into URL format
    >>> tamper("SELECT * FROM *")
    SELECT%20%2A%20FROM%20%2A """
    return urllib.quote(payload)
