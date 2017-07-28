import json
import string
import random
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
    #print(len(save))
    for i in range (1,41):
        randy = 3#random.randint(1,180854)

        try:
            x = (save[str(randy)])
            print ("Birthday Paradox: %i" % randy)
            print("GOT HERE YOU FUCKBOIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
        except:
            pass
        
        
        gotostring = "https://pucatrade.com/profiles/wants/" + str(randy)
        DRIVER.get(gotostring)

        
        failed = 0
        value = 0
        reason = []
        country = 'none'
        most_recent_want_update = 0
        account_type = 0
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

            wants1 = soup.find_all(class_= "item clear animated")
            print(len(wants1))
            wants2 = soup.find_all(class_="item clear animated promoted")
            print(len(wants2))
            wants = wants1 + wants2
            
            for j in wants:
                card_count = j.find_all(class_= "column quantity")[0].text
                card_count = int(card_count[:-1])
                #print(card_count)

                card_name = str(j.find_all(class_= "name")[0].contents[0].text) #should probably break this into more lines

                card_set_and_rarity = str(j.find_all(class_= "iconExpansion")[0])
                slice_index = string.find(card_set_and_rarity, "/expansions/")
                card_set_and_rarity = card_set_and_rarity[slice_index+12:-7].split("_")
                #should I be turning this into an array of tuples to make it like the Cardsphere one

                card_condition = str(j.find_all(class_= "condition")[0].contents[0].text)

                card_foil = len(str(j.find_all(class_= "foil")[0].contents[0].text))
                if card_foil > 0:
                    card_foil = True
                else:
                    card_foil = False

                card_languages = str(j.find_all(class_="language")[0].contents[0].text).split(", ")
                card_promoted = len(j.find_all(class_="hint iconQuestion icon icon-promoted")) #might wanna turn this into a bool
                card_point_value = 
                
                
                #for k in j:
                    #print(k)
                #if j.class_ == "item clear animated promoted"
            #print(len(wants))
            date = 0
            #if len(wants) > 0:
                #date = wants[1].find_all(class_= "column date")
                #date = str(date)
                #date = date[-11:-7]
                #print(date)

            icons = soup.find_all(class_= "icon")
            country = icons[10]['class'][1]
            country = str(country)
            country = country[-2:]
            #print(country)
                
                

        
            
    ##        if value <= 600:
    ##            print("User %i: Zeroed Out Account" % randy)
    ##            failed = 1
                
            if sent[0] == "0":
                #print("User %i: Never Traded" % randy)
                failed = 1
                reason.append("never traded")
                
            if len(wants) == 0:
                #print("User %i: No Wants" % randy)
                failed = 1
                reason.append("no wants")
            if date != "2017":
                #print("User %i: Wants not updated since last year" % randy)
                failed = 1
                reason.append("wants not updated since last year")

                       
        if failed == 0:
            #print("User %i: Active User" % randy)
            pass

        save[str(randy)] = {"failed": failed, "value": value, 'reason':list(reason), 'country':country}

        

##        ActiveUserPercent = 1.0-(fails/i)
##        ActiveUserPercent *= 100

##        if i % 10 == 0:
##            print("Number of users checked: %i" % i)
##            print("Active User Percentage: %f%%" % ActiveUserPercent)
    print('finished a loop of 40')
    with open('pu_data.json', 'w') as outfile:
        json.dump(save, outfile)
