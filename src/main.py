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

pattern = '^Name|^Type|^Price|^Weight|^Energy\sDrain|^Armor\sPoints|^Armor\sPoint|^Shell\sDefense|^Energy\sDefense|^Computer\sType|^Map\sType|^Noise\sCanceller|^Bio\sSensor|^Radar\sFunction|^Radar\sRange|^Radar\sType|^Flavor\sText|^Energy\sOutput|^Maximum\sCharge|^Maximum\sLock|^Boost\sPower|^RedZone\sCharge|^Lock\sType|^Charge\sDrain|^Max\sWeight|^Anti-Missile\sResponse|^Anti-Missile\sAngle|^Extension\s\(Option\)\sSlots|^Speed|^Stability|^Jump\sFunction'
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

def partFinder(title, classes, sectionNum):
    global parts
    while(title.name != 'hr'):
        if(re.search(pattern, title.text.strip())):
            subPart = re.findall(pattern, title.text.strip())[0]
            info = title.text.strip()
            info = info.removeprefix(subPart+':')
            if(subPart.find('(')):
                subPart = subPart.replace('(Option) ', '')
            if(subPart.find(' ')):
                subPart = subPart.replace(' ', '_')
            if(subPart.find('-')):
                subPart = subPart.replace('-', '_')
            if(subPart == 'Armor_Point'):
                subPart = subPart + 's'
            setattr(classes, subPart, info.strip())
        title = title.next_sibling
    parts[sectionNum].append(classes)
    return title

html_text = requests.get('https://www.reddit.com/r/armoredcore/comments/7ankkf/armored_core_1_guide_armor_and_internal_part/').text
soup = BeautifulSoup(html_text, 'lxml')
title = soup.find('h2', class_ = 'text-18 xs:text-20')
while title.text != mapping[7]:
    if title.name == 'h2':
        section = title.text
        sectionNum = 1 + sectionNum
        title = title.next_sibling
    else:
        if(re.search(pattern, title.text.strip())):
            if(sectionNum == 0):
                h = Head()
                title = partFinder(title, h, sectionNum)
            elif(sectionNum == 1):
                c = Core()
                title = partFinder(title, c, sectionNum)
            elif(sectionNum == 2):
                a = Arm()
                title = partFinder(title, a, sectionNum)
            elif(sectionNum == 3):
                l = Leg()
                title = partFinder(title, l, sectionNum)
            elif(sectionNum == 4):
                g = Genertators()
                title = partFinder(title, g, sectionNum)
            elif(sectionNum == 5):
                fc = FCS()
                title = partFinder(title, fc, sectionNum)
            elif(sectionNum == 6):
                b = Booster()
                title = partFinder(title, b, sectionNum)
        else:
            title = title.next_sibling
         
#for part in parts:
#    for type in part:
#       print(type.Armor_Points)

with open('style.txt', 'w') as file:    
    for part in parts:
        for component in part:
            file.write(component.Name + '\n')
            
'''while(title.name != 'hr'):
                    if(re.search(pattern, title.text.strip())):
                        subPart = re.findall(pattern, title.text.strip())[0]
                        info = title.text.strip()
                        info = info.removeprefix(subPart+':')
                        if(subPart.find(' ')):
                            subpart = subPart.replace(' ', '_')
                        if(subPart.find('-')):
                            subpart = subPart.replace('-', '_')
                        setattr(h, subPart, info)
                    title = title.next_sibling
                parts[sectionNum].append(h)'''