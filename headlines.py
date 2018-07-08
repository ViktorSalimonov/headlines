import feedparser
from flask import Flask
from flask import render_template
from flask import request
import json
import urllib.request

app = Flask(__name__)
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=cece302746072401c1d3915a7bcdbcf4"
RSS_FEEDS = {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://www.iol.co.za/cmlink/1.640'
}
DEFAULTS = {'publication':'bbc',
            'city': 'London,UK'}

def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])

    return feed['entries']

def get_weather(query):
    query = urllib.request.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {'description':parsed['weather'][0]['description'],
                   'temperature':parsed['main']['temp'],
                   'city':parsed['name'],
                   'country':parsed['sys']['country']
        }
    return weather

@app.route("/")
def home():
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)

    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)

    return render_template("home.html",
                            articles=articles,
                            weather=weather)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
