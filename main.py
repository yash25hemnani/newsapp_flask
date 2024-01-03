        # import libraries
import json

from flask import Flask, render_template, request, jsonify, redirect
from newsapi import *
import requests
from flask_mail import Mail, Message
import datetime

with open("config.json", 'r') as c:
    params = json.load(c)["params"]

import socket
socket.getaddrinfo('127.0.0.1', 5000)

def date_reversal(str):
    sp_from = str.split("-")
    print(sp_from)
    new_lis = []
    j = -1
    for i in range(len(sp_from)):
        new_lis.append(sp_from[j])
        j = j - 1

    print(new_lis)
    str = "-".join(new_lis)
    return str


key_url = str()
domain_url = str()
cc_url = str()
key_counter = 0
domain_counter = 0
cc_counter = 0
# API Key
api_key = '17d6f5bde2a243acadf60a0e8eac1f68'

# init flask app
app = Flask(__name__, template_folder='template')


@app.route('/', methods=['GET', 'POST'])
@app.route('/home/1', methods=['GET', 'POST'])
def home():
    page = 1
    url = ('https://newsapi.org/v2/everything?'
           'q=America&'
           'sortBy=popularity&'
           'apiKey=17d6f5bde2a243acadf60a0e8eac1f68')

    response = requests.get(url)
    articles = response.json()['articles'][0:5]
    total_item = 0
    for item in response.json()['articles']:
        total_item = total_item + 1

    last_page = total_item // 5
    last_page_num = last_page
    last_page = str(last_page)
    return render_template('index.html', articles=articles, last_page=last_page, page=page, last_page_num=last_page_num)


@app.route('/home/<int:page>', methods=['GET', 'POST'])
def paginated(page):
    url = ('https://newsapi.org/v2/everything?'
           'q=India&'
           'sortBy=popularity&'
           'apiKey=17d6f5bde2a243acadf60a0e8eac1f68')
    try:

        response = requests.get(url)

        articles = response.json()['articles'][5 * (page - 1):5 * (page)]
        total_item = 0
        for item in response.json()['articles']:
            total_item = total_item + 1
        last_page = total_item // 5
        last_page_num = last_page
        last_page = str(last_page)
        return render_template('index.html', articles=articles, page=page, last_page=last_page, last_page_num=last_page_num)
    except Exception as e:
        return render_template('error.html')
    # return str(total_item)


# @app.route('/key_search', methods = ['GET', 'POST'])
@app.route('/key_search/1', methods=['GET', 'POST'])
def key_search():
    global key_url
    page = 1
    if key_counter == 0:
        search = request.form.get('search_term')
        searchin = request.form.get('searchin')
        fromdate = request.form.get('from')
        todate = request.form.get('to')
        sortby = request.form.get('sortby')
        fromdate = date_reversal(f"{fromdate}")
        todate = date_reversal(f"{todate}")
        key_url = ('https://newsapi.org/v2/everything?'
                   f'q="{search}"&'
                   f'searchIn={searchin}&'
                   f'from={fromdate}&'
                   f'to={todate}&'
                   f'sortby={sortby}&'
                   'apiKey=17d6f5bde2a243acadf60a0e8eac1f68')
        try:
            response = requests.get(key_url)
            articles = response.json()['articles'][0:5]

            total_item = 0
            for item in response.json()['articles']:
                total_item = total_item + 1

            last_page = total_item // 5
            last_page_num = last_page
            last_page = str(last_page)
            return render_template('key_news.html', articles=articles, page=page, last_page=last_page,
                               last_page_num=last_page_num)
        except Exception as e:
            return render_template('error.html')
    else:
        url = key_url
        try:
            response = requests.get(url)
            articles = response.json()['articles'][0:5]

            total_item = 0
            for item in response.json()['articles']:
                total_item = total_item + 1

            last_page = total_item // 5
            last_page_num = last_page
            last_page = str(last_page)
            return render_template('key_news.html', articles=articles, page=page, last_page=last_page, last_page_num=last_page_num)

        except Exception as e:
            return render_template('error.html')
        # return response.json()


@app.route('/key_search/<int:page>', methods=['GET', 'POST'])
def paginated_key_search(page):
    global key_counter
    key_counter = key_counter + 1
    url = key_url
    try:
        response = requests.get(url)

        articles = response.json()['articles'][5 * (page - 1):5 * (page)]
        total_item = 0
        for item in response.json()['articles']:
            total_item = total_item + 1
        last_page = total_item // 5
        last_page_num = last_page
        last_page = str(last_page)
        return render_template('key_news.html', articles=articles, page=page, last_page=last_page,
                               last_page_num=last_page_num)
    except Exception as e:
        return render_template('error.html')
    # return str(total_item)


