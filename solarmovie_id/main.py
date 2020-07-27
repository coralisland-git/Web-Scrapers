import shutil
import os
import requests
from lxml import etree
import re
import csv
import json
import time
import multiprocessing.pool as mpool
import pdb
import logging

class Solarmovie:
    base_url = 'https://ww1.solarmovie.id'
    # count of multi thread
    thread_count = 3
    # force download: True - overdownload, False - skip
    force = False
    StopIfDupeTimes = False
    # directores for videos downloaded
    video_paths = [
        '/home/vod/movies10',
        '/home/vod/tvseries10'
        #  '/mnt/c/tumblr/movies10',
        # '/mnt/c/tumblr/tvseries10'
    ]
    init_urls = {
        # add clip list board urls here.
        'listview': [            
            'https://ww1.solarmovie.id/latest-movies',
            'https://ww1.solarmovie.id/latest-series'
        ],
        # add specific series urls here.
        'series': [
            # 'https://ww1.solarmovie.id/tv-series/hannibal-season-1/7pU4VKCW/2uqlE57W',
        ],
        # add specific movies urls here.
        'movies': [            
            # 'https://ww1.solarmovie.id/movie/tangled/M6SIN8PU/zaa4kjoa'
        ]
    }
    session = requests.Session()
    page_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
        }
    clip_headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    login_headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': '__cfduid=df75f14239752bce8b1363fc7192a7a021595542819; _ga=GA1.2.2080049802.1595542826; _gid=GA1.2.434736283.1595542826; _on_page=e9fc62b40b932ba8ae7e6835b6189f6506049f8e8410e15349688e402b8bf7f4a%3A2%3A%7Bi%3A0%3Bs%3A8%3A%22_on_page%22%3Bi%3A1%3Bs%3A8%3A%22onpage_1%22%3B%7D; _csrf-frontend=00a4307e384fcbe6f89bde2a8102743ff04cb2ae33c8f0afb2057dbacaad4465a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22LF4QL_O3ujMyL7S4eH-IUaefeo_HaMf6%22%3B%7D; advanced-frontend=khmdg3o77di6j3q2arhr06fef7; _gat_gtag_UA_121404696_2=1; __atuvc=45%7C30; __atuvs=5f1b051a9cdff682003; _PN_SBSCRBR_FALLBACK_DENIED=1595606426881',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    def __init__(self):
        self.create_directory()
        self.setup_logger('history', 'history.log')
        self.setup_logger('review', 'review.log')
        if self.login():        
            self.logger('Start scraping movies and series', 'info', 'history')
            for level, urls in self.init_urls.items():
                if level == 'listview':
                    [self.parse_page(url) for url in urls]
                if level == 'movies':
                    [self.parse_movies(url) for url in urls]
                if level == 'series':
                    [self.parse_series(url) for url in urls]
    
    def validate(self, item):
        if item == None:
            item = ''
        if type(item) == int or type(item) == float:
            item = str(item)
        if type(item) == list:
            item = ' '.join(item)
        return item.strip()

    def eliminate_space(self, items):
        rets = []
        for item in items:
            item = self.validate(item)
            if item != '':
                rets.append(item)
        return rets

    def format(self, item):
        item = re.sub(r'(?<=\[).+?(?=\])', r'', item).replace('[]', '').strip()
        item = re.sub(r'[^a-zA-Z0-9+s]', r'.', item)
        while True:
            item = item.replace('..', '.')
            if '..' not in item:
                break
        if item[-1] == '.':
            item = item[:-1]
        return item

    def create_directory(self):
        for video_path in self.video_paths:
            if not os.path.isdir(video_path):
                os.makedirs(video_path)

    def setup_logger(self, logger_name, log_file, level=logging.INFO):
        log_setup = logging.getLogger(logger_name)
        formatter = logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        fileHandler = logging.FileHandler(log_file, mode='a')
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        log_setup.setLevel(level)
        log_setup.addHandler(fileHandler)
        log_setup.addHandler(streamHandler)

    def logger(self, msg, level, logfile):
        if logfile == 'history'   : log = logging.getLogger('history')
        if logfile == 'review'   : log = logging.getLogger('review') 
        if level == 'info'    : log.info(msg) 
        if level == 'warning' : log.warning(msg)
        if level == 'error'   : log.error(msg)

    def login(self):
        self.logger('Initialzing...', 'info', 'history')
        try:
            url = 'https://ww1.solarmovie.id/user/login'
            captcha_api_key = ''
            data_site_key = ''
            username = ''
            password = ''
            captcha_id = requests.post(f'http://2captcha.com/in.php?key={captcha_api_key}&method=userrecaptcha&googlekey={data_site_key}&pageurl={url}').text.split('|')[1]
            self.logger('Trying to pass the reCaptcha...', 'info', 'history')
            while True:
                recaptcha_response = requests.get(f'http://2captcha.com/res.php?key={captcha_api_key}&action=get&id={captcha_id}').text               
                time.sleep(5)
                if 'CAPCHA_NOT_READY' not in recaptcha_response:
                    break
            recaptcha_response = str(recaptcha_response.split('|')[1])
            data = {
                'SignupForm[email]': username,
                'SignupForm[password]': password,
                'SignupForm[rememberMe]': 0,
                'SignupForm[rememberMe]': 1,
                'g-recaptcha-response': recaptcha_response,
                'notification': 'false',
                'SignupForm[reCaptcha]': recaptcha_response,
                '_csrf-frontend': 'bjNackhPMjgidW4jBBB9CxtZFwsEeGEMC3t3Ox0uV14LXAU6KQJUDg=='
            }
            response = self.session.post(url, data=data, headers=self.login_headers).text
            auth_status = json.loads(response)
            if auth_status['response'] == True:                
                self.logger('Logged in successfully', 'info', 'history')
            else:                
                self.logger('Login is failed. try again, please', 'warning', 'history')
            return auth_status['response']
        except Exception as e:
            self.logger(f'Error occurs in login : {e}', 'warning', 'review')
            return False

    def parse_page(self, url):
        try:
            response = self.session.get(url, headers=self.page_headers).text
            tree = etree.HTML(response)
            clips = tree.xpath('.//div[contains(@class, "watch-option-content")]')
            pool = mpool.ThreadPool(self.thread_count)
            for clip in clips:
                clip_url = self.base_url + self.validate(clip.xpath('.//a/@href'))
                if 'movie/' in clip_url:
                    # self.parse_movies(clip_url)
                    pool.apply_async(self.parse_movies, args=(clip_url, ))
                if 'series/' in clip_url:
                    # self.parse_series(clip_url)
                    pool.apply_async(self.parse_series, args=(clip_url, ))
            pool.close()
            pool.join()
            next_page = self.validate(tree.xpath('.//ul[@class="pagination"]//li[@class="next"]//a/@href'))
            if next_page != '':
                page_url = self.base_url + next_page
                self.parse_page(page_url)
        except Exception as e:
            self.logger(f'Error occurs in parse_page : {url} : {e}', 'warning', 'review')
    
    def parse_movies(self, url):
        try:
            response = self.session.get(url, headers=self.page_headers).text
            tree = etree.HTML(response)
            clip_url = self.base_url + self.validate(tree.xpath('.//div[@id="play-content-preview"]//a/@href'))
            self.parse_clip(clip_url)
        except Exception as e:
            self.logger(f'Error occurs in parse_movies : {e}', 'warning', 'review')
    
    def parse_clip(self, url, unit=None):
        try:
            response = self.session.get(url, headers=self.page_headers).text
            subtitles = json.loads(self.validate(response.split('window.subtitles =')[1].split('</script>')[0]))
            tree = etree.HTML(response)
            key = self.eliminate_space(url.split('/'))[-1].split('-')[0]
            title = self.validate(tree.xpath('.//div[@class="movie_title movie_title_name"]//h1/text()'))
            if 'movie/' in url:
                descs = tree.xpath('.//div[@id="usefull_info"]//div[@class="desc"]')
                for desc in descs:
                    if 'release:' == self.validate(desc.xpath('.//div[@class="t"]//text()')).lower():
                        year = self.validate(desc.xpath('.//div[@class="v"]//text()'))
                        title = f'{title}.{year}'
                        break
            self.parse_option(key, title, subtitles, unit)
        except Exception as e:            
            self.logger(f'Error occurs in parse_clip : {url} : {e}', 'warning', 'review')

    def parse_series(self, url):
        try:
            response = self.session.get(url, headers=self.page_headers).text
            tree = etree.HTML(response)
            episodes = tree.xpath('.//div[@id="episodes-select-pane"]//a')
            for episode in episodes:
                subtitle = self.validate(episode.xpath('.//text()'))
                units = re.findall(r'(Episode+\s+[0-9]*)', subtitle)
                if len(units) > 0:
                    unit = units[0].split(' ')[-1]
                else:
                    unit = ''
                episode_url = f'{self.base_url}{self.validate(episode.xpath("./@href"))}'
                self.parse_clip(episode_url, unit)
        except Exception as e:
            self.logger(f'Error occurs in parse_series : {url} : {e}', 'warning', 'review')

    def parse_option(self, key, title, subtitles, unit=None):
        try:
            url = f'{self.base_url}/download/{key}/{ "true" if unit == None else "false"}'
            response = self.session.get(url, headers=self.clip_headers).text
            options = json.loads(response)
            if len(options) == 0:
                return
            max_option = options[0]
            for option in options:
                if option['label'] > max_option['label']:
                    max_option = option
            self.download_clip(max_option, title, subtitles, unit)
        except Exception as e:
            self.logger(f'Error occurs in parse_option : {title} : {e}', 'warning', 'review')

    def download_clip(self, option, title, subtitles, unit=None):
        if option['src'] == '':
            return
        try:
            file_name = f'{self.video_paths[0]}/{self.format(title)}'
            if unit != None:
                season = re.findall(r'([a-z0-9]+\s+Season)', title)
                if len(season) == 0:
                    season = re.findall(r'(-+\s+Season+\s+[0-9])', title)
                if len(season) > 0:
                    title_ = self.format(self.validate(title.replace(season[0], '')))
                    season_number = re.findall('[0-9]', season[0])[0]
                    if len(season_number) < 2:
                        season_number = '0' + season_number  
                    file_name = f'{self.video_paths[1]}/{title_}.S{season_number}E{unit}'
                else:
                    file_name = f'{self.video_paths[1]}/{self.format(title)}.E{unit}'
            file_name_with_type = f'{file_name}.{option["type"]}'
            if os.path.exists(file_name_with_type) and not self.force:
                self.logger(f'{file_name_with_type} already exists', 'info', 'history')
            else:
                self.logger(f'{file_name_with_type} is downloading', 'info', 'history')
                with requests.get(option['src'], stream=True) as file_content:
                    with open(file_name_with_type, 'wb') as output:
                        shutil.copyfileobj(file_content.raw, output)
            for subtitle in subtitles:
                sub_file_name_with_type = f'{file_name}.{subtitle["srclang"]}.srt'
                if os.path.exists(sub_file_name_with_type) and not self.force:
                    self.logger(f'{sub_file_name_with_type} already exists', 'info', 'history')
                else:
                    self.logger(f'{sub_file_name_with_type} is downloading', 'info', 'history')
                    with requests.get(subtitle['src'], stream=True) as file_content:
                        with open(sub_file_name_with_type, 'wb') as output:
                            shutil.copyfileobj(file_content.raw, output)
        except Exception as e:
            self.logger(f'Error occurs in download_clip : {title} : {e}', 'warning', 'review')


if __name__ == '__main__':
    Solarmovie()
