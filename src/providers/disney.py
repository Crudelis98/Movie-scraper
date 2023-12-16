import requests
import re
import json
import sys
from provider import PROVIDER

sys.path.insert(1, '..')
from video import Video


class Disney(PROVIDER):

    def __init__(self, bearer,  region, language) -> None:
        self.MOVIES = '9f7c38e5-41c3-47b4-b99e-b5b3d2eb95d4'
        self.SERIES = '53adf843-491b-40ae-9b46-bccbceed863b'

        self.bearer = bearer
        self.region = region
        self.language = language

        self.watchURL = 'https://www.disneyplus.com/{}-{}/video/'.format(region.lower(), language.lower())

        PROVIDER.__init__(self)

    def getHeaders(self, bearer):
        return {
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6',
                'Authorization': '{}'.format(bearer),
                'Cache-Control': 'no-cache',
                'Origin': 'https://www.disneyplus.com',
                'Pragma': 'no-cache',
                'Referer': 'https://www.disneyplus.com/',
                'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'X-Application-Version': '1.1.2',
                'X-Bamsdk-Client-Id': '',
                'X-Bamsdk-Platform': 'javascript/windows/chrome',
                'X-Bamsdk-Version': '27.1',
                'X-Dss-Edge-Accept': 'vnd.dss.edge+json; version=2'
                }


    def scrapSeriesData(self):
        for index, serie in enumerate(self.series):
            index += 1
            print('Getting data for serie nr: {}, Title: "{}"'.format(index, serie.title))

            url = 'https://disney.content.edge.bamgrid.com/svc/content/DmcSeriesBundle/version/5.1/region/{}/audience/k-false,l-true/maturity/1850/language/{}/encodedSeriesId/{}'.format(self.region, self.language, serie.SeriesId)
            try:
                seasons = requests.request("GET", url, headers=self.getHeaders('Bearer ' + self.bearer)).json()['data']['DmcSeriesBundle']['seasons']['seasons']
                for season in seasons:
                    serie.seasons.append(season['downloadableEpisodes'])
                    serie.seasons.append( [self.watchURL + episode for episode in season['downloadableEpisodes']] )
                
            except:
                print('Error with serie nr: {}.'.format(index))

    def scrap(self, genre, id):
        url = 'https://disney.content.edge.bamgrid.com/svc/content/GenericSet/version/6.1/region/{}/audience/k-false,l-true/maturity/1850/language/{}/setId/{}/pageSize/30/page/{}'.format(self.region, self.language, genre, id)
        response = requests.request("GET", url, headers=self.getHeaders('Bearer ' + self.bearer))
        
        for index, video in enumerate(response.json()['data']['GenericSet']['items']):
            if genre == self.MOVIES:
                print('Found video nr: {}, Title: "{}".'.format(index + id, video['text']['title']['full']['program']['default']['content']))
                self.movies.append(Video(video['text']['title']['full']['program']['default']['content'], video['releases'][0]['releaseYear'], video['contentId'], video['image']['tile']['1.78']['program']['default']['url'], "", [], ""))
            else:
                print('Found video nr: {}, Title: "{}".'.format(index + id, video['text']['title']['full']['series']['default']['content']))
                self.series.append(Video(video['text']['title']['full']['series']['default']['content'], video['releases'][0]['releaseYear'], video['contentId'], video['image']['tile']['1.78']['series']['default']['url'], "", [], video['encodedSeriesId']))


    def scrapAll(self, genre):
        for id in range(1, 30):
            self.scrap(genre, id)



