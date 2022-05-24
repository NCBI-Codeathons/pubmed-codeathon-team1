"""
An implementation of the Token Bucket algorithm
"""
# NOTE: This code was adapted from https://github.com/porterjamesj/tokenbucket/blob/master/tokenbucket.py,
#       but modified to add a backoff that appears to be needed on Windows.
import time
from threading import Lock
from requests import Session


__all__ = (
    'TokenBucket',
    'RateLimitedSession',
)


class TokenBucket(object):

    def __init__(self, rate=1, tokens=0, capacity=100):
        # immutable attributes
        self.lock = Lock()
        self._rate = rate
        self._capacity = capacity
        # mutable attributes
        self._tokens = tokens
        self._time = time.monotonic()

    @property
    def rate(self):
        return self._rate

    @property
    def capacity(self):
        return self._capacity

    def _adjust(self):
        """
        Update internal time and tokens
        """
        now = time.monotonic()
        elapsed = now - self._time

        self._tokens = min(
            self._capacity,
            self._tokens + elapsed * self._rate
        )
        self._time = now

    @property
    def tokens(self):
        """
        Publicly accessible view of how many tokens the bucket has.
        """
        with self.lock:
            self._adjust()
            return self._tokens

    def consume(self, tokens):
        """
        Consume `tokens` tokens from the bucket, blocking until they are
        available
        """
        with self.lock:
            self._adjust()
            self._tokens -= tokens
            backoff = 1
            while self._tokens < 0:
                to_sleep = backoff * (-self._tokens / self._rate)
                time.sleep(to_sleep)
                self._adjust()
                backoff += 1


class RateLimitedSession(Session):
    def __init__(self, session=None, tokenbucket=None, rate=1, tokens=0, capacity=100, backoff=2.0,
                 *args, **kwargs):
        """Creates a TokenBucketSession

        Notes
        ~~~~~

        * If you provide a `tokenbucket`, then the `rate`, `tokens`, and `capacity` arguments are ignored.
        """
        super(RateLimitedSession, self).__init__(*args, **kwargs)
        if tokenbucket is None:
            tokenbucket  = TokenBucket(rate=rate, tokens=tokens, capacity=capacity)
        self.tokenbucket = tokenbucket
        self.session = session
        self.backoff = backoff

    def request(self, *args, **kwargs):
        """Maintains the existing api for Session.request.

        Used by all of the higher level methods, e.g. Session.get.
        """
        if self.session:
            func = self.session.request
        else:
            func = super(RateLimitedSession, self).request
        self.tokenbucket.consume(1)
        r = func(*args, **kwargs)
        if r.status_code == 429:
            time.sleep(self.backoff)
            r = func(*args, **kwargs)
        return r
