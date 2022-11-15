# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 16:39:56 2020
@author: hp
"""

import email
from logging import root
# from datatable import count
from flask import Flask, render_template, request
from numpy import double
import key_details as keys
import boto3 
import pickle
import numpy as np
import pandas as pd
import tkinter as tk
import requests
#import Tkinter as tk
window = tk.Tk()

model=pickle.load(open('new_prediction_1.pkl','rb'))
modelRattle=pickle.load(open('kmeansRattle.pkl','rb'))
modelArmwrap=pickle.load(open('kmeansArmwrap.pkl','rb'))
app = Flask(__name__)


dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                    region_name='ap-south-1')

from boto3.dynamodb.conditions import Key, Attr

@app.route('/')
def Doc_login():
    return render_template('Doc_login.html')

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['post'])
def signup():
    if request.method == 'POST':
        childID = request.form['childID']
        Age = request.form['Age']
        child_Name = request.form['child_Name']
        Gender = request.form['Gender']
        BirthDate = request.form['BirthDate']
        Gurdian_Address = request.form['Gurdian_Address']
        Gurdian_Contact = request.form['Gurdian_Contact']
        Gurdian_Name = request.form['Gurdian_Name']

        table = dynamodb.Table('child_details')
        
        table.put_item(
                Item={
        'childID': childID,
        'Age': Age,
        'child_Name':child_Name,
        'Gender':Gender,
        'BirthDate':BirthDate,
        'Gurdian_Address': Gurdian_Address,
        'Gurdian_Contact':Gurdian_Contact,
        'Gurdian_Name':Gurdian_Name,
            }
        )
        msg = "Registration Complete. Please Login to your account !"
    
        return render_template('home.html')
    return render_template('index.html')



@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/view')
def view():
        table = dynamodb.Table('IOT_feeding_spoon_marker')
        
        response=table.scan()
        data = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])

        return render_template('view.html',response = data)  


@app.route('/view_ones')
def view_one():

        table = dynamodb.Table('userdata')
        
        response = table.get_item(TableName='userdata', Key={'email':email})

        data= response["Item"]
        #print(response["Item"])
        return render_template('view_one.html',response = data)

@app.route('/searching',methods = ['post'])
def searching():
    if request.method=='POST':
        
        

        cid = request.form['cid']
        #password = request.form['password']
        
        table = dynamodb.Table('IOT_feeding_spoon_marker')
        table1 = dynamodb.Table('child_details')

        response = table.query(
                KeyConditionExpression=Key('cid').eq(cid)
        )

        response1 = table1.query(
                KeyConditionExpression=Key('childID').eq(cid)
        )
        
        items = response['Items']
        cid = items[0]['cid'] 
        acx = items[0]['acx']
        acy = items[0]['acy']
        acz = items[0]['acz']
        gyx = items[0]['gyx']
        gyY = items[0]['gyY']
        gyz = items[0]['gyz']
        #print(items[0]['email'])

        items1 = response1['Items']
        child_Name = items1[0]['child_Name'] 
        Gender = items1[0]['Gender']
        Gurdian_Name = items1[0]['Gurdian_Name']
        Gurdian_Contact = items1[0]['Gurdian_Contact']
        
        arr=np.array([[acx,acy,acz,gyx,gyY,gyz]])
        pred1=model.predict(arr)

        if cid == items[0]['cid']:
        

            return render_template("view_one.html",items=items,pred1=pred1,child_Name=child_Name,Gender=Gender,Gurdian_Name=Gurdian_Name,Gurdian_Contact=Gurdian_Contact)
    return render_template("search_data.html")

@app.route('/search_Rattle', methods = ['GET', 'POST'])
def search_Rattle():
    if request.method=='POST':
        cid = request.form['cid']
        #password = request.form['password']
        
        table = dynamodb.Table('rattle2_table')

        response = table.query(
                KeyConditionExpression=Key('cid').eq(cid)
        )
        
        items = response['Items']
        cid = items[0]['cid'] 
        acx = items[0]['acx']
        acy = items[0]['acy']
        acz = items[0]['acz']
        gyx = items[0]['gyx']
        gyY = items[0]['gyY']
        gyz = items[0]['gyz']
        #print(items[0]['email'])
        
        arr=np.array([[acx,acy,acz,gyx,gyY,gyz]])
        pred=modelRattle.predict(arr)

        if cid == items[0]['cid']:
            return render_template("view_rattle1.html",items=items,pred=pred)
    return render_template("search_rattle_data.html")

@app.route('/search_Arm', methods = ['GET', 'POST'])
def search_Arm():
    if request.method=='POST':
        cid = request.form['cid']
        #password = request.form['password']
        
        table = dynamodb.Table('iot_armwrap')

        response = table.query(
                KeyConditionExpression=Key('cid').eq(cid)
        )
        
        items = response['Items']
        cid = items[0]['cid'] 
        acx = items[0]['acx']
        acy = items[0]['acy']
        acz = items[0]['acz']
        gyx = items[0]['gyx']
        gyY = items[0]['gyY']
        gyz = items[0]['gyz']
        #print(items[0]['email'])
        
        arr=np.array([[acx,acy,acz,gyx,gyY,gyz]])
        pred=modelArmwrap.predict(arr)

        if cid == items[0]['cid']:
            return render_template("view_ArmWrap.html",items=items,pred=pred)
    return render_template("search_Armwrap_data.html")



# @app.route('/search_ban',methods = ['post'])
# def search_ban():
#     if request.method=='POST':
        
        

#         cid = request.form['cid']
#         #password = request.form['password']
        
#         table = dynamodb.Table('iot_bangle')

#         response = table.query(
#                 KeyConditionExpression=Key('cid').eq(cid)
#         )
        
#         items = response['Items']
#         cid = items[0]['cid'] 
#         acx = items[0]['acx']
#         acy = items[0]['acy']
#         acz = items[0]['acz']
#         gyx = items[0]['gyx']
#         gyY = items[0]['gyY']
#         gyz = items[0]['gyz']
#         #print(items[0]['email'])
        
#         arr=np.array([[acx,acy,acz,gyx,gyY,gyz]])
#         #pred=bangle_model.predict(arr)

#         if cid == items[0]['cid']:
        

#             return render_template("view_one.html",items=items,pred=pred)
#     return render_template("Bangle_ArmwrUser.html")



@app.route('/view_all_children')
def view_all_children():

        table = dynamodb.Table('child_details')
        
        response=table.scan()
        data = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
  
        return render_template('view_all_children.html',response = data)


@app.route('/search_data')
def search_data():    
    return render_template('search_data.html')
@app.route('/search_car')
def search_car():    
    return render_template('CarUserSearch.html')
@app.route('/search_bangle_armwrap')
def search_bangle_armwrap():    
    return render_template('search_Armwrap_data.html')
@app.route('/visualization')
def visualization():    
    return render_template('visualization.html')

@app.route('/marker_page',methods = ['post'])
def marker_page():    
    return render_template('marker_page.html')

@app.route('/spoon_page',methods=['post'])
def spoon_page():    
    return render_template('spoon_page.html')

@app.route('/bangle',methods=['post'])
def bangle():    
    return render_template('bangle_page.html')

@app.route('/armwrap',methods=['post'])
def armwrap():    
    return render_template('armwrap_page.html')

@app.route('/letter_ta',methods = ['post'])
def letter_ta():
    import pandas as pd
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as plt


    # Make a list of columns
    columns = ['Typical c1','Typical c2','Typical c3','Typical c4','Atypical c1','Atypical c2']


    # Read a CSV file

    df2 = pd.read_csv("gyY_2_2.csv", usecols=columns)

    # Plot the lines

    df2.plot()

    plt.title('Letter ta Writing')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.ylabel('Angular Velocity (rad/s)')
    plt.xlabel('time in seconds')
    plt.show()



    return render_template('marker_page.html')

@app.route('/letter_la',methods = ['post'])
def letter_la():
    import pandas as pd
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as plt


    # Make a list of columns
    columns = ['Typical c1','Typical c2','Typical c3','Typical c4','Atypical c1','Atypical c2']


    # Read a CSV file

    df2 = pd.read_csv("gyY_4_4.csv", usecols=columns)

    # Plot the lines

    df2.plot()

    plt.title('Letter la Writing')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.ylabel('Angular Velocity (rad/s)')
    plt.xlabel('time in seconds')
    plt.show()



    return render_template('marker_page.html')

@app.route('/letter_ra',methods = ['post'])
def letter_ra():
    import pandas as pd
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as plt


    # Make a list of columns
    columns = ['Typical c1','Typical c2','Typical c3','Typical c4','Atypical c1','Atypical c2']


    # Read a CSV file

    df2 = pd.read_csv("gyY_6_6.csv", usecols=columns)

    # Plot the lines

    df2.plot()

    plt.title('Letter ra Writing')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.ylabel('Angular Velocity (rad/s)')
    plt.xlabel('time in seconds')
    plt.show()



    return render_template('marker_page.html')

@app.route('/boxplot_sin',methods = ['post'])
def boxplot_sin():
# importing the required module
    from PIL import Image
    #read the image, creating an object
    im = Image.open(r"C:\Users\DELL\github_repo\Research_frontend\content\nm.png")
    #show picture
    im.show()



    return render_template('marker_page.html')

@app.route('/letter_A',methods = ['post'])
def letter_A():
    import pandas as pd
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as plt


    # Make a list of columns
    columns = ['Typical c1','Typical c2','Typical c3','Typical c4','Atypical c1','Atypical c2']


    # Read a CSV file

    df2 = pd.read_csv("gyY_7_7.csv", usecols=columns)

    # Plot the lines

    df2.plot()

    plt.title('Letter A Writing')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.ylabel('Angular Velocity (rad/s)')
    plt.xlabel('time in seconds')
    plt.show()



    return render_template('marker_page.html')


@app.route('/letter_E',methods = ['post'])
def letter_E():
    import pandas as pd
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as plt


    # Make a list of columns
    columns = ['Typical c1','Typical c2','Typical c3','Typical c4','Atypical c1','Atypical c2']


    # Read a CSV file

    df2 = pd.read_csv("gyY_5_5.csv", usecols=columns)

    # Plot the lines

    df2.plot()

    plt.title('Letter E Writing')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.ylabel('Angular Velocity (rad/s)')
    plt.xlabel('time in seconds')
    plt.show()



    return render_template('marker_page.html')

@app.route('/letter_F',methods = ['post'])
def letter_F():
    import pandas as pd
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as plt


    # Make a list of columns
    columns = ['Typical c1','Typical c2','Typical c3','Typical c4','Atypical c1','Atypical c2']


    # Read a CSV file

    df2 = pd.read_csv("gyY_3_3.csv", usecols=columns)

    # Plot the lines

    df2.plot()

    plt.title('Letter F Writing')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.ylabel('Angular Velocity (rad/s)')
    plt.xlabel('time in seconds')
    plt.show()



    return render_template('marker_page.html')

@app.route('/boxplot_eng',methods = ['post'])
def boxplot_eng():
# importing the required module
    from PIL import Image
    #read the image, creating an object
    im = Image.open(r"C:\Users\DELL\github_repo\Research_frontend\content\nm1.png")
    #show picture
    im.show()



    return render_template('marker_page.html')

@app.route('/spoon_violin',methods = ['post'])
def spoon_violin():
    from PIL import Image
    #read the image, creating an object
    im = Image.open(r"C:\Users\DELL\github_repo\Research_frontend\content\nm3.png")
    #show picture
    im.show()

    return render_template('spoon_page.html')


@app.route('/spoon_strip',methods = ['post'])
def spoon_strip():
    from PIL import Image
    #read the image, creating an object
    im = Image.open(r"C:\Users\DELL\github_repo\Research_frontend\content\nm2.png")
    #show picture
    im.show()

    return render_template('spoon_page.html')


@app.route('/boxplot_bangle',methods = ['post'])
def boxplot_bangle():
# importing the required module
    from PIL import Image
    #read the image, creating an object
    im = Image.open(r"C:\Users\DELL\github_repo\Research_frontend\content\boxplotban.png")
    #show picture
    im.show()

    return render_template('bangle_armwrap_page.html')

@app.route('/boxplot_armwrap',methods = ['post'])
def boxplot_armwrap():
# importing the required module
    from PIL import Image
    #read the image, creating an object
    im = Image.open(r"C:\Users\DELL\github_repo\Research_frontend\content\boxplotarm.png")
    #show picture
    im.show()

    return render_template('bangle_armwrap_page.html')

@app.route('/signup_doc', methods=['post'])
def signup_doc():
    if request.method == 'POST':
        Emp_no = request.form['Emp_no']
        Name = request.form['Name']
        email = request.form['email']
        Specialization = request.form['Specialization']
        contact_no = request.form['contact_no']
        Address = request.form['Address']
      

        table = dynamodb.Table('Doc_details')
        
        table.put_item(
                Item={
        'Emp_no': Emp_no,
        'Name': Name,
        'email':email,
        'Specialization':Specialization,
        'contact_no': contact_no,
        'Address':Address,
        
            }
        )
        msg = "Registration Complete. Please Login to your account !"
    
        return render_template('Doc_login.html',msg = msg)
    return render_template('signup_doc.html')

 


@app.route('/check_docs',methods = ['post'])
def check_doc():
    if request.method=='POST':
        
        Emp_no = request.form['Emp_no']
        email = request.form['email']
        
        table = dynamodb.Table('Doc_details')
        response = table.query(
                KeyConditionExpression=Key('Emp_no').eq(Emp_no)
        )
        items = response['Items']
        Name = items[0]['Name']
        print(items[0]['Emp_no'])
        if Emp_no == items[0]['Emp_no']:
            return render_template("home.html",Name=Name)
    return render_template("Doc_login.html")

@app.route('/Doc_signup')
def Doc_signup():
    return render_template('Doc_signup.html')

@app.route('/Doc_All')
def Doc_All():    

        table = dynamodb.Table('Doc_details')
        
        response=table.scan()
        data = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
       
        return render_template('Doc_All.html',response = data)







def PassValuePredictor1(id):
        url = 'https://0d8p49x2jb.execute-api.ap-south-1.amazonaws.com/ch/carforward'
        url2 = 'https://0d8p49x2jb.execute-api.ap-south-1.amazonaws.com/ch/carbackwardall'

        r = requests.get(url)
        r2 = requests.get(url2)
        json = r.json()
        json2 = r2.json()
        dataframe = pd.DataFrame.from_dict(json, orient="columns")
        dataframe=dataframe.loc[dataframe.Activity=='Forward',:]
        dataframe=dataframe.loc[dataframe.cid==id,:]

        dataframe2 = pd.DataFrame.from_dict(json2, orient="columns")
        dataframe2=dataframe2.loc[dataframe2.Activity=='Forward',:]
        dataframe2=dataframe2.loc[dataframe2.cid==id,:]
        # max  
        df1=dataframe.groupby('cid')[['nRotations1', 'nRotations2']].max()
        # max  
        df2=dataframe2.groupby('cid')[['nRotations3', 'nRotations4']].max()
        x = pd.concat([df1, df2], axis=1, join='outer')

        list=x.values.tolist()
        ro1=list[0][0]
        ro2=list[0][1]
        ro3=list[0][2]
        ro4=list[0][3]
        list2=[ro1,ro2,ro3,ro4]
 

        to_predict = np.array(list2).reshape(1,4)
        loaded_model = pickle.load(open("modelD.pkl","rb"))
        result = loaded_model.predict(to_predict)
        return result[0] 

        
def OneChildCar(id):
        cid = request.form['id']
        #password = request.form['password']
        
        table = dynamodb.Table('iotCar_frontWheels')

        response = table.query(
                KeyConditionExpression=Key('cid').eq(cid)
        )
        items = response['Items']
        nRotations1 = items[0]['nRotations1']
        nRotations2 = items[0]['nRotations2']
        MilliSeconds = items[0]['MilliSeconds']

        return items
          
@app.route('/CarUser',methods = ['POST'])
def resultCar():


    if request.method == 'POST':
        id = request.form.get("id")
        
        result = PassValuePredictor1(id)
        
        if float(result) == 1:
            prediction='Model Suggested Child as a Typical Child'
        elif float(result) == 0:
            prediction='Model Suggested Child as an atypicl child.It is suggested to have further medical instructions'
        else:
            prediction="no results"
        items = OneChildCar(id)     
        return render_template("resultCar.html",prediction=prediction,id=id,items=items)
 


if __name__ == "__main__":
    
    app.run(debug=True)
    
