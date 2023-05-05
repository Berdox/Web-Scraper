from bs4 import BeautifulSoup
import requests
import re
from WeaponClasses import *
import pandas as pd

mapping = ['Advanced Movement Tactics',
           'Weapons (Right Arm Weapons)',
           'Left Arm Weapons',
           'Back Weapons',
           'Radars',
           'Weapon Arms']

pattern = '^Name|^Type|^Price|^Weight|^Energy\sDrain|^Armor\sPoint|^Shell\sDefense|^Energy\sDefense|^Radar\sFunction|^Radar\sRange|^Radar\sType|^Flavor\sText|^Maximum\sLock|^Charge\sDrain|^Weapon\sLock|^Attack\sPower|^Number\sof\sAmmo|^Ammo\sType|^Ammo\sPrice|^Range|^Reload\sTime'

weapons = [[], [], [], [], []]
sectionNum = -1

def partFinder(title, classes, sectionNum):
    global weapons
    while(title.name != 'hr'):
        if(re.search(pattern, title.text.strip())):
            subPart = re.findall(pattern, title.text.strip())[0]
            info = title.text.strip()
            info = info.removeprefix(subPart+':')
            if(subPart.find(' ')):
                subPart = subPart.replace(' ', '_')
            if(subPart.find('-')):
                subPart = subPart.replace('-', '_')
            setattr(classes, subPart, info.strip())
        title = title.next_sibling
    weapons[sectionNum].append(classes)
    return title


html_text = requests.get('https://www.reddit.com/r/armoredcore/comments/7aheff/armored_core_1_guide_advanced_movement_and_weapon/').text
soup = BeautifulSoup(html_text, 'lxml')
title = soup.find('h2', class_ = 'text-18 xs:text-20', string='Weapons (Right Arm Weapons)')
while title.text.strip() != 'All in all, what do you guys think? Since I\'m nearing reddit\'s 40k character limit, I\'ll do Armor stats and Hidden Parts tomorrow.':
    if title.name == 'h2':
        sectionNum = 1 + sectionNum
        title = title.next_sibling
    else:
        if(re.search(pattern, title.text.strip())):
            if(sectionNum == 0):
                r = RightArm()
                title = partFinder(title, r, sectionNum)
            elif(sectionNum == 1):
                l = LeftArm()
                title = partFinder(title, l, sectionNum)
            elif(sectionNum == 2):
                b = Back()
                title = partFinder(title, b, sectionNum)
            elif(sectionNum == 3):
                r = Radar()
                title = partFinder(title, r, sectionNum)
            elif(sectionNum == 4):
                w = WeaponArms()
                title = partFinder(title, w, sectionNum)
        else:
            title = title.next_sibling
            
#for weapon in weapons:
#    for weaponNum in weapon:
#        print(vars(weaponNum))

index = 1;
for weapon in weapons:
    count = 0;
    dic = dict()
    for weaponNum in weapon:
        for key, value in vars(weaponNum).items():
            if(key.find('_')):
                replacekey = key.replace('_', ' ')
                if replacekey in dic.keys():
                    dic[replacekey].append(value)
                else:
                    dic[replacekey] = [value]
            else:
                if key in dic.keys():
                    dic[key].append(value)
                else:
                    dic[key] = [value]

    for key in dic:
       print(len(dic[key]))
    print(dic)
    df = pd.DataFrame(dic)
    with pd.ExcelWriter("part" + str(index) + ".xlsx", engine = "openpyxl", mode = "w") as writer:
        df.to_excel(writer, sheet_name = "{}".format(index), index = False, engine = "openpyxl")
    index = 1 + index