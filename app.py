from flask import Flask,render_template,request,Response,make_response,redirect
import requests
import datetime
from datetime import date,timedelta
from datetime import timedelta

app = Flask(__name__)


import mediacloud.api, json, datetime

# ID KEYWORDS AND KEY TO BE ADDED HERE

# my_key = 'ee9f47b5ff3e711f98904d23fda6e3ccfd6f97f039f484a4013646e4c5388e0d'
value1 = 'phone'
value2 = 'Colombia'
media_Id = 'AND media_id:'+(str(1))
no_of_stories = 100

from_date_start =  datetime.date(2019,1,1)
till_date_end =  datetime.date(2020,1,1)
###################


def feeds(value1,value2,media_Id,no_of_stories,from_date_start,till_date_end,
          my_key='ee9f47b5ff3e711f98904d23fda6e3ccfd6f97f039f484a4013646e4c5388e0d'):
    if my_key == None or my_key == '':
        my_key= 'ee9f47b5ff3e711f98904d23fda6e3ccfd6f97f039f484a4013646e4c5388e0d'
    mc = mediacloud.api.MediaCloud(my_key)
    fetch_size = 110
    stories = []
    last_processed_stories_id = 0
    while len(stories) < no_of_stories:
        fetched_stories = mc.storyList(value1+' AND "'+value2+'" ',
                                       solr_filter=mc.dates_as_query_clause(from_date_start,till_date_end),
                                       last_processed_stories_id=last_processed_stories_id, rows= fetch_size)
        stories.extend(fetched_stories)
        if len( fetched_stories) < fetch_size:
            break
        last_processed_stories_id = stories[-1]['processed_stories_id']
    return stories




@app.route('/',methods = ['GET','POST'])
def hello_world():
    return redirect('/get_data')


@app.route('/get_data',methods = ['GET','POST'])
def get_data():
    param = ''
    to_=str(datetime.date.today())
    from_=str(datetime.date.today())
    list_of_urls = list()
    if request.method == 'GET':
        param = request.args
    if request.method == 'POST':
        param = request.form
    try:
        to_ = str(param.get('to'))
        from_ = str(param.get('from'))
        key1 = param.get('key1')
        key2 = param.get('key2')
        count = param.get('count')
        code = None
        code = param.get('code')
        response_type =param.get('response_type')
        send_url=False
        if count == '' or count == None:
            try:
                count = int(count)
            except:
                count = no_of_stories
        else:
            count = no_of_stories
        if to_ == '' or to_ == None or to_ == 'None':
            to_ = (datetime.datetime.now().date())
        else:
            to_ = (datetime.datetime.strptime(to_,'%Y-%m-%d'))

        if from_ == '' or from_ == None or from_ == 'None':
            from datetime import timedelta
            from_ = datetime.date.today() - timedelta(365)
        else:
            from_ = datetime.datetime.strptime(from_,'%Y-%m-%d')
        if key1 == None:
            key1 = ''
        if key2 == None:
            key2 = ''
        if code == None:
            code = ''

        stories = feeds(value1=key1, value2=key2, media_Id=media_Id, no_of_stories=50, from_date_start=from_,
                    till_date_end=to_,my_key=code)

        data_list = []
        for i in stories:
            data_list.append(i['url'])
        from datetime import timedelta
        day_1 = datetime.date.today() - timedelta(365)
        today = datetime.datetime.now().date()
        print(str(day_1),str(today))
    except Exception as e:
        print('LAST EXCEPTION')
        print(e)
        return render_template('index.html',to_=to_,from_=from_)
    return render_template('index2.html',data = data_list,key1=key1,key2=key2,to_=to_,from_=from_)
