import os
import browser_cookie3
import requests
import psutil
import subprocess





def checkDir(dir_name):
    if os.path.isdir(dir_name):
        return
    else:
         os.makedirs(dir_name)


def writeMovies(movies, parent_dir = "netflix_movies"):
    checkDir(parent_dir)
    for movie in movies:
        if os.path.isdir(os.path.join(parent_dir, movie.dir_name)):
            continue
        os.makedirs("{}/{}".format(parent_dir, movie.dir_name))
        f = open("{}/{}/{}.strm".format(parent_dir, movie.dir_name, movie.dir_name), "a")
        f.write("https://www.netflix.com/watch/{}".format(movie.id))
        f.close()



def writeSeries(series, parent_dir = "netflix_series"):
        checkDir(parent_dir)

        for serie in series:
            if os.path.isdir(os.path.join(parent_dir, serie.dir_name)):
                continue
            os.makedirs("{}/{}".format(parent_dir, serie.dir_name))

            for season in serie.seasons:
                if int(season['seq'] < 10):
                    os.makedirs("{}/{}/Season 0{}".format(parent_dir, serie.dir_name, season['seq']))
                else:
                    os.makedirs("{}/{}/Season {}".format(parent_dir, serie.dir_name, season['seq']))

                episodes = season['episodes']
                for index, episode in enumerate(episodes):
                    index += 1
                    if int(season['seq'] < 10):
                        if index < 10:
                            f = open("{}/{}/Season 0{}/Episode S0{}E0{}.strm".format(parent_dir, serie.dir_name, season['seq'], season['seq'], index), "a")
                        else:
                            f = open("{}/{}/Season 0{}/Episode S0{}E{}.strm".format(parent_dir, serie.dir_name, season['seq'], season['seq'], index), "a")
                    else:
                        if index < 10:
                            f = open("{}/{}/Season {}/Episode S{}E0{}.strm".format(parent_dir, serie.dir_name, season['seq'], season['seq'], index), "a")
                        else:
                            f = open("{}/{}/Season {}/Episode S{}E{}.strm".format(parent_dir, serie.dir_name, season['seq'], season['seq'], index), "a")

                    f.write("https://www.netflix.com/watch/{}".format(episode['id']))
                    f.close()


def unlockChromium(name):
    processes = psutil.process_iter()
    for process in processes:
        if process.name() == name:
            process.kill()
            print('Stoping process: {}, pid: {}'.format(process.name(), process.pid))

    match name:
        case "chrome.exe":
            process = subprocess.Popen('"C:\Program Files\Google\Chrome\Application\chrome.exe" --disable-features=LockProfileCookieDatabase')
        case "msedge.exe":
            process = subprocess.Popen('"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --disable-features=LockProfileCookieDatabase')


def getCookies(domain):
    cookies={}
    chromeCookies = list(browser_cookie3.chrome(domain_name=domain))

    for cookie in chromeCookies:
        cookies[cookie.name]=cookie.value

    return cookies


def getCountry():
    url = 'https://geolocation.onetrust.com/cookieconsentpub/v1/geo/location'
    response = requests.request("GET", url,headers={'Accept':'application/json'})
    return response.json()['country'].lower()
