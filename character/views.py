from django.shortcuts import render
import pickle
import numpy as np
import pandas as pd

#Proprocess function
def process(arr):
    res=[]
    for each in arr:
        res.append(each/100)
    res=np.array(res)
    return res

#Load the model
pickle_file = "resources/pickle_model.pkl"
pickle_model = pickle.load(open(pickle_file, 'rb'))

#Load the character file 
data=pd.read_csv('resources/chars.csv')

#Function to return details 
def details(id):
    charid=data.loc[id]['ID']
    work=data.loc[id]['Fictional work']
    dispnm=data.loc[id]['Character display name']
    return charid,work,dispnm

#Base to render home html
def base(request):
    return render(request,"index.html")

#Function to inference predictions
def predictions(request):
    #Extracting data from input fields
    fields=['rg1', 'rg2', 'rg3', 'rg4', 'rg5', 'rg6', 'rg7', 'rg8', 'rg9', 'rg10', 'rg11', 'rg12', 'rg13', 'rg14', 'rg15', 'rg16', 'rg17', 'rg18', 'rg19', 'rg20']
    values=[]
    for each in fields:
        values.append(int(request.POST[each]))
    
    #Preprocessing data for prediction
    values=np.array([values])
    pred=process(values)
    
    #Prediction ID
    id=pickle_model.predict(pred)[0]

    #char id
    charid,work,dispnm=details(id)
    
    #url
    url='https://openpsychometrics.org/tests/characters/test-resources/pics/'+charid+'.jpg'

    return render(request,"disp.html",{'url':url,'work':work,'dispnm':dispnm})
