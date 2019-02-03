import re
import requests
from bs4 import BeautifulSoup

class PictureGrabber:
    def __init__(self, website):
        self.pics = []
        self.site = website
        self.response = requests.get(self.site)
        #print(self.response.text)
        soup = BeautifulSoup(self.response.text, 'html.parser')
        img_tags = soup.find_all('img')

        self.urls = [img['src'] for img in img_tags]
        #print(self.urls)

    def geturls(self):
        # for url in self.urls:
        #     self.filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
        #     with open(self.filename.group(1), 'wb') as f:
        #         if 'http' not in url:
        #             url = '{}{}'.format(self.site, url)
        #             self.pics.append(url)
        #         self.response = requests.get(url)
        #
        # print(self.pics)
        for url in self.urls:
            if (re.match(r'.+[.](jpg|png)', url) == None):
                self.urls.remove(url)
        return self.urls

#thing = PictureGrabber('http://web.mit.edu/torralba/www/database.html')
#thing.geturls()