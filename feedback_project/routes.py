import uuid
import io
import random
from flask import Response
from flask_login import login_user, logout_user, current_user
from flask_mail import Message
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from numpy import unicode
from sqlalchemy import and_
from models import FeedBack
from flask import json, request, render_template, flash, make_response, url_for, redirect
from settings import *
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import matplotlib.pyplot as plt
import os
from utils import *


def send_message(customer_name, course_name, rating, comments):
    mgs= Message('New Feedback Submission', sender='phailamsaonana@gmail.com', recipients=['bkd.hust@gmail.com'])
    mgs.body=f'''
    A new feedback    
    Customer Name: {customer_name}
    Course Name: {course_name}
    Rating: {rating}
    Comments: {comments}
    '''
    mail.send(mgs)
@app.route('/feedback', methods=['GET', 'POST'])
def feed_back():
    if request.method != 'POST':
        return render_template('feedback.html')
    try:
        customer_name = request.form.get('ten_khach_hang')
        course_name = request.form.get('ten_khoa_hoc')
        rating = request.form.get('rating')
        comments = request.form.get('phan_hoi')
        print(customer_name, course_name, rating, comments)
        new_feed = db.session.query(FeedBack).filter(
            and_(FeedBack.customer_name == customer_name, FeedBack.comments == comments,
                 FeedBack.course_name == course_name, FeedBack.rating == rating)).first()
        if new_feed:
            print('dont feed')
            flash("You have already submitted feedback",'warning')
            db.session.rollback()
            return redirect(url_for('feed_back'))
        send_message(customer_name=customer_name, course_name=course_name, rating=rating, comments=comments)
        new_feed = FeedBack(customer_name=customer_name, course_name=course_name, rating=rating, comments=comments)
        db.session.add(new_feed)
        db.session.commit()

        return render_template('success.html')
    except Exception as e:
        print(e)
        flash("Information is invalid",'danger')
        return  redirect(url_for('feed_back'))
@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('feed_back'))

@app.route('/admin_login',methods=['GET','POST'])
def login_admin():
    if current_user.is_authenticated:
        return redirect('/admin')

    if request.method == 'POST':
        username= request.form.get('username')
        password= request.form.get('pwd')
        user= db.session.query(User).filter(User.username == username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                next = request.args.get('next')
                print(next)
                if next:
                    return redirect(next)
                return redirect('/admin')
            flash('Your account is not correct')
    return render_template('admin/login.html')

