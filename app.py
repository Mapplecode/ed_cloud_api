from flask import Flask,render_template,request,Response,make_response,redirect
import requests
import datetime
from datetime import date

app = Flask(__name__)


import mediacloud.api, json, datetime

# ID KEYWORDS AND KEY TO BE ADDED HERE

my_key = 'c803be725711cdedd89941f2ff63a95c07457583f0ed355e50b58fc4d0ca3969'
value1 = 'phone'
value2 = 'Colombia'
media_Id = 'AND media_id:'+(str(1))
no_of_stories = 1

from_date_start =  datetime.date(2019,1,1)
till_date_end =  datetime.date(2020,1,1)
###################


def feeds(my_key,value1,value2,media_Id,no_of_stories,from_date_start,till_date_end):
    mc = mediacloud.api.MediaCloud(my_key)
    fetch_size = 10
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




@app.route('/')
def hello_world():
    return render_template('url_data.html')


@app.route('/get_data',methods = ['GET','POST'])
def get_data():
    param = ''
    if request.method == 'GET':
        param = request.args
    if request.method == 'POST':
        param = request.form
    try:
        to_ = param.get('to')
        from_ = param.get('from')
        key1 = param.get('key1')
        key2 = param.get('key2')
        count = param.get('key2')
        response_type =param.get('response_type')
        send_url=False
        print(to_,from_)
        if count == '' or count == None:
            try:
                count = int(count)
            except:
                count = no_of_stories
        else:
            count = no_of_stories
        if to_ == '' or to_ == None:
            to_ = datetime.datetime.now().date()
        else:
            to_ = datetime.datetime.strptime(to_,'%Y-%m-%d')

        if from_ == '' or from_ == None:
            from_ = date(date.today().year, 1, 1)
        else:
            from_ = datetime.datetime.strptime(from_,'%Y-%m-%d')
        stories = feeds(my_key,key1,key2,media_Id,count,from_,to_)
        # return render_template('index.html',context=json.dump(stories))
        url_list = []
        for i in stories:
            if 'Rss' in i['url'] or 'rss' in i['url'] or 'RSS' in i['url'] :
                test_request = str(requests.get(i['url']).status_code)
                print(test_request)
                if test_request == '200' or '200' in test_request:
                    send_url = i['url']
                    print(i['url'])
                title = (i['title'])
                c_date = str(i['collect_date'])
                p_date = str(i['publish_date'])
                media_name = str(i['media_name'])
                media_url = str(i['media_url'])
                story_tags = str(i['story_tags'])
                url = i['url']
                dict1 = {'title':title,'p_date':p_date,'url':url,'c_date':c_date,'media_name':media_name,
                         'media_url':media_url,'story_tags':story_tags}
                url_list.append(dict1)
        else:
            pass
            # return render_template('index.html', context=url_list,key1=key1,key2=key2,
            #                        to_=str(to_)[0:10],from_=str(from_)[0:10])
        if send_url:
            print(send_url)
            return redirect(send_url)
        return render_template('url_data.html', context=url_list)
    except:
        return render_template('index.html')




@app.route('/get_xml',methods = ['GET','POST'])
def get_file():
    param = ''
    if request.method == 'GET':
        param = request.args
    if request.method == 'POST':
        param = request.form
    # try:
    to_ = param.get('to')
    from_ = param.get('from')
    key1 = param.get('key1')
    key2 = param.get('key2')
    count = param.get('key2')
    response_type =param.get('res')
    print(to_,from_)
    if count == '' or count == None:
        try:
            count = int(count)
        except:
            count = no_of_stories
    else:
        count = no_of_stories
    if to_ == '' or to_ == None:
        to_ = datetime.datetime.now().date()
    else:
        to_ = datetime.datetime.strptime(to_,'%Y-%m-%d')

    if from_ == '' or from_ == None:
        from_ = date(date.today().year, 1, 1)
    else:
        from_ = datetime.datetime.strptime(from_,'%Y-%m-%d')
    stories = feeds(my_key,key1,key2,media_Id,count,from_,to_)
    # return render_template('index.html',context=json.dump(stories))
    url_list = []
    for i in stories:
        print(i['url'])
        if 'Rss' in i['url'] or 'rss' in i['url'] or 'RSS' in i['url'] :
            url_list.append(i['url'])
    url_file= open('url_file.txt','w')
    for urls in url_list:
        url_file.write(str(urls)+'\n')
    url_file.close()
    bar = ''
    bar += '<html><body><myurls xmlns:xlink="http://www.w3.org/1999/xlink">'
    for urls in url_list:
        bar+='<url>'
        bar += '<inurl xlink:type="simple" xlink:href="'+str(urls)+'">'+str(urls)+'</inurl>'
        bar+='</url>'
    bar += '</myurls></body></html>'
    bar = bar.replace('&','&amp;')
    xml_response = make_response(bar)
    xml_response.headers['Content-Type'] = 'text/xml; charset=utf-8'
    # if response_type == 'rss':
    return xml_response
        # else:
        #     return render_template('index.html', context=url_list,key1=key1,key2=key2,
        #                            to_=str(to_)[0:10],from_=str(from_)[0:10])
    # except:
    #     return render_template('index.html')
