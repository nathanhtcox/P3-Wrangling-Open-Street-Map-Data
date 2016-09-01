from pymongo import MongoClient
import pprint

def aggregate_unique(collection):
    
    unique_users = collection.aggregate([
        { "$match": { "created.user": { "$exists": True } }},
        { "$group": { "_id": { "user": "$created.user" }, "count": { "$sum": 1 } } },
        { "$group" : { "_id" : None, "unique_users" : { "$sum" : 1 } } }
    ])
    
    return unique_users 

def test():

    client = MongoClient ()
    db = client.test
    collection = db.toronto_small

    unique_users = aggregate_unique(collection)
    
    for a in unique_users:
        pprint.pprint(a)

if __name__ == "__main__":
    test()



