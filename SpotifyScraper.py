from datetime import date, timedelta
from typing import Iterator
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import Utils
from Song import Song
from SongService import SongService

baseURL = 'https://spotifycharts.com/regional/'
countryList = ['ec', 'pa', 'mx', 'hn', 'gt', 'cr', 'do', 'es']

class SpotifyScrapper:
    def requestAndObtainTopSongs(self, country: str, date: str, driver) -> Iterator[Song]:
        driver.get(baseURL + '{}/daily/{}'.format(country, date))
        delay = 80  # Increased delay to 30 seconds
        try:
            WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'chart-table'))
            )
            generalDetails: BeautifulSoup = BeautifulSoup(driver.page_source, "html.parser")
            songsList = generalDetails.find('table', {'class': 'chart-table'}) \
                            .find_all('tr')[1:]
            return map(
                lambda songRaw: self.parseSong(songRaw, country, date),
                songsList
            )

        except TimeoutException:
            print("Loading took too much time!")
            exit()
        except NoSuchWindowException:
            print("Window has been closed. Skipping...")
            return []

    def parseSong(self, songRaw: BeautifulSoup, country: str, date: str) -> Song:
        nameAndArtist = songRaw.find('td', {'class': 'chart-table-track'})
        name = nameAndArtist.find('strong').getText() \
            .replace("\"", "")\
            .strip()
        artist = nameAndArtist.find('span').getText()\
            .replace("by", "")\
            .replace("\"", "")\
            .strip()
        position = songRaw.find('td', {'class': 'chart-table-position'}).getText()
        return Song(int(position), name, artist, date, country)


if __name__ == '__main__':
    start_date = date(2024, 1, 1)
    end_date = date(2024, 9, 9)
    dateRange = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    service = Service(r'C:\\webdrivers\\msedgedriver.exe')
    driver = webdriver.Edge(service=service)
    songService = SongService()
    for country in countryList:
        for dateObj in dateRange:
            try:
                songs = list(SpotifyScrapper().requestAndObtainTopSongs(
                    country,
                    dateObj.strftime("%Y-%m-%d"),
                    driver
                ))
                for song in songs:
                    songService.save(song)
            except NoSuchWindowException:
                print("Window has been closed. Skipping...")
                continue
    driver.quit()  # Close the browser window