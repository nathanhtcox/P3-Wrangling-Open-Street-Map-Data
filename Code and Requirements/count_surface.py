
from pymongo import MongoClient
import pprint

def count_surfaces(collection):
    
    surfaces = collection.aggregate([
        { "$group" : { "_id" : "$surface", "count" : { "$sum" : 1 } } },
        { "$sort" : { "count" : -1 } },
        { "$limit" : 11 }
    ])
    
    return surfaces 

def test():

    client = MongoClient ()
    db = client.test
    collection = db.toronto_small

    number_of_nodes = count_surfaces(collection)
    
    for a in number_of_nodes:
        pprint.pprint(a)

if __name__ == "__main__":
    test()



'''
	"_id" : ObjectId("57b26d63b6cba0b2193ab505"),
	"id" : "699540",
	"address" : {
		
	},
	"type" : "node",
	"pos" : [
		43.6751621,
		-79.361332
	],
	"created" : {
		"changeset" : "15661098",
		"user" : "andrewpmk",
		"version" : "11",
		"uid" : "1679",
		"timestamp" : "2013-04-09T01:43:19Z"
	}
}

'''
