
from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import uuid
import re


app=Flask(__name__)

basedir=os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
Migrate(app, db)

class URL(db.Model):
    __tablename__= "urls"
    id=db.Column(db.Integer,primary_key=True)
    long_url=db.Column(db.String(500))
    short_url=db.Column(db.String(20))

    def __init__(self,long_url,short_url):
        self.long_url=long_url
        self.short_url=short_url

    def __repr__(self):
        return "Long Url-{}and Short_Url-{}".format(self.long_url,self.short_url)    
    
def is_valid_url(url):
    pattern = re.compile(r'^https?://(?:www\.)?.+\..+$')
    return bool(pattern.match(url))    


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        long_url=request.form['url_address']
        if not is_valid_url(long_url):
            return render_template('home.html', error='Invalid URL')
        short_url=str(uuid.uuid4())[:7]
        new_url=URL(long_url=long_url, short_url=short_url)
        db.session.add(new_url)
        db.session.commit()
        return render_template('home.html', short_url=short_url)
    else:
        return render_template('home.html')


@app.route('/<short_url>')
def redirect_url(short_url): 
    url=URL.query.filter_by(short_url=short_url).first_or_404()
    return redirect(url.long_url)


@app.route('/history')
def history():
    urls = URL.query.all()
    return render_template('history.html', urls=urls)

if __name__== '__main__':
   app.run(debug=True,port=5001)


