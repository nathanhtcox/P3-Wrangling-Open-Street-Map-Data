#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json


problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
addr = re.compile(r'(?:addr:).*')

#expected postal code pattern A1A 1A1
post_code_re = re.compile(r'^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$') 

#most common incorrect postal code pattern A1A1A1
post_code_re2 = re.compile(r'^[A-Z][0-9][A-Z][0-9][A-Z][0-9]$')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

street_mapping = {     "St": "Street",
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


city_mapping = {  'City of Brampton' : 'Brampton',
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


def clean_post_code(post_code):
    
    #matches the most common incorrect pattern (A1A1A1) and corrects by adding a space in the middle
    if post_code_re.search(post_code):  
        return post_code
              
    #postal codes that do not match the expected pattern (A1A 1A1) are added to the list for visual inspection    
    elif post_code_re2.search(post_code): 
        return re.sub(r'^[A-Z][0-9][A-Z]', post_code[:3] + " ", post_code)

    else:
        return None


def clean_city(city_name):
    if city_name in city_mapping:
        return city_mapping[city_name]
    else:
        return city_name

def clean_streen_names(street_name):
    if street_name in street_mapping:
        return street_mapping[street_name]
    else:
        return street_name

def shape_element(element):
    node = {}
    node['pos']=[]
    
    if element.tag == "node" or element.tag == "way" :
        node['type'] = element.tag
        
        if 'lat' in element.attrib:
            node['pos'].append(float(element.attrib['lat']))
            
            if 'lon' in element.attrib:
                node['pos'].append(float(element.attrib['lon']))
        
        
        node['created']={}
            
        for k,v in element.attrib.iteritems():
            if k in CREATED:
                node["created"][k]=v
            elif k=='k':
                print k, v
            elif k!='lon' and k!='lat':
                node[k]=v
        
        
        node['address']={}
        
        for child in element.iter('tag'):
            k = child.attrib['k']
            v = child.attrib['v']
            
            if not problemchars.match(k):
                if addr.match(k):
                    after_addr = k.partition("addr:")[2]
                    
                    if after_addr == 'postcode':
                        node['address'][after_addr] = clean_post_code(v)
                    
                    elif after_addr == 'city':
                        node['address'][after_addr] = clean_city(v)
                        
                    elif after_addr == 'street':
                        node['address'][after_addr] = clean_streen_names(v)
                    
                    elif ':' not in after_addr:
                        try:
                            node['address'][after_addr] = v
                        except:
                            pass
                            
                else:
                    if ':' in k:
                        a = k.partition(':')[0] 
                        b = k.partition(':')[2]
                        node[a]={}
                        node[a][b] = v
                    elif k!='address':
                        node[k]=v
                        print "tag added", k, v
           
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    #data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                #data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return 10
    #return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('toronto_small.osm', True)
    #pprint.pprint(data)
    
    

if __name__ == "__main__":
    test()
