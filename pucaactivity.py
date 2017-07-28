import json
import string
import random
import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup, SoupStrainer


DRIVER = webdriver.Firefox(executable_path='/Users/MarkusLeben/Downloads/geckodriver')

DRIVER.get("http://pucatrade.com/login")

try:
    with open('pu_data.json') as json_data:
        save = json.load(json_data)
except:
    save = {}


while(1):
    if DRIVER.current_url == "https://pucatrade.com/nexus":
        break

while(1):
    print(len(save))
    for i in range (1,41):
        randy = random.randint(1,180854)

        try:
            x = (save[str(randy)])
            print ("Birthday Paradox: %i" % randy)
        except:
            pass
        
        
        gotostring = "https://pucatrade.com/profiles/wants/" + str(randy)
        DRIVER.get(gotostring)

        
        failed = 0
        value = 0
        reason = []
        country = 'none'
        most_recent_want_update = 'none'
        account_type = 'commmon'
        sent = 0
        cards = []
        
        
        if (DRIVER.current_url == "https://pucatrade.com/nexus"
            or DRIVER.current_url == "https://pucatrade.com/"):
            #print("User %i: Deleted, Banned, or Private" % randy)
            failed = 1
            reason.append("deleted")
        else:
            
            soup = BeautifulSoup(DRIVER.page_source, "lxml")
            
            titles = soup.find_all(class_="main-title")
            sent = titles[2].text

            price = soup.find_all(class_="price undefined")
            value = price[0].text
            value = str(value) #this is dangerous but I'm lazy
            value = value.translate(None, string.punctuation)
            value = int(value)

            uncommon = len(soup.find_all(class_="icon-puca-uncommon"))
            rare = len(soup.find_all(class_="icon-puca-rare"))

            if uncommon > 0:
                #print("You're finding uncommons")
                account_type = 'uncommmon'

            if rare > 0:
                #print("You're finding rares")
                account_type = 'rare'
                    

            wants1 = soup.find_all(class_= "item clear animated")
            wants2 = soup.find_all(class_="item clear animated promoted")
            wants = wants1 + wants2
            
            for j in wants:
                card_count = j.find_all(class_= "column quantity")[0].text
                card_count = int(card_count[:-1])

                card_name = str(j.find_all(class_= "name")[0].contents[0].text) #should probably break this into more lines

                card_set_and_rarity = str(j.find_all(class_= "iconExpansion")[0])
                slice_index = string.find(card_set_and_rarity, "/expansions/")
                card_set_and_rarity = card_set_and_rarity[slice_index+12:-7].split("_")
                #should I be turning this into an array of tuples to make it like the Cardsphere one
                #should I be doing that post-scraping in another program?
                #should I be doing that in 
                card_condition = str(j.find_all(class_= "condition")[0].contents[0].text)

                card_foil = len(str(j.find_all(class_= "foil")[0].contents[0].text))
                if card_foil > 0:
                    card_foil = True
                else:
                    card_foil = False

                card_languages = str(j.find_all(class_="language")[0].contents[0].text).split(", ")

                card_promoted = len(j.find_all(class_="hint iconQuestion icon icon-promoted")) #might wanna turn this into a bool

                card_point_value = j.find_all(class_="price small")[0].contents[0]
                card_point_value = card_point_value.replace("+","")
                card_point_value = card_point_value.replace(",","")
                card_point_value = card_point_value.replace(" ","") #Dude fuck these filler characters so much

                card_date_added = j.find_all(class_="column date")[0].text.split("/")
                card_date_added = datetime.date(int(card_date_added[2]),int(card_date_added[0]),int(card_date_added[1]))
                if most_recent_want_update == 'none':
                    most_recent_want_update = card_date_added
                else:
                    if card_date_added > most_recent_want_update:
                        most_recent_want_update = card_date_added
                        
                card_date_added = str(card_date_added)

                card = {'count':card_count,
                        'name':card_name,
                        'set_and_rarity':card_set_and_rarity,
                        'condition':card_condition,
                        'foil':card_foil,
                        'languages':card_languages,
                        'promoted':card_promoted,
                        'point_value':card_point_value,
                        'date_added':card_date_added}

                cards.append(card)

            
            

            icons = soup.find_all(class_= "icon")
            country = icons[10]['class'][1]
            country = str(country)
            country = country[-2:]
                           
    ##        if value <= 600:
    ##            print("User %i: Zeroed Out Account" % randy)
    ##            failed = 1
                
            if sent[0] == "0":
                #print("User %i: Never Traded" % randy)
                failed = 1
                reason.append("never traded")
                
            if len(cards) == 0:
                #print("User %i: No Wants" % randy)
                failed = 1
                reason.append("no wants")
                
            if type(most_recent_want_update) == str:
                failed = 1
            elif most_recent_want_update < datetime.date(2017,1,1):
                #print("User %i: Wants not updated since last year" % randy)
                failed = 1
                reason.append("wants not updated since last year")

        

                       
        most_recent_want_update = str(most_recent_want_update)
        
        save[randy] = {"failed": failed,
                       "value": value,
                       "reason":list(reason),
                       "country":country,
                       "sent":sent,
                       "most_recent_want_update":most_recent_want_update,
                       "account_type":account_type,
                       "cards":cards}
        

        

##        ActiveUserPercent = 1.0-(fails/i)
##        ActiveUserPercent *= 100

##        if i % 10 == 0:
##            print("Number of users checked: %i" % i)
##            print("Active User Percentage: %f%%" % ActiveUserPercent)
    print('finished a loop of 40')
    with open('pu_data.json', 'w') as outfile:
        json.dump(save, outfile)
