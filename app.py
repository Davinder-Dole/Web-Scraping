from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars_app")


@app.route("/")
def index():
    listings = mongo.db.listings.find_one()
    return render_template("index.html", listings=listings)


@app.route("/scrape")
def scrape():
    listings = mongo.db.listings
    listings_data = scrape_mars.scrape_mars_news()
    listings_data = scrape_mars.scrape_mars_image()
    listings_data = scrape_mars.scrape_mars_facts()
    listings_data = scrape_mars.scrape_mars_weather()
    listings_data = scrape_mars.scrape_mars_hemispheres()
    listings.update({}, listings_data, upsert=True)
    return "finish scraping"
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
