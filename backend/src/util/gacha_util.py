import random
import pymongo
from flask import current_app
import json
import src
from threading import Thread

def roll_single_gacha(two_stars_guaranteed=False):
    pass

def roll_gacha(gacha_count):
    mongo_client = current_app.mongo_client
    gacha_prob = [0, 0.785, 0.185, 0.03]
    gacha_prob_two_stars_guaranteed = [0.185, 0.03]

    cursor = mongo_client.local.students.find( {"affordable" :{"$eq": True} } )
    canditates = [[] for i in range(3+1)]
    for i in cursor:
        canditates[i["stars"]].append(i)

    ret = []

    for i in range(gacha_count):
        p = random.random()
        if i % 10 == 9:
            p *= gacha_prob_two_stars_guaranteed[0] + gacha_prob_two_stars_guaranteed[1]
            if p >= gacha_prob[2]:
                stars = 3
            else:
                stars = 2
        else:
            if p >= gacha_prob[1] + gacha_prob[2]:
                stars = 3
            elif p >= gacha_prob[1]:
                stars = 2
            else:
                stars = 1
        row = canditates[stars][random.randint(0, len(canditates) - 1)].copy()
        row.pop("_id")
        ret.append(row)

    return ret