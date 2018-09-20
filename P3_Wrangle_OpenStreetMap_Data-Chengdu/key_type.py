import re
import pprint
import xml.etree.cElementTree as ET

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'\"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        # YOUR CODE HERE
        #print element.get('k')
        global lower
        global lower_colon
        global problemchars
        if lower.match(element.get('k')):
            keys['lower']+=1
        elif lower_colon.match(element.get('k')):
            keys['lower_colon']+=1
        elif problemchars.search(element.get('k')):
            keys['problemchars']+=1
        else:
            keys['other']+=1
        
    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertion below will be incorrect then.
    # Note as well that the test function here is only used in the Test Run;
    # when you submit, your code will be checked against a different dataset.
    keys = process_map('chengdu_china.osm')
    pprint.pprint(keys)

if __name__ == "__main__":
    test()