from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests


# ul.trackList__list>li>*>*>a.sc-link-primary

def get_song_list(play_list_url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(play_list_url)
    
    print("Waiting for page to load...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.trackList__list>li>*>*>a.sc-link-primary'))
    )
    time.sleep(3)
    print('Page Loaded...')
    song_list = driver.find_elements(By.CSS_SELECTOR, 'ul.trackList__list>li>*>*>a.sc-link-primary')
    # TODO: get the matching song name for href
    # {'song_name': }
    combined_list = [{'song_name': elem.text, 'song_link': elem.get_attribute('href')} for elem in song_list]
    # print(links)
    print(f"Found {len(combined_list)} songs in the playlist...")
    driver.quit()
    return combined_list


def download_songs(links):
    api_base = 'https://co.wuk.sh'
    
    headers = { 'Accept': 'application/json', 'Content-Type': 'application/json'}
    
    valid_links = []
    failed_links = []
    print("Starting API Calls...")
    for link in links:
        response = requests.post(f'{api_base}/api/json', headers=headers, json={'url': link['song_link']})
        # print(response.json())
        if response.json()['status'] == 'stream':
            # valid_links.append({'url': response.json()['url'], 'song_name': link['song_name']})
            valid_links.append({'song_link': response.json()['url'], 'song_name': link['song_name']})
        else:
            failed_links.append(link['song_name'])
        time.sleep(1)
        
    print(f"Found {len(valid_links)} valid links...")
    print(f"Failed to find {len(failed_links)} links...")
    print("Downloading Songs...")
    for link in valid_links:
        response = requests.get(link['song_link'])
        # with..... ./out/link['song_name'].mp3
        with open(f"./out/{link['song_name'].replace('/', '-')}.mp3", 'wb') as f:
            f.write(response.content)
    print("Download Complete...")

if __name__ == '__main__':
    links = get_song_list('https://soundcloud.com/glamorized/sets/jane_remover_remixes-zip')
    download_songs(links)


