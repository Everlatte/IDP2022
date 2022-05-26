# -*- coding: utf-8 -*-
"""
Created on Sun May  8 11:16:28 2022

@author: Everlatte
"""

from flask import Flask, redirect, url_for, render_template
from datetime import datetime
import pyodbc
from chart_studio.plotly import plot, iplot
import plotly.graph_objs as go
import matplotlib.pyplot as plt

app = Flask(__name__)
server = '127.0.0.1,1433' 
database = 'Testing 1' 
username = 'iot1' 
password = 'iot1' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute("SELECT [DataValue], [DateTime] FROM [Testing 1].[dbo].[Data_Backup_them1:NewTag] WHERE [ID] BETWEEN 0 AND 10000 AND ([ID]%60 = 0)")
row = cursor.fetchone()
data_temp = []
data_datetime = []
while row: 
    data_temp.append(row[0])
    data_datetime.append(row[1])
    row = cursor.fetchone()
    
def plot():
    data_plot = go.Scatter(x=data_datetime, y=data_temp, line=dict(width=2,color='blue',dash='solid'),name='Temperature (Celcius)')
#    data_plot_url = py.plot(data_plot, filename='Temperature', auto_open=False,)
    fig = go.Figure(data_plot)
    fig.show()
    data_plot_url = 'temp_plot.png'
    fig.savefig(data_plot_url)
    return data_plot_url

@app.route("/")
def home():
    return render_template("index.html", username="Everlatte", email="everlatte@1utar.my")

@app.route("/temp")
def temp():
    temp_plot = plot()
    return render_template("temp.html", username="Everlatte", email="everlatte@1utar.my", temp=data_temp, dt=data_datetime, length=len(data_temp), temp_url=temp_plot)

if __name__ == "__main__":
    app.run(debug=True)
