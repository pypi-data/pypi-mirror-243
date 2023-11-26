import random
from collections import namedtuple
from hashlib import sha256

import pytest

from syamaguc.utils.KVS import KVS

dummy_urls = [f"{k:04d}" for k in range(1000)]
dummy_title = "title"
dummy_html = """
 <html>
   <body>
     <div>
       <h1> Hello World </h1>
     </div>
   </body>
 </html>
 """


class TestKVS:
    @pytest.fixture(scope="class")
    def kvs(self):
        kvs = KVS()
        Datum = namedtuple("Datum", ["title", "html"])
        for dummy_url in dummy_urls:
            if kvs.is_exists(dummy_url) is True:
                continue
            dummy_title = "title"
            dummy_html = """
            <html>
              <body>
                <div>
                  <h1> Hello World </h1>
                </div>
              </body>
            </html>
            """
            datum = Datum(title=dummy_title, html=dummy_html)
            kvs.flash(dummy_url, datum)
        yield kvs
        kvs.cleanup()

    def test_is_exists(self, kvs):
        for dummy_url in dummy_urls:
            if kvs.is_exists(dummy_url) is False:
                AssertionError()

    def test_get(self, kvs):
        for dummy_url in dummy_urls:
            datum = kvs.get(dummy_url)
            if datum is None or datum.title != dummy_title or datum.html != dummy_html:
                AssertionError()

    def test_get_digest(self, kvs):
        assert kvs.get_digest("https://syamaguc.dev") == sha256(bytes("https://syamaguc.dev", "utf8")).hexdigest()[:24]
        assert kvs.get_digest("http://syamaguc.dev") != sha256(bytes("https://syamaguc.dev", "utf8")).hexdigest()[:24]

    def test_random(self, kvs):
        Datum = namedtuple("Datum", ["title", "html"])
        for _ in range(10000):
            dummy_url = random.choice(dummy_urls)
            if kvs.is_exists(dummy_url) is True:
                continue
            datum = Datum(title=dummy_title, html=dummy_html)
            kvs.flash(dummy_url, datum)
