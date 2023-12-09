import sys
import requests
import time

sys.path.insert(1, '..')
import utils
import video

MOVIES = '34399'
SERIES = '83'


class Netflix():

    def __init__(self) -> None:
        self.movies = []
        self.series = []
        self.cookies = utils.getCookies('.netflix')

        self.headers = {
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'X-Netflix.osFullName': 'Windows 10',
        'x-netflix.nq.stack': 'prod',
        'X-Netflix.clientType': 'akira',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'X-Netflix.osName': 'Windows',
        'X-Netflix.esn': '',
        'X-Netflix.browserVersion': '118',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'X-Netflix.uiVersion': 'v6db6f478',
        'X-Netflix.esnPrefix': '',
        'x-netflix.request.client.user.guid': '',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Netflix.osVersion': '10.0',
        'X-Netflix.Client.Request.Name': 'ui/falcorUnclassified',
        'X-Netflix.browserName': 'Chrome',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
    }


    def payload(self, genre, f, t):
        return 'path=%5B%22genres%22%2C{}%2C%22az%22%2C%7B%22from%22%3A{}%2C%22to%22%3A{}%7D%2C%22itemSummary%22%5D&path=%5B%22genres%22%2C{}%2C%22az%22%2C%7B%22from%22%3A{}%2C%22to%22%3A{}%7D%2C%22reference%22%2C%5B%22availability%22%2C%22episodeCount%22%2C%22inRemindMeList%22%2C%22queue%22%2C%22summary%22%5D%5D'.format(genre, f, t, genre, f, t)


    def getSeriesData(self, id):
        time.sleep(0.005)
        return requests.request("GET", 'https://www.netflix.com/nq/website/memberapi/vca8af39d/metadata?movieid={}&imageFormat=webp&withSize=true&materialize=true&_=1699820978622'.format(id), headers=self.headers, cookies=self.cookies).json()['video']['seasons']


    def scrap(self, genre, f, t):
        url = "https://www.netflix.com/nq/website/memberapi/v6db6f478/pathEvaluator?webp=true&drmSystem=widevine&isVolatileBillboardsEnabled=true&isTop10Supported=true&isTop10KidsSupported=true&hasVideoMerchInBob=true&hasVideoMerchInJaw=true&falcor_server=0.1.0&withSize=true&materialize=true&original_path=%2Fshakti%2Fmre%2FpathEvaluator"
        
        response = requests.request("POST", url, headers=self.headers, data=self.payload(genre, f, t), cookies=self.cookies)
        videos = response.json()['jsonGraph']['genres'][genre]['az']
        
        try:
            for v in videos:
                info = videos[v]["itemSummary"]["value"]
                print('Found video: "{}".'.format(info['title']))
                if genre == MOVIES:
                    self.movies.append(video.Video(info['title'], info['releaseYear'], info['id'], info['boxArt']['url'], info['availability']['availabilityDate'], []))
                else:
                    self.series.append(video.Video(info['title'], info['releaseYear'], info['id'], info['boxArt']['url'], info['availability']['availabilityDate'], self.getSeriesData(info['id'])))
        except:
            return
        
        if genre is MOVIES:
            return self.movies
        else:
            return self.series


    def scrapAll(self, genre):
        for index in range(0, 10000, 200):
            self.scrap(genre, index, index+1)
        
        if genre is MOVIES:
            return self.movies
        else:
            return self.series
