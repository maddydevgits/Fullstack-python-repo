from flask import Flask,render_template,request,redirect,session
import urllib.request as url
import json

frontend=Flask(__name__)
frontend.secret_key='litam'

@frontend.route('/')
def homepage():
    return render_template('log-sign.html')

@frontend.route('/register')
def register():
    return render_template('signup.html')

@frontend.route('/login')
def login():
    return render_template('signnnn.html')

@frontend.route('/viewproduct')
def viewproduct():
    api='http://127.0.0.1:2000/viewproducts'
    response=url.urlopen(api).read().decode('utf-8')
    response=json.loads(response)
    print(response)
    data=[]
    for i in response:
        dummy=[]
        dummy.append(i['title'])
        dummy.append(i['img'])
        dummy.append(i['sPrice'])
        data.append(dummy)

    return render_template('productview.html',dashboard_data=data,l=len(data))

@frontend.route('/addproduct')
def addproduct():
    return render_template('addpro.html')

@frontend.route('/qrcode')
def qrcode():
    return render_template('qrcode.html')


@frontend.route('/registerform',methods=['post'])
def registerform():
    name=request.form['name']
    Emailid=request.form['Emailid']
    mobile=request.form['phone'] 
    password=request.form['password']
    reenterpassword=request.form['reenterpassword']
    print(name,Emailid,mobile,password,reenterpassword)
    apirequest='http://127.0.0.1:2000/register?name='+name+'&phone='+mobile+'&password='+password+'&Emailid='+Emailid+'&reenterpassword='+reenterpassword
    k=url.urlopen(apirequest).read()
    print(k)
    k=k.decode('utf-8')
    if(k=='account exist'):
        return render_template('signup.html',err='Account Existed')
    return redirect('/login')

@frontend.route('/loginform',methods=['post'])
def loginform():
    Emailid=request.form['username']
    password=request.form['password']
    print(Emailid,password)
    apirequest='http://127.0.0.1:2000/login?username='+Emailid+'&password='+password
    k=url.urlopen(apirequest).read()
    k=k.decode('utf-8')
    if(k=='True'):
        session['username']=Emailid
        return redirect('/viewproduct')
    elif(k=='False'):
        return render_template('signnnn.html',err='Login Invalid')

@frontend.route('/addproductform',methods=['post'])
def addproductForm():
    title=request.form['title']
    img=request.form['img']
    desc=request.form['desc']
    rPrice=request.form['rPrice']
    cate=request.form['cate']
    sPrice=request.form['sPrice']
    apirequest='http://127.0.0.1:2000/addproduct?title='+title+'&img='+img+'&desc='+desc+'&rPrice='+rPrice+'&sPrice='+sPrice+'&cate='+cate
    k=url.urlopen(apirequest).read()
    k=k.decode('utf-8')
    if(k=='Already Added'):
        return render_template('addpro.html',err='Already Added')
    else:
        return render_template('addpro.html',res='Product Added')

@frontend.route('/logout')
def logout():
    session['username']=None
    return redirect('/')

if __name__=="__main__":
    frontend.run(host='0.0.0.0',port=5001, debug=True)