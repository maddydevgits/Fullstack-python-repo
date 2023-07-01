from flask import Flask,render_template,redirect,request,session
import urllib3
import json

backendServer='http://127.0.0.1:2000'
registerapi='/register'
loginapi='/login'
chatapi='/chat'

frontend=Flask(__name__)
frontend.secret_key='litam'

@frontend.route('/')
def homePage():
    return render_template('register.html')

@frontend.route('/register')
def registerPage():
    return render_template('register.html')

@frontend.route('/login')
def loginPage():
    return render_template('login.html')

@frontend.route('/dashboard')
def dashboardPage():
    return render_template('chatbot.html')

@frontend.route('/registerForm',methods=['post','get'])
def registerForm():
    name=request.form['name']
    mobile=request.form['mobile']
    password=request.form['password']
    emailid=request.form['emailid']
    print(name,mobile,password,emailid)
    api=backendServer+registerapi+'?'+'name='+name+'&mobile='+mobile+'&password='+password+'&emailid='+emailid
    http=urllib3.PoolManager()
    response=http.request('get',api)
    response=response.data
    response=response.decode('utf-8')
    if(response=='account exist'):
        return render_template('register.html',err=response)
    else:
        return render_template('register.html',res='Account Created Successfully')

@frontend.route('/loginForm',methods=['get','post'])
def loginForm():
    username=request.form['username']
    password=request.form['password']
    print(username,password)
    api=backendServer+loginapi+'?'+'username='+username+'&password='+password
    http=urllib3.PoolManager()
    response=http.request('get',api)
    response=response.data
    response=response.decode('utf-8')
    if(response=='True'):
        session['username']=username
        return redirect('/dashboard')
    else:
        return render_template('login.html',err='Invalid Login')

@frontend.route('/chatForm',methods=['get','post'])
def chatForm():
    message=request.form['message']
    print(message)
    api=backendServer+chatapi+'?message='+message
    http=urllib3.PoolManager()
    response=http.request('get',api)
    print(response.data)
    response=response.data
    response=response.decode('utf-8')
    response=json.loads(response)
    answer=response['message']

    return render_template('chatbot.html',res=answer)

if __name__=="__main__":
    frontend.run('0.0.0.0',port=5001,debug=True)