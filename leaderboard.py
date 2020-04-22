from flask import Flask,request
import json
app = Flask(__name__)

user_details = [{"id":"1","name":"Svijay","score":"130","city":"Chennai","imgURL":"https:\/\/demonuts.com\/Demonuts\/SampleImages\/roger.jpg"},
                  {"id":"2","name":"annonymousDevil","score":"32","city":"Coimbatore","imgURL":"https:\/\/demonuts.com\/Demonuts\/SampleImages\/nadal.jpg"},
                  {"id":"3","name":"dark_knight","score":"95","city":"Bangalore","imgURL":"https:\/\/demonuts.com\/Demonuts\/SampleImages\/djoko.jpg"},
                  {"id":"4","name":"mudblood","score":"41","city":"Delhi","imgURL":"https:\/\/demonuts.com\/Demonuts\/SampleImages\/murray.jpg"},
                  {"id":"5","name":"Elderwand","score":"30","city":"Indore","imgURL":"https:\/\/demonuts.com\/Demonuts\/SampleImages\/shara.jpg"},
                  {"id":"6","name":"darklord","score":"120","city":"Hyderabad","imgURL":"https:\/\/demonuts.com\/Demonuts\/SampleImages\/woz.jpg"},
                  {"id":"7","name":"goldminer","score":"71","city":"Mangalore","imgURL":"https:\/\/demonuts.com\/Demonuts\/SampleImages\/bou.png"},
                  {"id":"8","name":"pythonFlask","score":"20","city":"Chennai","imgURL":"https:\/\/demonuts.com\/Demonuts\/SampleImages\/iva.jpg"}]


@app.route('/')
def index():
    return 'server working'


@app.route('/leaderboard')
def about():
    sorted_scores = sorted(user_details,key= lambda i: int(i['score']),reverse=True)
    return {"status":"true","message":"Data fetched successfully!",
          "data":sorted_scores}


@app.route('/getSensorValues',methods=['POST'])
def getsensorvalues():
    if request.method == 'POST':
        print(request.form['userid'])
        print("sensor values:")
        print(json.loads(request.form['sensorvalues']))
        print("gps values:")
        print( json.loads(request.form['gpsvalues']))
        return 'received'


@app.route('/getUserResponse',methods=['POST'])
def getUserResponse():
    if request.method == 'POST':
        print(request.form['userResponse'])
        return 'received'


if __name__ == '__main__':
    app.run(port=4000)
