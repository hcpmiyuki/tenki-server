from bs4 import BeautifulSoup
import requests
import os 
import flask 
from main import app
import json

res = requests.get('https://tenki.jp/indexes/cloth_dried/3/16/4410/')
soup = BeautifulSoup(res.text, "html.parser")
weather_status = {"部屋干し推奨":"heyaboshi", "よく乾く":"yoku", "やや乾く":"yaya", "乾く":"kawaku", "大変よく乾く":"taihen"}

@app.route('/tomorrow-weather')
def get_tomorrow_washing():
    # 明日の洗濯指数
    tomorrow_weather = soup.find_all("span", attrs={"class", "indexes-telop-0"})[1].text
    
    if tomorrow_weather in weather_status:
        tomorrow_weather_status = weather_status[tomorrow_weather]
    else:
        tomorrow_weather_status = None
    
    return tomorrow_weather_status


@app.route('/today-weather')
def get_today_washing():
    # 今日の洗濯指数
    today_weather = soup.find_all("span", attrs={"class", "indexes-telop-0"})[0].text
 
    if today_weather in weather_status:
        today_weather_status = weather_status[today_weather]
    else:
        today_weather_status = None

    return today_weather_status


@app.route('/today-tomorrow-weather')
def get_washing():
    # 今日と明日の洗濯指数
    weather = soup.find_all("span", attrs={"class", "indexes-telop-0"})
    today_tomorrow_weather_status = {}

    # today
    if weather[0].text in weather_status:
        today_tomorrow_weather_status["today"] = weather_status[weather[0].text]
    else:
        today_tomorrow_weather_status["today"] = None

    # tomorrow
    if weather[1].text in weather_status:
        today_tomorrow_weather_status["tomorrow"] = weather_status[weather[1].text]
    else:
        today_tomorrow_weather_status["tomorrow"] = None


    return json.dumps(today_tomorrow_weather_status, ensure_ascii=False)


@app.route('/weekly-weather')
def get_weekly_washing():
    # 一週間のの洗濯指数
    weekly_weather = soup.find_all("p", attrs={"class", "indexes-telop-0"})
    weekly_date = soup.find_all("td", attrs={"class", "cityday"})
    weekly_weather_status = [{"date": weekly_date[i].text, "status": weather_status[weekly_weather[i].text] if weekly_weather[i].text in weather_status else None} for i in range(len(weekly_weather))]
      
    return json.dumps(weekly_weather_status, ensure_ascii=False)
