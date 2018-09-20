#!usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

english_name_mapping = { "Tian Xian Qiao Bei Jie": "天仙桥北街",
            "Long du nan Road": "龙都南路",
            "JinAn": "金安路",
            "Huadu Avenue West": "华都大道西",
            "Jinquan Street": "金泉街",
            u"高新区南城都汇2A期汇雅园": "景明路"
            }

def is_street_name(element):
    return (element.attrib['k'] == "addr:street")

def audit(element): 
    if element.tag == "node" or element.tag == "way": 
        for tag in element.iter("tag"): 
            if is_street_name(tag): 
                for key,value in english_name_mapping.items(): 
                    if key == tag.attrib['v']: 
                        tag.set('v', value)
                                                                
if __name__ == '__main__':
    audit()