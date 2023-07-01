from flask import Flask,request,render_template,jsonify
from pymongo import MongoClient

client=MongoClient('127.0.0.1',27017)
db=client['bms']
registercollection=db['registerdata']
donarcollection=db['donors']
reqcollection=db['requirements']

api=Flask(__name__)

@api.route('/register',methods=['get'])
def register():
    Name=request.args.get('Name')
    Email=request.args.get('Email')
    Phone=request.args.get('Phone')
    Gender=request.args.get('Gender')
    BloodType=request.args.get('Bloodtype')
    Password=request.args.get('Password')
    
    data={}
    data['Name']=Name
    data['Email']=Email
    data['Phone']=Phone
    data['Gender']=Gender
    data['BloodType']=BloodType
    data['Password']=Password
    
    query={'Phone':Phone}
    for i in registercollection.find(query):
        return('account exist')
    registercollection.insert_one(data)
    return('data stored')

@api.route('/login',methods=['get'])
def login():
    UserID=request.args.get('UserID')
    Password=request.args.get('Password')
    query={'Phone':UserID}
    for i in registercollection.find(query):
        if (i['Password']==Password):
            return 'True'
    return 'False'
        
@api.route('/applicationform',methods=['get'])
def application_form():
    FullName=request.args.get('FullName')
    Email=request.args.get('Email')
    PhoneNumber=request.args.get('PhoneNumber')
    Age=request.args.get('Age')
    BloodType=request.args.get('BloodType')
    DonationFrequency=request.args.get('DonationFrequency')
    LastDonationDate=request.args.get('LastDonationDate')
    AdditionalComments=request.args.get('AdditionalComments')

    data={}
    data['FullName']=FullName
    data['Email']=Email
    data['PhoneNumber']=PhoneNumber
    data['Age']=Age
    data['BloodType']=BloodType
    data['DonationFrequency']=DonationFrequency
    data['LastDonationDate']=LastDonationDate
    data['AdditionalComments']=AdditionalComments

    query={'PhoneNumber':PhoneNumber}
    for i in donarcollection.find(query):
        return('already registered')
    donarcollection.insert_one(data) 
    return('registered')
  
@api.route('/requirementpage',methods=['get'])
def requirement_page():
    Name=request.args.get('Name')
    Email=request.args.get('Email')
    BloodType=request.args.get('BloodType')
    Quantity=request.args.get('Quantity')
    Urgency=request.args.get('Urgency')
    RequirementDate=request.args.get('RequirementDate')
    AdditionalInformation=request.args.get('AdditionalInformation')

    data={}
    data['Name']=Name
    data['Email']=Email
    data['BloodType']=BloodType
    data['Quantity']=Quantity
    data['Urgency']=Urgency
    data['RequrirementDate']=RequirementDate
    data['AdditionalInformation']=AdditionalInformation
    query={'Email':Email,'RequrirementDate':RequirementDate}
    for i in reqcollection.find(query):
        return('already stored')
    reqcollection.insert_one(data)
    return('data stored')

@api.route('/getdonors')
def get_donors():
    donors=[]
    for i in donarcollection.find():
        dummy=[]
        dummy.append(i['FullName'])
        dummy.append(i['BloodType'])
        dummy.append(i['PhoneNumber'])
        dummy.append(i['Email'])
        donors.append(dummy)
    return jsonify(donors)

@api.route('/getrequests')
def get_requests():
    req=[]
    for i in reqcollection.find():
        dummy=[]
        dummy.append(i['Name'])
        dummy.append(i['Email'])
        dummy.append(i['BloodType'])
        dummy.append(i['Quantity'])
        dummy.append(i['Urgency'])
        dummy.append(i['RequrirementDate'])
        dummy.append(i['AdditionalInformation'])
        req.append(dummy)
    return jsonify(req)

if __name__=="__main__":
    api.run(
        host='0.0.0.0',
        port=2000,
        debug=True
    )