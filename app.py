from script2 import feeds
from flask import Flask,render_template
import json
import datetime
import pprint
app = Flask(__name__)
my_key = 'c803be725711cdedd89941f2ff63a95c07457583f0ed355e50b58fc4d0ca3969'
value1 = 'phone'
value2 = 'India'
media_Id = 'AND media_id:'+(str(1))
no_of_stories = 1
from_date_start =  datetime.date(2019,1,1)
till_date_end =  datetime.date(2020,1,1)


@app.route('/')
def hello_world():
    stories = feeds(my_key,value1,value2,media_Id,no_of_stories,from_date_start,till_date_end)
    # return render_template('index.html',context=json.dump(stories))
    pprint.pprint(json.dumps(stories))
    return json.dumps(stories)


    