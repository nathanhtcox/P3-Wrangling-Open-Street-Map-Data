
import xml.etree.cElementTree as ET
import pprint
import re

OSMFILE = "toronto_small.osm"

#expected postal code pattern A1A 1A1
post_code_re = re.compile(r'^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$') 

#most common incorrect postal code pattern A1A1A1
post_code_re2 = re.compile(r'^[A-Z][0-9][A-Z][0-9][A-Z][0-9]$')

def audit_post_code(post_code_types, post_code):
    m = post_code_re.search(post_code)
    n = post_code_re2.search(post_code)
    
    
    if n:  #matches the most common incorrect pattern (A1A1A1) and corrects by adding a space in the middle
        post_code = re.sub(r'^[A-Z][0-9][A-Z]', post_code[:3] + " ", post_code)
        print post_code      
    elif not m: #postal codes that do not match the expected pattern (A1A 1A1) are added to the list for visual inspection    
        if post_code not in post_code_types:
            post_code_types[post_code] = 1
        else:
            post_code_types[post_code] += 1


def is_post_code(elem):
    return (elem.attrib['k'] == "addr:postcode")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    post_code_types = {}
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_post_code(tag):
                    audit_post_code(post_code_types, tag.attrib['v'])
    
    osm_file.close()
    return post_code_types


def test():
    post_code_types = audit(OSMFILE)
    pprint.pprint(dict(post_code_types))


if __name__ == '__main__':
    test()
