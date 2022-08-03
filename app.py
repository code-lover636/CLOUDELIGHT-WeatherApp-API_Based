from flask import Flask, render_template, request
from getweather import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "coder636"

@app.route("/",methods =["POST","GET"])
def homePage():
    data = weatherdata(loc="london")  # get weather data
    if request.method == "POST":
        query = request.form.get("city").strip().lower()
        data = weatherdata(loc=query)  
    return render_template("index.html", data=data)
    
if __name__ == "__main__":
    app.run()