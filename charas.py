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

class Chara:

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

    def get_page(self, name):
        """
        Run the get_url function to get the URL,
        request the page and extract the summary table of the character from page,
        Split the text result and translate the text result,
        return the translated text
        :param name:
        :return translated_summary_list:
        """

        data = self.get_url(name)  # Get URL

        if data == "":
            return False
        else:
            page = requests.get(data[URL])  # Request page

            soup = BeautifulSoup(page.content, "html.parser")  # parse HTML to soup
            results = soup.find(id="article-body")  # Find id "article-body" in webpage
            results_elements = results.find_all("div", class_="puri_hyouka_table")  # Find class "puri-hyouka-table" for table of summary

            # change all br to new lines
            for br in soup.find_all("br"):
                br.replace_with("\n")

            # get the text from table in "puri_hyouka_table"
            for element in results_elements:
                for tr in element:
                    fulltext = tr.getText(separator='').strip()

            # split the full text into ratings, chara type and summary
            split_text1 = re.split(r'.(?=役割)', fulltext)
            ratings = split_text1[0]
            split_text2 = re.split(r'.(?=簡易評価)', split_text1[1])
            chara_type = split_text2[0]
            summary = split_text2[1]

            # Separator to add linebreak between string
            separator = "\n"
            # Create translator object
            translator = Translator()

            # break ratings into multiple lines and translate it
            split_ratings = re.split(r'.(?=【)', ratings)  # split string based on 【
            ratings = separator.join(split_ratings)  # join back the strings with linebreaks
            ratings_tl = translator.translate(ratings, dest='en').text  # translate the string and save it to new variable

            # add ")" at the end and translate chara type
            chara_type = chara_type + ")"
            chara_type_tl = translator.translate(chara_type, dest='en').text

            # remove "簡易評価" and translate summary
            summary = summary.replace("簡易評価", "")
            summary_tl = translator.translate(summary, dest='en').text

            translated_summary_list = [data[NAME], ratings_tl, chara_type_tl, summary_tl]
            return translated_summary_list
