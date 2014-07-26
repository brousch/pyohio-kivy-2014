import webbrowser
from kivy.logger import Logger

def open_url(url):
    Logger.info('Opening {} in web browser.'.format(url))
    webbrowser.open(url)
    
