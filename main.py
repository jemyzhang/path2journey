import json
import os
import shutil
import time
import uuid
from datetime import datetime

from bs4 import BeautifulSoup

if __name__ == '__main__':
    if not os.path.exists('journey'):
        os.mkdir('journey')
    next_page = 'index.html'
    while next_page is not None:
        print(f'Processing {next_page}...')
        with open(next_page, 'r') as f:
            soup = BeautifulSoup(f.read(), features='html.parser')
        next_page = soup.find('div', class_='pagination_next')
        if next_page is not None and next_page.a is not None:
            next_page = next_page.a['href']
        else:
            next_page = None
        for feed in soup.find_all('div', class_='box_feed'):
            journey_ = {'text': '', 'date_modified': 0, 'date_journal': 0, 'id': '', 'preview_text': '', 'address': '',
                        'music_artist': '', 'music_title': '', 'lat': 0.0, 'lon': 0.0, 'mood': 6,
                        'label': '',
                        'folder': '', 'sentiment': 0, 'timezone': '', 'favourite': False, 'type': '',
                        'weather': {'id': 803, 'degree_c': 0, 'description': 'broken clouds', 'icon': '04n',
                                    'place': 'Yongfeng'}, 'photos': [], 'tags': ['Path']}
            head = feed.find('div', class_='area_head')
            div_time = head.find('div', class_='time')
            try:
                ts = int(
                    time.mktime(datetime.strptime(div_time.get_text(), '%Y-%m-%d %H:%M:%S CST').timetuple())) * 1000
                last_ts = ts
            except ValueError:
                ts = last_ts
            journey_['date_modified'] = ts
            journey_['date_journal'] = ts
            journey_['id'] = f'{ts}-{uuid.uuid4().hex[-16:]}'
            text = feed.find('div', class_='area_text').div.string
            if text is not None:
                journey_['text'] = text
                journey_['preview_text'] = text
            media = feed.find('div', class_='area_media')
            if media is not None:
                media_file = media.video['src'] if media.img is None else media.img['src']
                _, suffix = os.path.splitext(media_file)
                new_media_file = os.path.join('journey', f'{journey_["id"]}{suffix}')
                journey_['photos'].append(f'{journey_["id"]}{suffix}')
                shutil.copy2(media_file, new_media_file)
            json_file = os.path.join('journey', f'{journey_["id"]}.json')
            with open(json_file, 'w') as f:
                f.write(json.dumps(journey_, ensure_ascii=False))
