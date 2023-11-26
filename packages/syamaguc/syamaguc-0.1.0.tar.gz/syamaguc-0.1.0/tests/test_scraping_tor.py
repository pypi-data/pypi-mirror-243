from syamaguc.scraping.tor import tor_driver, trequests


class TestTor:
    def test_trequests(self):
        response = trequests("https://check.torproject.org/api/ip", verify=False)
        assert response.json()["IsTor"] is True

    def test_tor_driver(self):
        driver = tor_driver()
        driver.get("https://check.torproject.org/")
        title = driver.title.lower()
        if "congratulations" not in title:
            AssertionError()
