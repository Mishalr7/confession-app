from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["confessly"]
collection = db["confessions"]


@app.route("/", methods=["GET", "POST"])
def homepage():

    if request.method == "POST":

        message = request.form.get("message")

        if message and message.strip():

            confession = {
                "message": message.strip(),
                "created_at": datetime.utcnow()
            }

            collection.insert_one(confession)

        return redirect(url_for("show_all_confessions"))

    return render_template("index.html")


@app.route("/confessions")
def show_all_confessions():

    confessions = list(collection.find().sort("created_at", -1))

    return render_template(
        "confessions.html",
        confessions=confessions
    )


if __name__ == "__main__":
    app.run(debug=True)