@app.route('/domain_search/1', methods=['GET', 'POST'])
def domain_search():
    page = 1
    global domain_url
    if domain_counter == 0:
        search = request.form.get('search_term')
        searchin = request.form.get('searchin')
        fromdate = request.form.get('from')
        todate = request.form.get('to')
        sortby = request.form.get('sortby')
        fromdate = date_reversal(f"{fromdate}")
        todate = date_reversal(f"{todate}")
        domain = request.form.get('domain')
        edomain = request.form.get('edomain')
        if domain == 'all':
            if edomain == 'none':
                domain_url = ('https://newsapi.org/v2/everything?'
                              f'q="{search}"&'
                              f'searchIn={searchin}&'
                              f'from={fromdate}&'
                              f'to={todate}&'
                              f'sortby={sortby}&'
                              'apiKey=17d6f5bde2a243acadf60a0e8eac1f68')
            else:
                domain_url = ('https://newsapi.org/v2/everything?'
                              f'q="{search}"&'
                              f'searchIn={searchin}&'
                              f'from={fromdate}&'
                              f'to={todate}&'
                              f'sortby={sortby}&'
                              f'excludeDomains={edomain}&'
                              'apiKey=17d6f5bde2a243acadf60a0e8eac1f68')
        else:
            if edomain == 'none':
                domain_url = ('https://newsapi.org/v2/everything?'
                              f'q="{search}"&'
                              f'searchIn={searchin}&'
                              f'from={fromdate}&'
                              f'to={todate}&'
                              f'sortby={sortby}&'
                              f'doamins={domain}&'
                              'apiKey=17d6f5bde2a243acadf60a0e8eac1f68')
            else:
                domain_url = ('https://newsapi.org/v2/everything?'
                              f'q="{search}"&'
                              f'searchIn={searchin}&'
                              f'from={fromdate}&'
                              f'to={todate}&'
                              f'sortby={sortby}&'
                              f'doamins={domain}&'
                              f'excludeDomains={edomain}&'
                              'apiKey=17d6f5bde2a243acadf60a0e8eac1f68')
        try:
            response = requests.get(domain_url)
            articles = response.json()['articles'][0:5]
            total_item = 0
            for item in response.json()['articles']:
                total_item = total_item + 1

            last_page = total_item // 5
            last_page_num = last_page
            last_page = str(last_page)
            return render_template('dom_news.html', articles=articles, last_page=last_page, page=page,
                                   last_page_num=last_page_num)
        except Exception as e:
            return render_template('error.html')

    else:
        url = domain_url
        try:
            response = requests.get(url)
            articles = response.json()['articles'][0:5]
            total_item = 0
            for item in response.json()['articles']:
                total_item = total_item + 1

            last_page = total_item // 5
            last_page_num = last_page
            last_page = str(last_page)
            return render_template('dom_news.html', articles=articles, last_page=last_page, page=page,
                                   last_page_num=last_page_num)
        except Exception as e:
            return render_template('error.html')


@app.route('/domain_search/<int:page>', methods=['GET', 'POST'])
def paginated_dom_search(page):
    global domain_url
    domain_url += 1
    url = domain_url
    try:
        response = requests.get(url)

        articles = response.json()['articles'][5 * (page - 1):5 * (page)]
        total_item = 0
        for item in response.json()['articles']:
            total_item = total_item + 1
        last_page = total_item // 5
        last_page_num = last_page
        last_page = str(last_page)
        return render_template('dom_news.html', articles=articles, page=page, last_page=last_page,
                               last_page_num=last_page_num)
    except Exception as e:
        return render_template('error.html')


@app.route('/cc_search/1', methods=['GET', 'POST'])
def cc_search():
    page = 1
    global cc_url
    if (cc_counter == 0):
        search = request.form.get('search_term')
        country = request.form.get('country')
        category = request.form.get('category')


        cc_url = ('https://newsapi.org/v2/top-headlines?'
                  f'country={country}&'
                  f'category={category}&'
                  'apiKey=17d6f5bde2a243acadf60a0e8eac1f68')
        try:
            response = requests.get(cc_url)
            articles = response.json()['articles'][0:5]
            total_item = 0
            for item in response.json()['articles']:
                total_item = total_item + 1

            last_page = total_item // 5
            last_page_num = last_page
            last_page = str(last_page)
            return render_template('cc_news.html', articles=articles, last_page=last_page, page=page,
                                   last_page_num=last_page_num)
        except Exception as e:
            return render_template('error.html')
    else:
        url = cc_url
        try:
            response = requests.get(url)
            articles = response.json()['articles'][0:5]
            total_item = 0
            for item in response.json()['articles']:
                total_item = total_item + 1

            last_page = total_item // 5
            last_page_num = last_page
            last_page = str(last_page)
            return render_template('cc_news.html', articles=articles, last_page=last_page, page=page,
                                   last_page_num=last_page_num)
        except Exception as e:
            return render_template('error.html')


@app.route('/cc_search/<int:page>', methods=['GET', 'POST'])
def paginated_cc_search(page):
    global cc_counter
    cc_counter = cc_counter + 1
    url = cc_url
    try:
        response = requests.get(url)
        articles = response.json()['articles'][5 * (page - 1):5 * (page)]
        total_item = 0
        for item in response.json()['articles']:
            total_item = total_item + 1
        last_page = total_item // 5
        last_page_num = last_page
        last_page = str(last_page)
        return render_template('cc_news.html', articles=articles, page=page, last_page=last_page,
                               last_page_num=last_page_num)
    except Exception as e:
        return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
