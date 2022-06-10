import requests
from bs4 import BeautifulSoup
import re
from googletrans import Translator
import csv

with open("csv/gamewith_urls.csv", 'r', encoding='cp932', errors='ignore') as csv_file:
    list_reader = csv.reader(csv_file)
    next(list_reader, None)
    url_list = list(list_reader)


class Skills:

    def get_url(self, name):
        """
        Run name through character list to get exact match of string and
        return page url of the character
        :param name:
        :return url:
        """
        url = ""
        # Iterate through character name to get exact match
        count = 0
        while count < (len(url_list) + 1):
            for data in url_list:
                if name.lower() == data[0].lower():
                    url = data
                    break
            # If exact chara name not found, iterate through chara aliases to get exact match
            if not url:
                for data in url_list:
                    alias = data[3].split(",")
                    if name.lower() in alias:
                        url = data
                        break
            count = count + 1
        return url

    def get_skills(self, name):
        data = self.get_url(name)  # Get URL

        if data == "":
            return False
        else:
            page = requests.get(data[4])  # Request page

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
        skills = []
        for text in fulltext:
            skills.append(translator.translate(text, dest='en').text)

        return skills
