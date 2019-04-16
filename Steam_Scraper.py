from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate



class SteamScrapper:
    def __init__(self):
        self.url = 'https://steamcharts.com/top'

    def get_page(self):
        return requests.get(self.url).text

    @staticmethod
    def soup(html):
        return BeautifulSoup(html, 'html.parser')

    def main(self):
        page = self.soup(self.get_page())
        names = page.find_all('td', {'class': 'game-name left'})
        curr_pl = page.find_all(lambda tag: tag.name == 'td' and
                                   tag.get('class') == ['num'])
        p_player = page.find_all('td', {'class': 'num period-col peak-concurrent'})

        game_names = list(map(lambda name: name.findChildren('a', recursive=False)[0].text.strip(), names))
        current_players = list(map(lambda num: num.text, curr_pl))
        peak_players = list(map(lambda num: num.text, p_player))

        games_array = []

        for c, value in enumerate(game_names):
            games_array.append([c + 1, value, current_players[c], peak_players[c]])


        output_string = tabulate(games_array, headers=['Position', 'Name', 'Current Playersa', 'Peak Players'])

        return output_string


class Whatsapp:

    def __init__(self):
        self.path = "C:\\Users\\Cesar M L Westphal\\PycharmProjects\\Scrappers\\Data\\chromedriver"
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--user-data-dir=./User_Data')
        self.driver = webdriver.Chrome(self.path, options=self.options)
        self.url = 'https://web.whatsapp.com'
        self.time = 20

    def search(self):
        self.driver.get(self.url)
        time.sleep(self.time)

        elem = self.driver.find_element_by_xpath('//span[contains(text(),"GameLab 2019.1")]')
        elem.click()
        msg = SteamScrapper().main()
        time.sleep(35)
        print(msg)

        input_box = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        input_box.send_keys(msg)
        input_box.send_keys(Keys.ENTER)
        time.sleep(6)

    def main(self):
        self.search()



if __name__ == "__main__":
   print(SteamScrapper().main())