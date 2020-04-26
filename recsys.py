from flask import Flask,request
import json
app = Flask(__name__)

import app as domain

user_details = [{"id":"1","name":"Svijay","score":"130","city":"Chennai","imgURL":"https:\/\/demonuts.com\/Demonuts\/SampleImages\/roger.jpg"},
                  {"id":"2","name":"annonymousDevil","score":"32","city":"Coimbatore","imgURL":"https:\/\/demonuts.com\/Demonuts\/SampleImages\/nadal.jpg"},
                  {"id":"3","name":"dark_knight","score":"95","city":"Bangalore","imgURL":"https:\/\/demonuts.com\/Demonuts\/SampleImages\/djoko.jpg"},
                  {"id":"4","name":"mudblood","score":"41","city":"Delhi","imgURL":"https:\/\/demonuts.com\/Demonuts\/SampleImages\/murray.jpg"},
                  {"id":"5","name":"Elderwand","score":"30","city":"Indore","imgURL":"https:\/\/demonuts.com\/Demonuts\/SampleImages\/shara.jpg"},
                  {"id":"6","name":"darklord","score":"120","city":"Hyderabad","imgURL":"https:\/\/demonuts.com\/Demonuts\/SampleImages\/woz.jpg"},
                  {"id":"7","name":"goldminer","score":"71","city":"Mangalore","imgURL":"https:\/\/demonuts.com\/Demonuts\/SampleImages\/bou.png"},
                  {"id":"8","name":"pythonFlask","score":"20","city":"Chennai","imgURL":"https:\/\/demonuts.com\/Demonuts\/SampleImages\/iva.jpg"}]


@app.route('/getUserDetails', methods=['GET'])
def get_user_details():
    uname = request.form['Username']
    details = domain.get_user_details(uname)
    if details:
        print (details)
        return {
            "Username": details['Username'],
            "IconUrl": details['IconUrl'] if "IconUrl" in details else '',
            "UserScore": details['UserScore'] if "UserScore" in details else '',
            "CurrentActivity": details['CurrentActivity'] if "CurrentActivity" in details else ''
        }
    else:
        return {}

@app.route('/registerUser', methods=['POST'])
def register_user():
    uname = request.form['Username']
    age = request.form['Age']
    survey = json.loads(request.form['Survey'])
    user_long = request.form['UserLongitude']
    user_lat = request.form['UserLatitude']
    updated_uname = domain.register_user(
        uname, age, survey, user_lat, user_long)
    if updated_uname:
        return {
            "Username": updated_uname
        }
    else:
        return {}

@app.route('/leaderboard', methods=['GET'])
def get_leader_board():
    #uname = request.form['Username']
    top_10 = domain.get_top_ten()
    if top_10:
        return {
            'leaderboard': [{
                "Username": user['Username'],
                "Score": user["TotalPoints"] if "TotalPoints" in user else 'NA',
                "IconUrl": user["IconUrl"] if "IconUrl" in user else ''
            } for user in top_10]
        }
    else:
        return { 'leaderboard': [] }


@app.route('/getSensorValues', methods=['POST'])
def getsensorvalues():
    if request.method == 'POST':
        print(request.form['userid'])
        print("sensor values:")
        print(json.loads(request.form['sensorvalues']))
        print("gps values:")
        print( json.loads(request.form['gpsvalues']))
        return 'received'


@app.route('/getUserResponse', methods=['POST'])
def get_user_response():
    uname = request.form['Username']
    ans = request.form['Answer']
    if ans == 'bad':
        domain.mqpqalter(uname, 'm', -2)
    if ans == 'ok':
        domain.mqpqalter(uname, 'm', -1)
    return 'received'

@app.route('/updateFeedback', methods=['POST'])
def update_feedback():
    uname = request.form['Username']
    aid = request.form['taskId']
    completed = request.form['Completed']
    rat = request.form['Rating']
    domain.addpts(aid, uname, completed == 'true')
    domain.feedback(aid, uname, int(rat))
    return 'received'


@app.route('/getSuggestion', methods=['POST'])
def get_suggestion():
    time = request.form['time']
    uname = request.form['uname']
    activity = domain.suggest(time, uname)
    return { 'taskId': activity['Aid'] } if activity else {}


@app.route('/getTaskDetails', methods=['POST'])
def get_task_details():
    tid = request.form['TaskId']
    details = domain.get_task_details(int(tid))
    if details:
        return {
            'taskName': details['Aname'],
            'taskDescription': details['Adesc'],
            'taskCategory': details['class'],
            'taskRating': details['rat'],
            'taskImageUrl': details['guidelink'],
            'taskMinTime': details['mintime'],
            'taskRestTime': details['resttime']
        }
    else:
        return {}


@app.route('/getDailyChallenges', methods=['GET'])
def get_daily_challenges():
    daily_tasks = {}
    dc_list = domain.get_dc()
    if dc_list:

        return {"tasks":[{
                'id': task['Aid'],
                'desc': task['Adesc'],
                'imgurl': task['imgurl']
            } for task in domain.get_dc()]}
    else:
        return {}


@app.route('/setProfilePic',methods=['POST'])
def set_dp():
    uname = request.form['Username']
    dp = request.form['IconUrl']
    if dp:
        return domain.update_dp(uname, dp)
    else:
        return ''
    

@app.route('/validateUsername',methods=['GET'])
def validate_username():
    uname = request.form['Username']
    exists = domain.validate_user(uname)
    return { 'exists': exists } if exists else {}


@app.route('/')
def index():
    return "hello"

if __name__ == '__main__':
    app.run(port=4000)