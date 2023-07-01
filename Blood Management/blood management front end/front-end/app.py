from flask import Flask,render_template,redirect,request,session
import urllib3
import json

backendserver='http://127.0.0.1:2000'

frontend=Flask(__name__)
frontend.secret_key='litam'

@frontend.route('/')
def homePage():
    return render_template('home.html')

@frontend.route('/signup')
def signupPage():
    return render_template('signup.html')

@frontend.route('/signupform',methods=['post'])
def signupform():
    name=request.form['name']
    email=request.form['email']
    phone=request.form['phone']
    gender=request.form['gender']
    bloodtype=request.form['bloodtype']
    password=request.form['password']
    print(name,email,phone,gender,bloodtype,password)
    apirequest=backendserver+'/register?Name='+name+'&Email='+email+'&Phone='+phone+'&Gender='+gender+'&Bloodtype='+bloodtype+'&Password='+password
    http=urllib3.PoolManager()
    response=http.request('get',apirequest)
    response=response.data.decode('utf-8')
    print(response)
    if response=='account exist':
        return render_template('signup.html',err='account already exist')
    return render_template('signup.html',res='Registered')

@frontend.route('/login')
def loginPage():
    return render_template('login.html')

@frontend.route('/loginform',methods=['post'])
def loginform():
    userid=request.form['userid']
    password=request.form['password']
    print(userid,password)
    apirequest=backendserver+'/login?UserID='+userid+'&Password='+password
    http=urllib3.PoolManager()
    response=http.request('get',apirequest)
    response=response.data.decode('utf-8')
    print(response)
    if(response=='True'):
        session['username']=userid
        return redirect('/dashboard')
        # return render_template('login.html',res='Login Valid')
    else:
        return render_template('login.html',err='Login Invalid')

@frontend.route('/dashboard')
def dashboardPage():
    return render_template('application.html')

@frontend.route('/logout')
def logoutpage():
    session['username']=None
    return redirect('/')

@frontend.route('/applicationform',methods=['post'])
def applicationform():
    name=request.form['name']
    email=request.form['email']
    phone=request.form['phone']
    age=request.form['age']
    bloodtype=request.form['bloodtype']
    donationFrequency=request.form['donationFrequency']
    date=request.form['date']
    additionalcomments=request.form['additionalcomments']
    print(name,email,phone,age,bloodtype,donationFrequency,date,additionalcomments)
    apirequest=backendserver+'/applicationform?FullName='+name+'&Email='+email+'&PhoneNumber='+phone+'&Age='+age+'&BloodType='+bloodtype+'&DonationFrequency='+donationFrequency+'&LastDonationDate='+date+'&AdditionalComments='+additionalcomments
    http=urllib3.PoolManager()
    response=http.request('get',apirequest)
    response=response.data.decode('utf-8')
    print(response)
    if response=="already registered":
        return render_template('application.html',err="You are already registered")
    else:
        return render_template('application.html',res='Registered Successfully')

@frontend.route('/donors')
def donors():
    apirequest=backendserver+'/getdonors'
    http=urllib3.PoolManager()
    response=http.request('get',apirequest)
    response=response.data.decode('utf-8')
    response=json.loads(response)
    print(response)
    return render_template('donor.html',dashboard_data=response,l=len(response))

@frontend.route('/announcements')
def announcements():
    return render_template('announcements.html')

@frontend.route('/announcementsform',methods=['post'])
def announcementsform():
    name=request.form['name']
    email=request.form['email']
    bloodtype=request.form['bloodtype']
    quantity=request.form['quantity']
    urgency=request.form['urgency']
    date=request.form['date']
    message=request.form['message']
    print(name,email,bloodtype,quantity,urgency,date,message)
    apirequest=backendserver+'/requirementpage?Name='+name+'&Email='+email+'&BloodType='+bloodtype+'&Quantity='+quantity+'&Urgency='+urgency+'&RequirementDate='+date+'&AdditionalInformation='+message
    http=urllib3.PoolManager()
    response=http.request('get',apirequest)
    response=response.data.decode('utf-8')
    if response=='already stored':
        return render_template('announcements.html',err='announcement already added')
    else:
        return render_template('announcements.html',res='announcement added')

@frontend.route('/requests')
def requests():
    apirequest=backendserver+'/getrequests'
    http=urllib3.PoolManager()
    response=http.request('get',apirequest)
    response=response.data.decode('utf-8')
    response=json.loads(response)
    print(response)
    return render_template('requests.html',dashboard_data=response,l=len(response))


if __name__=="__main__":
    frontend.run(host='0.0.0.0',port=5001,debug=True)