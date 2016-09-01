"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
from json import dumps, loads, JSONEncoder, JSONDecoder
import pickle

OSMFILE = "toronto_small.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "West", "East", "North", "South", "Way", "Townline", "Terrace",
            "Wood", "Walk", "Vineway", "Sideroad", "Run", "Row", "Ridge", "Starway", "Promenade", "Path", 
            "Pathway", "Point", "Park", "Millway", "Mews", "Meadoway", "Manor", "Line", "Landing", 
            "Hollow", "Hill", "Highway", "Heights", "Grove", "Gate", "Gardens", "Crescent", "Fernway", 
            "Crossing", "Garden", "Common", "Concession", "Close", "Circuit", "Circle" ]

# UPDATE THIS VARIABLE
mapping = {     "St": "Street",
                "St.": "Street",
                "Ave": "Avenue",
                "Ave." : "Avenue",
                "Rd.": "Road",
                "Rd" : "Road",
                "W." : "West",
                "E." : "East",
                "N." : "North",
                "S." : "South",
                "W" : "West",
                "E" : "East",
                "N" : "North",
                "S" : "South",
                "Unionville" : "",
                "Tottenham" : "",
                "Hrbr" : "Harbour",
                "Dr" : "Drive",
                "EHS" : "",
                "Cresent" : "Crescent",
                "By-pass" : "Bypass",
                "Blvd" : "Boulevard",
                "Blvd." : "Boulevard",
                "Alliston" : "",
                "Adjala" : "",
                "Beeton" : "",
                 "By-pass" : "Bypass"
                 }


#mapping = {}

class PythonObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, unicode, int, float, bool, type(None))):
            return JSONEncoder.default(self, obj)
        return {'_python_object': pickle.dumps(obj)}

def as_python_object(dct):
    if '_python_object' in dct:
        return pickle.loads(str(dct['_python_object']))
    return dct


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
    
    osm_file.close()
    print "Audit complete"
    return street_types


def update_name(name, mapping):
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if street_type in mapping:
            name = re.sub(street_type_re, mapping[street_type], name)
    
    #print name 
    return name


def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))
    
    #with open('nonstd_street_types.json', 'w') as fp:
    #   dumps(st_types, fp, sort_keys=True, indent=4, cls=PythonObjectEncoder)

    #with open('nonstd_street_types.pickle', 'wb') as fp:
    #    pickle.dump(st_types, fp)


    #for st_type, ways in st_types.iteritems():
    #    for name in ways:
    #        better_name = update_name(name, mapping)
            


if __name__ == '__main__':
    test()
