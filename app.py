from flask import Flask,render_template,redirect,request,flash,url_for,Blueprint
import pandas as pd
import numpy as np
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import  os
from flask_sqlalchemy import SQLAlchemy
from io import TextIOWrapper
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, Date, String, VARCHAR
from flask_paginate import Pagination,get_page_parameter
import csv
from flask_bootstrap import Bootstrap
from os import environ
from sqlalchemy import MetaData
from sqlalchemy.orm import mapper
from sqlalchemy import create_engine,inspect
import tensorflow as tf
from keras.models import model_from_json
from keras.models import load_model
import numpy as np
mod = Blueprint('users',__name__)
app = Flask(__name__)
app.config['SECRET_KEY'] = '^%huYtFd90;90jjj'
app.config['UPLOADED_FILES'] = 'static'
engine = create_engine('sqlite:///test.db',echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base=declarative_base()
Base.metadata.create_all(engine)
inspector = inspect(engine)
Bootstrap(app)





# Define structure of table
class dataset(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__ = 'dataset'
    __table_args__ = {'sqlite_autoincrement': True}
    #tell SQLAlchemy the name of column and its attributes:
    id = Column(Integer, primary_key=True, nullable=False)
    Bench = Column(Integer)
    diameter = Column(Integer)
    Burden = Column(Integer)
    Spacing = Column(Integer)
    subdrill = Column(Integer)
    charge = Column(Integer)
    stemm= Column(Integer)
    pf= Column(Integer)
    delayt= Column(Integer)
    ucs= Column(Integer)
    vibrations= Column(Integer)


colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        csv = request.files['csv']
        filename = secure_filename(csv.filename)
        csv.save(os.path.join(app.config['UPLOADED_FILES'], filename))
        ext = csv.filename.split('.')[1]
        try:
            if ext == 'xlsx':
                data =pd.read_excel(csv)
                data.to_sql(con=engine, index_label='id', name=dataset.__tablename__, if_exists='replace')
                return redirect(url_for('index'))
            elif ext == 'csv':
                data = pd.read_csv(csv)
                data.to_sql(con=engine, index_label='id', name=dataset.__tablename__, if_exists='replace')
                return redirect(url_for('index'))
            else:
                print("Unknown file format")
        except:
            print("Unknown File format")
    return render_template('index.html')
@app.route('/')
def index():
    df = pd.read_sql('SELECT * FROM dataset', engine)
    index = df.index
    number_of_rows = len(index)
    columns = df.columns
    colmns = len(columns)
    return render_template('index.html',number_of_rows=number_of_rows,colmns=colmns)
@app.route('/charts')
def charts():
    df = pd.read_sql('SELECT * FROM dataset', engine)
    index = df.index
    number_of_rows = len(index)
    columns = df.columns.values
    sum_column = df.sum(axis=0)
    labels = columns
    values = sum_column.values
    bar_labels = labels
    bar_values = values
    line_labels = labels
    line_values = values
    pie_labels = labels
    pie_values = values
    return  render_template('charts.html',title='Dataset Distribution', max=10000, labels=bar_labels, values=bar_values,labels_=line_labels, values_=line_values,set=zip(pie_values,pie_labels, colors))

@app.route('/tables')
def tables():
    df = pd.read_sql('SELECT * FROM dataset',engine)
    index = df.index
    number_of_rows = len(index)
    columns =df.columns.values

    return render_template('tables.html',df=list(df.values.tolist()),column_names=columns,zip=zip)

@app.route('/predict')

def predict():
    
    return render_template('register.html')
@app.route('/submit_args',methods=["POST","GET"])
def submit_args():
    input_=[]
    if request.method=="POST":
        bench = request.form["Bench"]
        input_.append(float(bench))
        h_diameter=request.form['h_diameter']
        input_.append(float(h_diameter))
        burden=request.form['burden']
        input_.append(float(burden))
        spacing=request.form['spacing']
        input_.append(float(spacing))
        Charge=request.form['Charge']
        input_.append(float(Charge))
        subdrill=request.form['subdrill']
        input_.append(float(subdrill))
        stemm=request.form['stemm']
        input_.append(float(stemm))
        pf=request.form['pf']
        input_.append(float(pf))
        delay=request.form['delay']
        input_.append(float(delay))
        ucs=request.form['ucs']
        input_.append(float(ucs))
        value_=np.array([input_])
        loaded_model=load_model('vibration.hdf5')
        result=loaded_model.predict(value_)
        return render_template('result.html',result=result)
@app.route('/description')
def description():
    return  render_template('ann_file.html')
if __name__ == '__main__':
    app.run(debug=True)
