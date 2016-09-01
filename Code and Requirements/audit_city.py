
import xml.etree.cElementTree as ET
import pprint

OSMFILE = "toronto_small.osm"


# UPDATE THIS VARIABLE
mapping = {  'City of Brampton' : 'Brampton',
             'City of Burlington' : 'Burlington',
             'City of Hamilton': 'Hamilton',
             'City of Kawartha Lakes': 'Kawartha Lakes',
             'City of Oshawa': 'Oshawa',
             'City of Pickering': 'Pickering',
             'City of St. Catharines': 'St. Catherines',
             'City of Toronto': 'Toronto',
             'City of Vaughan': 'Vaughan',
             'Richmond Hill (Oak Ridges)': 'Richmond Hill',
             'Town of Ajax': 'Ajax',
             'Town of Aurora': 'Aurora',
             'Town of Bradford West Gwillimbury': 'Bradford West Gwillimbury',
             'Town of Caledon': 'Caledon',
             'Town of East Gwillimbury': 'East Gwillimbury',
             'Town of Erin': 'Erin',
             'Town of Grimsby': 'Grimsby',
             'Town of Halton Hills': 'Halton Hills',
             'Town of Innisfil': 'Innisfil',
             'Town of Markham': 'Markham',
             'Town of Milton': 'Milton',
             'Town of Mono': 'Mono',
             'Town of New Tecumseth': 'New Tecumseth',
             'Town of Newmarket': 'Newmarket',
             'Town of Niagara-On-The-Lake': 'Niagara-On-The-Lake',
             'Town of Whitby': 'Whitby',
             'Town of Whitchurch-Stouffville': 'Whitchurch-Stouffville'  }

def audit_city(city_types, city_name):
    if city_name not in city_types:
        city_types[city_name] = 1
    else:
        city_types[city_name] += 1


def is_city(elem):
    
    return (elem.attrib['k'] == "addr:city")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    city_types = {}
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_city(tag):
                    audit_city(city_types, tag.attrib['v'])
    
    osm_file.close()
    return city_types


def test():
    city_types = audit(OSMFILE)
    pprint.pprint(dict(city_types))


if __name__ == '__main__':
    test()
