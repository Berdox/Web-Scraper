from bs4 import BeautifulSoup
import requests
import re
from classes import *

mapping = ['Head Parts',
            'Core Units',
            'Arm Parts (not including Weapon Arms)',
            'Leg Parts',
            'Generators',
            'FCS (Fire Control Systems)',
            'Boosters',
            'Secrets']

pattern = '^Name|^Type|^Price|^Weight|^Energy\sDrain|^Armor\sPoints|^Armor\sPoint|^Shell\sDefense|^Energy\sDefense|^Computer\sType|^Map\sType|^Noise\sCanceller|^Bio\sSensor|^Radar\sFunction|^Radar\sRange|^Radar\sType|^Flavor\sText|^Energy\sOutput|^Maximum\sCharge|^Maximum\sLock|^Boost\sPower|^RedZone\sCharge|^Lock\sType|^Charge\sDrain|^Max\sWeight|^Anti-Missile\sReponse|^Anti-Missile\sAngle|^Extension\s(Option)\sSlots|^Speed|^Stability|^Jump\sFunction'
heads = []
core = []
arm = []
leg = []
generator = []
fcs = []
boosters = []
parts = [heads, core, arm, leg, generator, fcs, boosters]
section = ''
sectionNum = -1


html_text = requests.get('https://www.reddit.com/r/armoredcore/comments/7ankkf/armored_core_1_guide_armor_and_internal_part/').text
soup = BeautifulSoup(html_text, 'lxml')
title = soup.find('h2', class_ = 'text-18 xs:text-20')
while title.text != mapping[1]:
    if title.name == 'h2':
        section = title.text
        sectionNum = 1 + sectionNum
        title = title.next_sibling
    else:
        if(re.search(pattern, title.text.strip())):
            if(sectionNum == 0):
                h = Head()
                while(title.name != 'hr'):
                    #print(title.text.strip())
                    if(re.search(pattern, title.text.strip())):
                        subPart = re.search(pattern, title.text.strip())
                        info = title.text.strip()
                        print(subPart.span)
                        prefix = subPart.string + ':'
                        info.removeprefix(prefix)
                        if(subPart.string.find(' ')):
                            subpart = subPart.string.replace(' ', '_')
                        if(subpart.find('-')):
                            subpart = subpart.replace('-', '_')
                        b = subpart
                        h.b = info
                        #print(b)
                    title = title.next_sibling
                parts[sectionNum].append(h)
        else:
            title = title.next_sibling

with open('style.txt', 'w') as file:    
    for part in parts:
        for component in part:
            file.write(component.Name)