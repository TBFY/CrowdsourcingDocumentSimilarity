import pandas as pd
import json
import mturk
import time
import pymongo
import sys
from datetime import datetime

""" Run this with 'python update_db.py x y' where x is 0 if using the sandbox, 1 if using the marketplace
and y is the amount of seconds to wait between loops """

create_hits_in_production = (sys.argv[1] == '1')
# Change the string in MongoClient to a connection string to a Mongodb base/cluster of your choice

db_client = pymongo.MongoClient(
    "mongodb+srv://<username>:<password>@cluster0-hjstc.mongodb.net/test?retryWrites=true&w=majority"
)
db = db_client['tbfy']
hit_result_collection = db.hit_results if create_hits_in_production else db.hit_results_sandbox

mt = mturk.MTurk()
mt.launch_client(create_hits_in_production)

fails = 0
while True:
    ''' Update all hits in the database with correct results '''
    hit_result_collection_list = list(hit_result_collection.find({'hit.HITStatus': {'$not': {'$eq': 'Disposed'}}}))
    for hit in hit_result_collection_list:
        try:
            hit_result_collection.update_one(
                {'_id': hit['_id']},
                {
                    "$set": {
                        "hit": mt.client.get_hit(HITId = hit['_id'])['HIT'],
                        'answers': mt.approve_and_get_hit_answers(hit['_id'])
                    }
                })
        except Exception as e:
            print(e)
            fails = fails + 1
            if fails > 4:
                sys.exit(-1)
            continue
    print('{}: Updated db has {} non-disposed entries'.format(datetime.now(),len(hit_result_collection_list)))
    time.sleep(int(sys.argv[2]))
