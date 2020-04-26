import pymongo
import random
from pymongo import MongoClient
cluster=MongoClient("mongodb+srv://root:password1!@cluster0-1ptya.mongodb.net/test?retryWrites=true&w=majority" )
db=cluster["test"]
collection=db["activity"]
pts=db["points"]
his=db["acthist"]
dc=db["daily"]

def suggest(time,uname):
    ch=predict(uname)
    if (ch=='p' or ch=='P'):
        ta=collection.find({"$and":[{"timeallowed":{"$eq":time,"$eq":"A"}},{"pf":{"$gte":5}},{"rat":{"$gte":random.choice([2,3])}}]})
    else:
        ta=collection.find({"$and":[{"timeallowed":{"$eq":time,"$eq":"A"}},{"mf":{"$gte":5}},{"rat":{"$gte":random.choice([2,3])}}]})
    ta=list(ta)
    return (random.choice(ta))


def predict(uname):
    userq = list(pts.find( { "Username": uname }, { "MQ": 1, "PQ": 1 ,"_id" :0 } ))
    mqval=userq[0].get("MQ")
    pqval = userq[0].get("PQ")
    if mqval>=pqval:
        return 'p'
    else:
        return('m')

def addpts(aid,uname,skip):
    if skip != True:
        userq = list(pts.find({"Username": uname}, {"MQ": 1, "PQ": 1, "_id": 0}))
        act = list(collection.find({"Aid": aid}, {"mf": 1, "pf": 1, "_id": 0}))

        pfval = act[0].get("pf")
        mfval = act[0].get("mf")
        mqval = userq[0].get("MQ") + act[0].get("mf")
        pqval = userq[0].get("PQ") + act[0].get("pf")
        tot = mfval + pfval
        pp = pts.update_one({"Username": uname}, {"$inc": {"MQ": mqval, "PQ": pqval, "TotalPoints": tot}})
        rec = list(pts.find({"Username": uname}))
        return rec[0]
    else:
        pp = pts.update_one({"Username": uname}, {"$inc": {"MQ": -3, "PQ": -2, "TotalPoints":-5 }})
        rec = list(pts.find({"Username": uname}))
        return rec[0]

def set_user_details(uname, gender, country, age, interest, mqval, pqval):
    mqval+=10
    pqval+=10
    tot=mqval+pqval
    pts.insert_one({
        "Username":uname,
        "MQ":mqval,
        "PQ":pqval,
        "Country":country,
        "TotalPoints":tot,
        "Gender":gender,
        "Interests":interest,
        "Age":age
    })
    rec = pts.find_one({"Username": uname})
    return rec

def register_user(uname, age, survey, user_lat, user_long):
    pts.insert_one({
        "Username": uname,
        "Age": age,
        "Survey": survey,
        "UserLatitude": user_lat,
        "UserLongitude":user_long
    })
    return uname


def get_user_details(uname):
    rec = pts.find_one({"Username": uname})
    return rec

def feedback(aid,uname,rating):
    act = list(collection.find({"Aid": aid}, {"rat": 1, "_id": 0}))
    his.insert_one({"Aid":aid,"Username":uname,"rating":rating})
    rating+= act[0].get("rat")
    rating/=2
    collection.update_one({"Aid":aid},{"$set":{"rat":rating}})
    return("updated")

def mqpqalter(uname,mtype,val):
    if mtype=='m':
        pts.update_one({"Username":uname},{"$inc":{"MQ":val}})
    else:
        pts.update_one({"Username": uname}, {"$inc": {"PQ": val}})
    return("Quotient updated")

def get_top_ten():
    return list(
        pts.aggregate([{"$sort": {"TotalPoints": -1}}, {"$limit": 10}]))


def get_task_details(aid):
    return collection.find_one({"Aid": aid})

def get_dc():
    return list(dc.find())

def update_dp(uname, dp):
    pts.update_one({"Username": uname}, {"$set":{"IconUrl": dp}})
    return dp


def validate_user(uname):
    user = pts.find_one({"Username": uname})
    return "true" if user else "false"







