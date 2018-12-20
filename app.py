from flask import Flask, render_template, request
import random
import requests
import json
from faker import Faker

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
    
@app.route('/lotto')
def lotto():
    # 요부분
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=837"
    res = requests.get(url).text
    lotto_dict = json.loads(res)
    print(lotto_dict["drwNoDate"])
    week_num = []
    bonusNum = lotto_dict["bnusNo"]
    for i in range(1,7):
        num = lotto_dict["drwtNo{}".format(i)]
        week_num.append(num)
    # print(type(res))
    # print(type(json.loads(res)))
    
    num_list = range(1,46)
    pick = random.sample(num_list,6)
    pick.sort()
    
    cnt=0
    for i in pick:
        if i in week_num:
            cnt+=1
    if cnt == 6:
        rank = '1'
    elif cnt == 5:
        if bonusNum in pick:
            rank = '2'
        else:
            rank = '3'
    elif cnt == 4:
        rank ='4'
    elif cnt == 3:
        rank ='5'
    else:
        rank='you fail'
    
    return render_template("lotto.html",lotto=pick, week_num=week_num, rank = rank)
    
@app.route('/ping')
def ping():
    return render_template("ping.html")
    
@app.route('/pong')
def pong():
    input_name = request.args.get('name')
    fake = Faker('ko_KR')
    fake_job = fake.job()
    return render_template("pong.html", html_name = input_name, fake_job = fake_job)
    