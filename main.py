import utils
import sys

sys.path.insert(1, 'providers')
import netflix

try:
    if input('This will restart your browser, continue? y/N ') == 'y':
        utils.unlockChromium('chrome.exe')
except:
    pass

n = netflix.Netflix()

utils.writeSeries(n.scrapAll(netflix.SERIES))
#utils.writeMovies(n.scrapAll(netflix.MOVIES))
