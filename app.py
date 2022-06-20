from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    # find one document from our mongo db and return it.
    Mars_facts = mongo.db.mars_list.find_one()
    # pass that listing to render_template
    return render_template("index.html", Mars = Mars_facts)

@app.route("/scrape")
def scrape():
    # Run the scrape function
    Mars_dict = scrape_mars.scrape_web()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_list.update({}, Mars_dict, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)