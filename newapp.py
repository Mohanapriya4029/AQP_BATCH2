from joblib import load
from flask import Flask, render_template, request,redirect, url_for, flash,session
import sqlite3



app = Flask(__name__)
app.secret_key = "bkcx nvxdjmxv t6767"

database="new.db"
con = sqlite3.connect(database)
con.execute("create table if not exists register(id integer primary key,name text,mail text,password text)")
con.close()


@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register1', methods=['GET','POST'])
def register1():
     return render_template('register.html')
    
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
            name=request.form['username']
            mail=request.form['usermail']
            password=request.form['password']
            con=sqlite3.connect(database)
            cur=con.cursor()
            cur.execute("insert into register(name,mail,password)values(?,?,?)",(name,mail,password))
            con.commit()
            flash("Record Added Successfully","success")
            return render_template('register.html')
    return render_template('register.html')



@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
            mail=request.form['usermail']
            password=request.form['password']
            con=sqlite3.connect(database)
            cur=con.cursor()
            cur.execute("select *from  register where mail=? and password=?",( mail,password))
            con.commit()
            flash("Record Added Successfully","success")
            return render_template('upload..html')
    return render_template('register.html')

@app.route('/upload1', methods=['GET','POST'])
def upload1():
     return render_template('upload..html')

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method=='POST':
             city=int(request.form['city'])
             date = request.form['date']
             year, month, day = map(int, date.split('-'))
             model = load("extra_trees_model.joblib")
             EXTRA_TREES = model.predict([[city,day,month,year]])
             prediction=EXTRA_TREES[0]
    
             if prediction<200 :
                 aqi="Moderate"
                 aqi_class = "moderate"
             elif prediction<300 and prediction>200:
                aqi="Poor"
                aqi_class = "poor"
             elif prediction<400 and prediction>300:
                aqi="Very Poor"
                aqi_class = "very-poor"
             elif prediction>400:
                aqi="Severe"
                aqi_class = "severe"
             return render_template('result.html',prediction=prediction,aqi=aqi,aqi_class=aqi_class)


if __name__ == '__main__':
    app.run(debug=False, port=500)
