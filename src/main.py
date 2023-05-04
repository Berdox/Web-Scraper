from bs4 import BeautifulSoup
import requests
import re

mapping = ['Head Parts',
            'Core Units',
            'Arm Parts (not including Weapon Arms)',
            'Leg Parts',
            'Generators',
            'FCS (Fire Control Systems)',
            'Boosters',
            'Secrets']

pattern = '^Name|^Type|^Price|^Weight|^Energy\sDrain|^Armor\sPoint|^Shell\sDefense|^Energy\sDefense|^Computer\sType|^Map\sType|^Noise\sCanceller|^Bio\sSensor|^Radar\sFunction|^Radar\sRange|^Radar\sType|^Flavor\sText|^Energy\sOutput|^Maximum\sCharge|^Maximum\sLock|^Boost\sPower|^RedZone\sCharge|^Lock\sType|^Charge\sDrain|^Max\sWeight|^Anti-Missile\sReponse|^Anti-Missile\sAngle|^Extension\s(Option)\sSlots|^Speed|^Stability|^Jump\sFunction'
parts = []
section = ''


html_text = requests.get('https://www.reddit.com/r/armoredcore/comments/7ankkf/armored_core_1_guide_armor_and_internal_part/').text
soup = BeautifulSoup(html_text, 'lxml')
title = soup.find('h2', class_ = 'text-18 xs:text-20')
while title.text != mapping[7]:
    if title.name == 'h2':
        section = title.text
        title = title.next_sibling
    else:
        if(re.search(pattern, title.text.strip())):
            print(title.text)
            print(title.name)
            parts.append(title.text.strip() + '\n')
            title = title.next_sibling
        else:
            title = title.next_sibling

with open('style.txt', 'w') as file:    
    for part in parts:
        file.write(part)