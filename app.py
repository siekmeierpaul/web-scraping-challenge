from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")


@app.route('/')
def index():
    stuff = mongo.db.content.find_one()
    return render_template('index.html', mars=stuff)


@app.route('/scrape')
def scrape():
    scraped = mongo.db.content
    data = scrape_mars.scrape()
    scraped.update(
        {},
        data,
        upsert=True
    )
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
