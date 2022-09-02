import csv
import random
from charas import Chara

with open("csv/gamewith_urls.csv", 'r', encoding='cp932', errors='ignore') as csv_file:
    list_reader = csv.reader(csv_file)
    next(list_reader, None)
    chara_list = list(list_reader)

NAME = 0
RARITY = 1
TYPE = 2
ALIAS = 3
URL = 4

perm_list = []
summer_list = []
halloween_list = []
xmas_list = []
fes_list = []
limited_list = []
newyear_list = []
threestar_list = []
twostar_list = []
onestar_list = []

# Load charas into seperate list
for chara in chara_list:
    if chara[RARITY] == "3" and chara[TYPE] == "perm":
        perm_list.append(chara[NAME])
    elif chara[RARITY] == "3" and chara[TYPE] == "summer":
        summer_list.append(chara[NAME])
    elif chara[RARITY] == "3" and chara[TYPE] == "halloween":
        halloween_list.append(chara[NAME])
    elif chara[RARITY] == "3" and chara[TYPE] == "xmas":
        xmas_list.append(chara[NAME])
    elif chara[RARITY] == "3" and chara[TYPE] == "fes":
        fes_list.append(chara[NAME])
    elif chara[RARITY] == "3" and chara[TYPE] == "limited":
        limited_list.append(chara[NAME])
    elif chara[RARITY] == "3" and chara[TYPE] == "newyear":
        newyear_list.append(chara[NAME])
    elif chara[RARITY] == "2":
        twostar_list.append(chara[NAME])
    elif chara[RARITY] == "1" and chara[TYPE] == "perm":
        onestar_list.append(chara[NAME])

# Rates
CHARA_RATE_UP = 0.007
LIMITED_RATE_UP = 0.016
SSR_RATE = 0.03
SR_RATE = 0.18
R_RATE = 0.79


