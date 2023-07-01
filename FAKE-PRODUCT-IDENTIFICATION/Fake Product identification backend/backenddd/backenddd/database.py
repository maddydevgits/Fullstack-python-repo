# Launch API Server
# create a login API to validate login
from flask import Flask,request,jsonify
from pymongo import MongoClient
from flask_cors import CORS

client=MongoClient('127.0.0.1',27017)
db=client['project'] # register database is created here
collection=db['frontend']# Create collection
productcollection=db['products']


# Flask - class

# flask - Library

# Create an object

api=Flask(__name__)
cors = CORS(api)

# Create Register API to store data in mongoDB

#Nmae,EmailID,Mobile,Password
@api.route('/register',methods=['get'])
def register():
    name=request.args.get('name')
    Emailid=request.args.get('Emailid')
    mobile=request.args.get('phone')
    password=request.args.get('password')
    reenterpassword=request.args.get('reenterpassword')
    k={} #Creating a dictionary
    k['name']=name
    k['Emailid']=Emailid
    k['mobile']=mobile
    k['password']=password
    k['reenterpassword']=reenterpassword
    query={'mobile':mobile}
    for i in collection.find(query):
        return ('account exist')
    collection.insert_one(k)
    return('data stored')

@api.route('/login',methods=['get'])
def login():
    username=request.args.get('username')
    password=request.args.get('password')
    query={'Emailid':username}
    for i in collection.find(query):
        if(i['password']==password):
            return 'True'
    return 'False'

@api.route('/addproduct',methods=['get'])
def addproduct():
    title=request.args.get('title')
    img=request.args.get('img')
    desc=request.args.get('desc')
    cate=request.args.get('cate')
    rPrice=request.args.get('rPrice')
    sPrice=request.args.get('sPrice')
    k={}
    k['title']=title
    k['img']=img
    k['desc']=desc
    k['rPrice']=rPrice
    k['sPrice']=sPrice

    query=k
    for i in productcollection.find(k):
        return 'Already Added'

    productcollection.insert_one(query)
    return 'Product Added'

@api.route('/viewproducts',methods=['get'])
def viewproducts():
    data=[]
    for i in productcollection.find():
        dummy={}
        dummy['title']=i['title']
        dummy['img']=i['img']
        dummy['sPrice']=i['sPrice']
        data.append(dummy)
    
    return jsonify(data)

@api.route('/fakeverification',methods=['get'])
def fakeverification():
    id=request.args.get('id')
    query={'rPrice':id}
    for i in productcollection.find(query):
        return 'original product'
    return 'fake product'

if __name__ == "__main__":
    api.run(
        host='0.0.0.0',
        port=2000,
        debug=True
    )