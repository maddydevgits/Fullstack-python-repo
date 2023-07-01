from flask import Flask,render_template,request,redirect,session
from pymongo import MongoClient
client=MongoClient('127.0.0.1',27017)
db= client ['himanshu']
c=db['flaskapp']
app=Flask(__name__)
app.secret_key='himanshu'
#Home Handler-register page
@app.route('/')
def homePage():
    return render_template('index.html')
#Login Handler-Login page
@app.route('/login')
def loginpage():
    return render_template('login.html')
#Dashboard Handler
@app.route('/dashboard')
def dashboardPage():
    owner=session['username']
    return render_template('dashboard.html',owner=owner)
#Insert notes handler
@app.route('/insertnotes')
def insertnotesPage():
    return render_template('insertnotes.html')
#View notes handler
@app.route('/viewnotes')
def viewnotes():
    #reading data
    c1=db['notes']
    data=[]
    for i in c1.find():
        if i['owner']==session['username']: #to display only owner notes
            data.append(i['notes'])
    return render_template('viewnotes.html',data=data,l=len(data))
#Form Handler-to collect data from HTML
@app.route('/formdata',methods =['POST'])
def formdata():
    name=request.form['name'] 
    email=request.form['email'] 
    Mobile=request.form['Mobile'] 
    password=request.form['password'] 
    print (name,email,Mobile,password)
    for i in c.find():
        if i ['Mobile']== Mobile:
            return render_template('index.html',err='Phone already exists')
    k={}
    k['name']=name
    k['email']=email
    k['Mobile']=Mobile
    k['password']=password
    c.insert_one(k)
    return render_template('index.html',res='Registered Successfully')
#LoginForm Handler-Check credentials
@app.route('/logindata',methods=['post'])
def logindata():
    Mobile=request.form['Mobile']
    password=request.form['password']
    print(Mobile,password)
    for i in c.find():
        if i['Mobile']==Mobile and i['password']==password:
            session['username']=Mobile #Storing the session
            return redirect('/dashboard') #Dashboard page 
            #return render_template('login.html',res1='Valid Credentials')
    return render_template('login.html',err1='Invalid Credentials')

@app.route('/logout')
def logout():
    session['username']=None #Destroy Session
    return redirect('/') #Home page

@app.route('/insertnotesdata',methods=['post'])
def inerternotesdata():
    notes=request.form['notes']
    owner=session['username']
    print(notes, owner)
    c1=db['notes']
    k={}
    k['owner']=owner
    k['notes']=notes
    c1.insert_one(k) #inserting notes and owner details
    return render_template('insertnotes.html',res2='Notes Saved')

if __name__=="__main__":
    app.run(host='0.0.0.0',port=5001,debug=True)