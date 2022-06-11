import requests
from bs4 import BeautifulSoup
import re
from googletrans import Translator
import csv

with open("csv/gamewith_urls.csv", 'r', encoding='cp932', errors='ignore') as csv_file:
    list_reader = csv.reader(csv_file)
    next(list_reader, None)
    url_list = list(list_reader)

NAME = 0
RARITY = 1
TYPE = 2
ALIAS = 3
URL = 4


class Skills:

    def get_url(self, name):
        """
        Run name through character list to get exact match of string and
        return page url of the character
        :param name:
        :return url:
        """
        url = ""
        # Iterate through character aliases to get exact match
        for data in url_list:
            aliases = data[ALIAS].split(",")
            for alias in aliases:
                if name.lower() == alias.lower():
                    url = data
        return url

    def get_skills(self, name):
        """
        Run get_url function to get the URL of the character,
        Request the page and extract the skills table from the page,
        Save the skills into a list and translate the list,
        Return the translated skills list.
        :param name:
        :return skills:
        """
        data = self.get_url(name)  # Get URL

        if data == "":
            return False
        else:
            page = requests.get(data[URL])  # Request page

            soup = BeautifulSoup(page.content, "html.parser")  # parse HTML to soup
            results = soup.find(id="article-body")  # Find id "article-body" in webpage
            # Find class "pcr_skillt_table" for table of summary
            results_elements = results.find_all("div", class_="pcr_skillt_table")

            # change all br to new lines
            for br in soup.find_all("br"):
                br.replace_with("\n")

            # get the text from table in "pcr_skillt_table"
            fulltext = []
            for element in results_elements:
                for td in element:
                    fulltext.append(td.getText(separator='').strip())

        # Create translator object
        translator = Translator()

        # Translate fulltext skills into English
        skills = [data[NAME]]
        for text in fulltext:
            skills.append(translator.translate(text, dest='en').text)

        return skills