class LOGIN(object):
    def __init__(self, email, password, proxies=False):
        self.email = email
        self.password = password
        self.web_page = 'https://www.disneyplus.com/login'
        self.devices_url = "https://global.edge.bamgrid.com/devices"
        self.login_url = 'https://global.edge.bamgrid.com/idp/login'
        self.token_url = "https://global.edge.bamgrid.com/token"
        self.grant_url = 'https://global.edge.bamgrid.com/accounts/grant'
        self.SESSION = requests.Session()
        if proxies:
            self.SESSION.proxies.update(proxies)

    def clientapikey(self):
        r = self.SESSION.get(self.web_page)
        match = re.search("window.server_path = ({.*});", r.text)
        janson = json.loads(match.group(1))
        clientapikey = janson["sdk"]["clientApiKey"]

        return clientapikey

    def assertion(self, client_apikey):

        postdata = {
            "applicationRuntime": "firefox",
            "attributes": {},
            "deviceFamily": "browser",
            "deviceProfile": "macosx"
        }

        header = {"authorization": "Bearer {}".format(client_apikey), "Origin": "https://www.disneyplus.com"}
        res = self.SESSION.post(url=self.devices_url, headers=header, json=postdata)

        assertion = res.json()["assertion"]
        
        return assertion

    def access_token(self, client_apikey, assertion_):

        header = {"authorization": "Bearer {}".format(client_apikey), "Origin": "https://www.disneyplus.com"}

        postdata = {
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "latitude": "0",
            "longitude": "0",
            "platform": "browser",
            "subject_token": assertion_,
            "subject_token_type": "urn:bamtech:params:oauth:token-type:device"
        }

        res = self.SESSION.post(url=self.token_url, headers=header, data=postdata)

        if res.status_code == 200:
            access_token = res.json()["access_token"]
            return access_token

        if 'unreliable-location' in str(res.text):
            print('Make sure you use NL proxy/vpn, or your proxy/vpn is blacklisted.')
            exit()
        else:
            try:
                print('Error: ' + str(res.json()["errors"]['error_description']))
                exit()
            except Exception:
                print('Error: ' + str(res.text))
                exit()

        return None

    def login(self, access_token):
        headers = {
            'accept': 'application/json; charset=utf-8',
            'authorization': "Bearer {}".format(access_token),
            'content-type': 'application/json; charset=UTF-8',
            'Origin': 'https://www.disneyplus.com',
            'Referer': 'https://www.disneyplus.com/login/password',
            'Sec-Fetch-Mode': 'cors',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'x-bamsdk-platform': 'windows',
            'x-bamsdk-version': '3.10',
        }

        data = {'email': self.email, 'password': self.password}
        res = self.SESSION.post(url=self.login_url, data=json.dumps(data), headers=headers)
        if res.status_code == 200:
            id_token = res.json()["id_token"]
            return id_token

        try:
            print('Error: ' + str(res.json()["errors"]))
            exit()
        except Exception:
            print('Error: ' + str(res.text))
            exit()

        return None

    def grant(self, id_token, access_token):

        headers = {
            'accept': 'application/json; charset=utf-8',
            'authorization': "Bearer {}".format(access_token),
            'content-type': 'application/json; charset=UTF-8',
            'Origin': 'https://www.disneyplus.com',
            'Referer': 'https://www.disneyplus.com/login/password',
            'Sec-Fetch-Mode': 'cors',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'x-bamsdk-platform': 'windows',
            'x-bamsdk-version': '3.10',
        }

        data = {'id_token': id_token}

        res = self.SESSION.post(url=self.grant_url, data=json.dumps(data), headers=headers)
        assertion = res.json()["assertion"]

        return assertion


    def FinalToken(self, subject_token, client_apikey):

        header = {"authorization": "Bearer {}".format(client_apikey), "Origin": "https://www.disneyplus.com"}

        postdata = {
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "latitude": "0",
            "longitude": "0",
            "platform": "browser",
            "subject_token": subject_token,
            "subject_token_type": "urn:bamtech:params:oauth:token-type:account"
        }

        res = self.SESSION.post(url=self.token_url, headers=header, data=postdata)

        if res.status_code == 200:
            access_token = res.json()["access_token"]
            expires_in = res.json()["expires_in"]
            return access_token, expires_in

        try:
            print('Error: ' + str(res.json()["errors"]))
            exit()
        except Exception:
            print('Error: ' + str(res.text))
            exit()

        return None, None

    def GetAuthToken(self):

        clientapikey_ = self.clientapikey()
        assertion_ = self.assertion(clientapikey_)
        access_token_ = self.access_token(clientapikey_, assertion_)
        id_token_ = self.login(access_token_)
        user_assertion = self.grant(id_token_, access_token_)
        TOKEN, EXPIRE = self.FinalToken(user_assertion, clientapikey_)

        return TOKEN, EXPIRE
    