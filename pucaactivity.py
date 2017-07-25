import json
import string
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup, SoupStrainer


DRIVER = webdriver.Firefox(executable_path='/Users/MarkusLeben/Downloads/geckodriver')
from bs4 import BeautifulSoup, SoupStrainer




DRIVER.get("http://www.pucatrade.com/login")

try:
    with open('data.json') as json_data:
        save = json.load(json_data)
except:
    save = {}





#Lazy Login function
while(1):
    if DRIVER.current_url == "https://pucatrade.com/nexus":
        break

while(1):
    print(len(save))

    fails = 0.0
    for i in range (1,101):
        randy = random.randint(1,180854)

        try:
            x = save[randy]
            print("GOT HERE YOU FUCKBOIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
            continue
            #if x = 1:
            #    fails += 1
            #continue
        except:
            pass
        
        #randy = i
        
        gotostring = "https://pucatrade.com/profiles/wants/" + str(randy)
        #print (gotostring)
        DRIVER.get(gotostring)
        #print(DRIVER.current_url)
        failed = 0
        
        if (DRIVER.current_url == "https://pucatrade.com/nexus"
            or DRIVER.current_url == "https://pucatrade.com/"):
            #print("User %i: Deleted, Banned, or Private" % randy)
            failed = 1
        else:
            
            soup = BeautifulSoup(DRIVER.page_source, "lxml")
            titles = soup.find_all(class_="main-title")
            trades = titles[2].text
            #print(trades)

            price = soup.find_all(class_="price undefined")
            value = price[0].text
            value = str(value) #this is dangerous but I'm lazy
            value = value.translate(None, string.punctuation)
            value = int(value)

            wants = soup.find_all(class_= "animated")
            #print(len(wants))
            date = 0
            if len(wants) > 0:
                date = wants[1].find_all(class_= "column date")
                date = str(date)
                date = date[-11:-7]
                #print(date)
                

        
            
    ##        if value <= 600:
    ##            print("User %i: Zeroed Out Account" % randy)
    ##            failed = 1
                
            if trades[0] == "0":
                #print("User %i: Never Traded" % randy)
                failed = 1
                
            if len(wants) == 0:
                #print("User %i: No Wants" % randy)
                failed = 1
            if date != "2017":
                #print("User %i: Wants not updated since last year" % randy)
                failed = 1

                       
        if failed == 0:
            #print("User %i: Active User" % randy)
            pass
        else:
            fails += 1

        save[randy] = {"failed": failed, "value": value}

        

        ActiveUserPercent = 1.0-(fails/i)
        ActiveUserPercent *= 100

##        if i % 10 == 0:
##            print("Number of users checked: %i" % i)
##            print("Active User Percentage: %f%%" % ActiveUserPercent)
    print('finished a loop of 100')
    with open('data.json', 'w') as outfile:
        json.dump(save, outfile)
