from requests import Session

class ScraperSession(Session):

    def __init__(self):
        super(ScraperSession, self).__init__()
        # self.headers = dict()
        self.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Origin': 'https://www.onlineupsrtc.co.in',
            'Referer': 'https://www.onlineupsrtc.co.in/'
        })