class Gacha:

    def __init__(self):
        self.perm_list = perm_list
        self.summer_list = summer_list
        self.halloween_list = halloween_list
        self.xmas_list = xmas_list
        self.fes_list = fes_list
        self.limited_list = limited_list
        self.newyear_list = newyear_list
        self.twostar_list = twostar_list
        self.onestar_list = onestar_list
        self.ssr_rate = SSR_RATE
        self.limited_pool = []
        self.special_list = summer_list + halloween_list + xmas_list + fes_list + limited_list + newyear_list

    def set_pool(self, pools):
        """
        Set the gacha pool according to banners pools inputted
        And set the SSR rate according to banner pools inputted
        :param pools:
        """
        for pool in pools:
            # iterate through each banner to add to the total pool
            if pool.lower() == "summer" or \
                    pool.lower() == "sum":
                self.limited_pool = self.limited_pool + summer_list
            elif pool.lower() == "xmas" or \
                    pool.lower() == "christmas" or \
                    pool.lower() == "holiday":
                self.limited_pool = self.limited_pool + xmas_list
            elif pool.lower() == "halloween" or \
                    pool.lower() == "hal":
                self.limited_pool += halloween_list
            elif pool.lower() == "fes" or \
                    pool.lower() == "prifes" or \
                    pool.lower() == "prifest":
                self.limited_pool = self.limited_pool + fes_list
                self.ssr_rate = SSR_RATE * 2
            elif pool.lower() == "newyear" or \
                    pool.lower() == "ny" or \
                    pool.lower() == "new year":
                self.limited_pool = self.limited_pool + newyear_list
            elif pool.lower() == "limited" or \
                    pool.lower() == "lim":
                self.limited_pool = self.limited_pool + limited_list
            elif pool.lower() == "all":
                self.limited_pool = self.limited_pool + summer_list + fes_list + \
                                    xmas_list + halloween_list + newyear_list + limited_list
                self.ssr_rate = SSR_RATE * 2
            elif pool.lower() == "100" or \
                    pool.lower() == "100%":
                self.ssr_rate = 1
            else:
                self.perm_list = self.perm_list

    def get_single(self):
        """
        Do a single roll
        If there is limited banner, rate up for limited banner will be applied
        """
        random_num = random.random()
        if self.limited_pool:
            if random_num < LIMITED_RATE_UP:
                return random.choice(list(self.limited_pool))
            elif random_num < (self.ssr_rate - LIMITED_RATE_UP):
                return random.choice(list(self.perm_list))
            elif random_num < SR_RATE:
                return random.choice(list(self.twostar_list))
            else:
                return random.choice(list(self.onestar_list))
        else:
            if random_num < self.ssr_rate:
                return random.choice(self.perm_list)
            elif random_num < SR_RATE:
                return random.choice(self.twostar_list)
            else:
                return random.choice(self.onestar_list)

    def get_last_draw(self):
        """
        Last draw of a 10 roll with SR and up
        """
        random_num = random.random()
        if self.limited_pool:
            if random_num < LIMITED_RATE_UP:
                return random.choice(list(self.limited_pool))
            elif random_num < (self.ssr_rate - LIMITED_RATE_UP):
                return random.choice(list(self.perm_list))
            else:
                return random.choice(list(self.twostar_list))
        else:
            if random_num < self.ssr_rate:
                return random.choice(list(self.perm_list))
            else:
                return random.choice(list(self.twostar_list))

    def get_ten(self):
        """
        Do single draw 9x + 1x last draw and add them to draw_result
        Then return draw_result
        """
        self.draw_result = []
        count = 1
        for i in range(10):
            if count == 10:
                self.draw_result.append(self.get_last_draw())
            else:
                self.draw_result.append(self.get_single())
                count += 1
        return self.draw_result

    def get_single_target(self, target):
        """
        Do a single roll
        If there is limited banner, rate up for limited banner will be applied
        """
        random_num = random.random()
        if self.limited_pool:
            if random_num < CHARA_RATE_UP:
                return target
            elif random_num < LIMITED_RATE_UP:
                return random.choice(list(self.limited_pool))
            elif random_num < (self.ssr_rate - LIMITED_RATE_UP):
                return random.choice(list(self.perm_list))
            elif random_num < SR_RATE:
                return random.choice(list(self.twostar_list))
            else:
                return random.choice(list(self.onestar_list))
        else:
            if random_num < self.ssr_rate:
                return random.choice(self.perm_list)
            elif random_num < SR_RATE:
                return random.choice(self.twostar_list)
            else:
                return random.choice(self.onestar_list)

    def get_last_draw_target(self, target):
        """
        Last draw of a 10 roll with SR and up
        """
        random_num = random.random()
        if self.limited_pool:
            if random_num < CHARA_RATE_UP:
                return target
            elif random_num < LIMITED_RATE_UP:
                return random.choice(list(self.limited_pool))
            elif random_num < (self.ssr_rate - LIMITED_RATE_UP):
                return random.choice(list(self.perm_list))
            else:
                return random.choice(list(self.twostar_list))
        else:
            if random_num < self.ssr_rate:
                return random.choice(list(self.perm_list))
            else:
                return random.choice(list(self.twostar_list))

    def get_ten_target(self, target):
        """
        Do single draw 9x + 1x last draw and add them to draw_result
        Then return draw_result
        """
        self.draw_result = []
        count = 1
        for i in range(10):
            if count == 10:
                self.draw_result.append(self.get_last_draw_target(target))
            else:
                self.draw_result.append(self.get_single_target(target))
                count += 1
        return self.draw_result

    def get_spark(self):
        """
        Do get_ten 20x and return ssr list
        """
        self.draw_results = []
        self.draw_result = []
        for i in range(20):
            self.draw_results.append(self.get_ten())  # Result is a list of list
        # Convert list of list into a single list
        self.draw_result = [item for sublist in self.draw_results for item in sublist]
        '''
        for sublist in self.draw_results:
            for item in sublist:
                self.draw_result.append(item)
        '''
        # Filter item in list by SSR only
        ssr_result = [ssr for ssr in self.draw_result if ssr in self.perm_list or ssr in self.limited_pool]
        return ssr_result

    def roll_until(self, target):
        """
        Roll until you get the specified character
        """
        self.target = target
        self.draw_results = []
        self.draw_result = []
        self.get_ten_result = []
        count = 0

        chara = Chara()
        character_to_remove = "!. "  # set unwanted characters in text
        joined_name = "".join(target)  # join the input into one string
        name = joined_name.lower().strip()  # convert input into lowercase and remove any spaces
        for character in character_to_remove:
            name = name.replace(character, "")  # remove any unwanted characters in text
        data = chara.get_url(name)  # run get_skills from skills.py to get character skills

        if data == "":
            return False
        else:
            banner = (data[TYPE],)
            self.set_pool(banner)
            while data[NAME] not in self.get_ten_result:
                self.get_ten_result = self.get_ten_target(data[NAME])
                self.draw_results.append(self.get_ten_result)
                if count == 200:
                    break
                count = count + 10
            self.draw_result = [item for sublist in self.draw_results for item in sublist]
            ssr_result = [ssr for ssr in self.draw_result if ssr in self.perm_list or ssr in self.limited_pool]
            return count, data[NAME], ssr_result

    def roll_until_nl(self, target):
        """
        Roll until you get the specified character with no limit
        """
        self.target = target
        self.draw_results = []
        self.draw_result = []
        self.get_ten_result = []
        count = 0

        chara = Chara()
        character_to_remove = "!. "  # set unwanted characters in text
        joined_name = "".join(target)  # join the input into one string
        name = joined_name.lower().strip()  # convert input into lowercase and remove any spaces
        for character in character_to_remove:
            name = name.replace(character, "")  # remove any unwanted characters in text
        data = chara.get_url(name)  # run get_skills from skills.py to get character skills

        if data == "":
            return False
        else:
            banner = (data[TYPE],)
            self.set_pool(banner)
            while data[NAME] not in self.get_ten_result:
                self.get_ten_result = self.get_ten_target(data[NAME])
                self.draw_results.append(self.get_ten_result)
                count = count + 10
            self.draw_result = [item for sublist in self.draw_results for item in sublist]
            ssr_result = [ssr for ssr in self.draw_result if ssr in self.perm_list or ssr in self.limited_pool]
            return count, data[NAME], ssr_result
