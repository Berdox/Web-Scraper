from bs4 import BeautifulSoup
import requests
import re

mapping = ['Head Parts',
            'Core Units',
            'Arm Parts (not including Weapon Arms)',
            'Leg Parts',
            'Generators',
            'FCS (Fire Control Systems)',
            'Boosters']

pattern = '^Name|^Type|^Price|^Weight|^Energy\sDrain|^Armor\sPoint|^Shell\sDefense|^Energy\sDefense|^Computer\sType|^Map\sType|^Noise\sCanceller|^Bio\sSensor|^Radar\sFunction|^Radar\sRange|^Radar\sType|^Flavor\sText|^Energy\sOutput|^Maximum\sCharge|^Maximum\sLock|^Boost\sPower|^RedZone\sCharge|^Lock\sType|^Charge\sDrain|^Max\sWeight|^Anti-Missile\sReponse|^Anti-Missile\sAngle|^Extension\s(Option)\sSlots|^Speed|^Stability|^Jump\sFunction'
parts = []

html_text = requests.get('https://www.reddit.com/r/armoredcore/comments/7ankkf/armored_core_1_guide_armor_and_internal_part/').text
soup = BeautifulSoup(html_text, 'lxml')
title = soup.find('h2', class_ = 'text-18 xs:text-20')
while title.text != mapping[6]:
    if title.name == 'hr':
        title = title.next_sibling
    else:
        parts.append(title.text)
        title = title.next_sibling

with open('style.txt', 'w') as file:    
    for part in parts:
        file.write(part)

        
#print(titles.next_sibling.text)
#for title in titles:
#    print(title.next_element.text)
#parts = soup.find_all('p', class_= '')
