import requests
from bs4 import BeautifulSoup
import time 
import pandas as pd

# スクレイピング対象のページURL
base_url = "https://voice-key.news/artist-key/"
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

dls = soup.find_all('dl', {'class': 'accordionBox'})


singer_name_list, song_name_list, sound_low_list, sound_high_list, sound_super_high_list, = [],[],[],[],[]

# 1から始めるのは閲覧数の多いアーティストが0番目なので
# まずはあ行のアーティスト
for i,dl in enumerate(dls[1:]):
    print((i+1) * 10 )
    # aタグを全て取得、X行のアーティスト
    a_tags = dl.find_all('a')
    

    for a_tag in a_tags:
        s0 = a_tag.text #artist
        
        time.sleep(2)
        artist_url = a_tag.get('href')
        response = requests.get(artist_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        song_list_div = soup.find('tbody', {'class': 'row-hover'})

        song_name = song_list_div.find_all('td', {'class': 'column-1'})
        sound_low = song_list_div.find_all('td', {'class': 'column-2'})
        sound_high = song_list_div.find_all('td', {'class': 'column-3'})
        sound_super_high = song_list_div.find_all('td', {'class': 'column-4'})

        for s1,s2,s3,s4 in zip(song_name,sound_low,sound_high,sound_super_high):
            singer_name_list.append(s0)
            song_name_list.append(s1.text)
            sound_low_list.append(s2.text)
            sound_high_list.append(s3.text)
            sound_super_high_list.append(s4.text)
            

df = pd.DataFrame([singer_name_list,song_name_list, sound_low_list, sound_high_list, sound_super_high_list]).T
df.columns = ['singer','song','low','high','super_high']
df.to_csv('song_data.csv', index = False)     
print('保存完了')