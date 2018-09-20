import pprint
import re
import xml.etree.cElementTree as ET
from collections import defaultdict

osm_file = open("chengdu_china.osm", 'r')
street_type_re = re.compile(r'\w$', re.U)
street_types = defaultdict(set)
expected = [u'街', u'道', u"段", u"路", u'\u6bb5', u'\u8857', u'\u8def',  u'\u9053']

def audit_street_type(street_types, street_name):
    #print street_name
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit():
    for event, elem in ET.iterparse(osm_file, events = ("start",)):
        if elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    pprint.pprint(dict(street_types))

audit()