import json
import string
import random
import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup, SoupStrainer


DRIVER = webdriver.Firefox(executable_path='/Users/MarkusLeben/Downloads/geckodriver')

DRIVER.get("http://cardsphere.com/login")

try:
    with open('cs_data.json') as json_data:
        save = json.load(json_data)
except:
    save = {}

while(1):
    if DRIVER.current_url == "https://www.cardsphere.com/":
        break


for i in range(1, 2841):
    gotostring = "https://www.cardsphere.com/user/" + str(i)
    DRIVER.get(gotostring)
    

    failed = 0
    value = 0
    reason = []
    country = 'none'
    join_date = 0
    sent = 0
    recieved = 0
    cards = []
    

    soup = BeautifulSoup(DRIVER.page_source, "lxml")
    failpage = soup.find_all(class_="text-center")

    if len(failpage) == 1:
        failed = 1
        reason.append("deleted")
        print("Deleted account?")
    else:
        userdata = soup.find(class_="well")
        userdata = userdata.find_all('p')
        country = userdata[1].text[9:].strip()
        join_date = userdata[2].text[9:].strip().split()

        date_converter = {'Jan':1,
                          'Feb':2,
                          'Mar':3,
                          'Apr':4, #may be wrong abbreviation
                          'May':5,
                          'Jun':6,
                          'Jul':7,
                          'Aug':8,
                          'Sep':9,
                          'Oct':10,
                          'Nov':11,
                          'Dec':12}

        join_date[0] = date_converter[join_date[0]]
        join_date[1] = int(join_date[1])

        join_date = datetime.date(2017,join_date[0],join_date[1])
        join_date = str(join_date)
        
        

        sent = int(userdata[3].text[12:].strip())
        recieved = int(userdata[4].text[17:].strip())
        value = float(userdata[5].text[11:].strip())

    if (join_date == '2017-07-23' or
        join_date == '2017-07-24' or
        join_date == '2017-07-25' or
        join_date == '2017-07-26' or
        join_date == '2017-07-27'):
        continue

    
    if sent == 0 and recieved == 0:
        failed = 1
        reason.append("never traded")
        
    has_no_wants = soup.find_all(class_="alert alert-info")
    if has_no_wants:
        failed = 1
        reason.append("no wants")
    else:
        wants = soup.find_all(class_="cs-row")[1:-1] #there's a header and footer to remove
        for j in wants:
            card_count = str(j.contents[1].contents[0].strip())
            card_name = j.contents[1].contents[1].text
            card_set_and_rarity = []
            for k in j.contents[3]:
                raw = str(k)
                if len(raw) < 2:
                    continue
                
                rarity = 0
                common = string.find(raw, "ss-common")
                uncommon = string.find(raw, "ss-uncommon")
                rare = string.find(raw, "ss-rare")
                mythic = string.find(raw, "ss-mythic")
                other = string.find(raw, "ss-c")
                if common > -1:
                    rarity = 'common'
                elif uncommon > -1:
                    rarity = 'uncommon'
                elif rare > -1:
                    rarity = 'rare'
                elif mythic > -1:
                    rarity = 'mythic'
                elif other > -1:
                    rarity = 'other'

                slice_index = string.find(raw, "title=")
                set_ = raw[slice_index+7:-6]

                card_set_and_rarity.append((set_,rarity))
            card_condition = j.contents[5].text.strip().split()
            card_foil = j.contents[7].text.strip().split()
            card_languages = j.contents[9].text.strip().split()

            raw_money = j.contents[11].text.strip().split()
            min_offer = float(raw_money[0][1:])
            min_offer_markdown = float(raw_money[1][:-1])/100
            min_value = float(raw_money[3][1:])
            
            raw_money = j.contents[13].text.strip().split()
            max_offer = float(raw_money[0][1:])
            max_offer_markdown = float(raw_money[1][:-1])/100
            max_value = float(raw_money[3][1:])
            
            card = {'count':card_count,
                    'name':card_name,
                    'set_and_rarity':card_set_and_rarity,
                    'condition':card_condition,
                    'foil':card_foil,
                    'languages':card_languages,
                    'min_offer':min_offer,
                    'min_offer_markdown':min_offer_markdown,
                    'min_value':min_value,
                    'max_offer':max_offer,
                    'max_offer_markdown':max_offer_markdown,
                    'max_value':max_value}

            cards.append(card)


    save[i] = {"failed":failed,
               "value":value,
               "reason": list(reason),
               "country":country,
               "join_date":join_date,
               "sent":sent,
               "recieved":recieved,
               "cards":cards}



    if i % 100 == 0:
        with open('cs_data.json', 'w') as outfile:
            json.dump(save, outfile)
            print('saving')

    

with open('cs_data.json', 'w') as outfile:
    json.dump(save, outfile)                    
                    
print('done')

    
