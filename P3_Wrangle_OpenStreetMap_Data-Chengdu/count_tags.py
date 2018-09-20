#解析数据
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    # YOUR CODE HERE
    tags = {}
    tree = ET.parse(filename)
    root = tree.getroot()
    tags.update({root.tag:1})
    def walkData(root, tags): 
        #遍历每个子节点 
        children_node = root.getchildren() 
        for child in root:
            if child.tag not in tags:
                tags.update({child.tag:1})
            else:
                tags[child.tag]+=1
        if len(children_node) == 0: 
            return  
        for child in children_node: 
            walkData(child, tags) 
    walkData(root, tags)            
    return tags
    

def test():
    tags = count_tags('chengdu_china.osm')
    pprint.pprint(tags)

test()