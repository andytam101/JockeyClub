from flask import Flask, render_template, request, jsonify, redirect
from datetime import datetime
from compete import scrape_compete
from store import scrape_all_on_date, add_all_data
from edit import *


app = Flask(__name__)


@app.route("/")
def index():
    return redirect("/compete")


@app.route("/compete", methods=["POST", "GET"])
def compete():
    if request.method == "POST":
        result = {"status": "success"}
        url = request.json["url"].strip()

        try:
            result.update(scrape_compete(url))
        except Exception as e:
            print(e)
            result["status"] = "failed"

        return jsonify(result)

    else:
        return render_template("compete.html")


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        try:
            date = request.form["date"]
            selected_date = datetime.strptime(date, '%Y-%m-%d')
            formatted_date = selected_date.strftime('%Y/%m/%d')
            location = request.form["location"]
            total_count = int(request.form["count"])

            results = scrape_all_on_date(formatted_date, location, total_count)
            add_all_data(results)

            return jsonify({
                "status": "success"
            })

        except Exception as e:
            return jsonify({
                "status": "fail",
                "message": str(e)
            })

    else:
        return render_template("add.html")


@app.route("/edit", methods=["POST", "GET"])
def edit():
    if request.method == "POST":
        try:
            raceId = int(request.form["raceId"])
            fairness = request.form["fairness"]
            high_quality = "highQuality" in request.form

            if not set_high_quality(raceId, high_quality):
                raise Exception("Failed")
            if not set_fair(raceId, fairness):
                raise Exception("Failed")

            return jsonify({"status": "success"})
        except Exception as e:
            print(e)
            return jsonify({"status": "fail", "message": str(e)})
    else:
        return render_template("edit.html")


if __name__ == "__main__":
    app.run(debug=True)
