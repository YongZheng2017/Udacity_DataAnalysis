import xml.etree.cElementTree as ET
from collections import defaultdict
import re

OSMFILE = "chengdu_china.osm"
street_type_re = re.compile(r'\w$', re.U)


expected = [u'街', u'道', u"段", u"路", u'\u6bb5', u'\u8857', u'\u8def',  u'\u9053']

# UPDATE THIS VARIABLE
english_name_mapping = { "Tian Xian Qiao Bei Jie": "天仙桥北街",
            "Long du nan Road": "龙都南路",
            "JinAn": "金安路",
            "Huadu Avenue West": "华都大道西",
            "Jinquan Street": "金泉街",
            u"高新区南城都汇2A期汇雅园": "景明路"
            }

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                    
    for street_type, ways in street_types.iteritems():
        for name in ways:
            better_name = update_name(name, english_name_mapping)
            print name, "=>", better_name
            
    
    
    osm_file.close()
    return street_types


def update_name(name, mapping):

    for key,value in mapping.items():
        if key in name:
            name = name.replace(key, value)
            break
    return name

'''
def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, english_name_mapping)
            print name, "=>", better_name
'''
            

if __name__ == '__main__':
    audit(OSMFILE)