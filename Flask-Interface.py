# This version committed on December 23
from flask import Flask, redirect, url_for, render_template, request, flash
from  Komoot_Ana3 import K_Analize
from FetchTours import API
from datetime import datetime as dt
from pathlib import Path
from Comments import Comments as cm

'''-----Initialization---------'''
app = Flask(__name__)
app.secret_key = "Doron"
komoot_email = ""
komoot_password = ""
stat_data = []

@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
def home():
    global komoot_email
    global komoot_password
    global stat_data
    print(f"the request method is {request.method}")
    display_status="none"
    if request.method == "POST":

        komoot_email = request.form["email"]
        komoot_password = request.form["password"]
        get_list = API()
        approved = get_list.login(komoot_email, komoot_password)

        print(f"approved: {approved}")

        if not approved:
            flash ("Wrong email or password", "info")
            display_status="none"
        else:
            get_list.get_user_tours_list() #save the outvome from the site API to "main.csv"
            display_status = "block"     #change the link to the second page to block(to be shown)

    updated_time = date_of_main()
    return render_template("home.html", display_status=display_status, updated_time=updated_time)


@app.route("/mainstat", methods=["POST", "GET"])
def mainstat():
    global stat_data
    if request.method == "POST":
        week_days_options = request.form.getlist('week_days_options')[0]
        from_when = request.form.getlist('from_when')[0]
        start_date = request.form.getlist('date')[0]
        print(f"status of radio buttons  week days: {week_days_options}")
        print(f"status of radio buttons  from when: {from_when}")
        print(f"status of start date: {start_date}")
        conf = confirm_create([start_date] ,week_days_options, from_when)
        daily = 1 if week_days_options == "daily" else 0
        stat_data = K_Analize(conf)
        updated_time = date_of_main()
        return render_template("main-stat.html", stat_data=stat_data.data, summary=stat_data.summary,
                               updated_time=updated_time, daily=daily)
    else:
        today_gen = dt.now()
        today_str = [f"{today_gen.year}-{today_gen.month}-{today_gen.day}"]
        conf = confirm_create(today_str)
        stat_data = K_Analize(conf)
        daily = 0

    updated_time = date_of_main()
    return render_template("main-stat.html", stat_data=stat_data.data, summary=stat_data.summary,
                           updated_time=updated_time, daily=daily)

@app.route("/comments", methods=["POST", "GET"])
def comments():
    comments_data = cm.show_comments()
    return render_template("comments.html", comments=comments_data)

#--------------this rpocedure convert the radio swiches to a configuration list------------------#
def confirm_create(start_date , week_days_options = 'weekly', from_when = 'from_date' ):
    if start_date == [""]:
        start_date = ['2023-12-10'] # pseudo date just to fill
    else:
        start_date = start_date
    conf_begin = {'weekly' : [1,0], 'daily' : [0,1]}
    conf_end = {'day_one' : [1,0,0], 'year_start' : [0,1,0] , 'from_date' : [0,0,1]}
    conf = start_date + conf_begin[week_days_options] + conf_end[from_when]
    print(conf)
    return conf

#--------------this pocedure get from the OS the last time main.csv was updated------------------#
def date_of_main():
    try:
        file_name = Path("main.csv")
        time = file_name.stat().st_mtime
        t = dt.fromtimestamp(time) #time stamp
        minutes = f"0{t.minute}" if t.minute <10 else t.minute
        return f"{t.day}/{t.month}/{t.year}  {t.hour}:{minutes}"
    except Exception:
        return "main.csv does not exist"


if __name__ == "__main__":
    app.run()
