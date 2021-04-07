import uuid
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from numpy import unicode
from sqlalchemy import and_
from models import FeedBack
from flask import json, request, render_template, flash, make_response, url_for, redirect
from settings import *
from werkzeug.security import generate_password_hash
import numpy as np
import matplotlib.pyplot as plt
import os
from utils import *
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


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
        new_feed = FeedBack(customer_name=customer_name, course_name=course_name, rating=rating, comments=comments)
        db.session.add(new_feed)
        db.session.commit()
        return render_template('success.html')
    except Exception as e:
        print(e)
        flash("Information is invalid",'danger')
        return  redirect(url_for('feed_back'))



@app.route('/rating_courses')
def rating_course():
    data= get_data_rating()
    xs=[];ys=[]
    for x,y in data:
        xs.append(x)
        ys.append(y)

    fig = create_figure(xs ,ys,'rating_coures' ,'courses','number of rating')
    url='static/images/rating_course.png'
    if os.path.exists(url):
        os.remove(url)
    fig.savefig(url)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure(xs,ys,title,ylabel,xlabel):
    fig = Figure(figsize=(16,7),dpi=120)
    axis = fig.add_subplot(1, 1, 1)
    axis.barh(xs, ys,height = 0.3)
    axis.set_title(title)
    axis.set_ylabel(ylabel)
    axis.set_xlabel(xlabel)
    axis.set_xticks(ys)
    return fig
def create_figure_line(xs,ys,title,ylabel,xlabel):
    fig = Figure(figsize=(16,7),dpi=120)
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(xs, ys,'b*--')
    axis.set_title(title)
    axis.set_ylabel(ylabel)
    axis.set_xlabel(xlabel)
    axis.set_xticks(xs)
    axis.grid(axis='y')
    return fig
@app.route('/comments_courses')
def comments_course():
    data= get_data_comments()
    xs=[];ys=[]
    for x,y in data:
        xs.append(x)
        ys.append(y)
    fig = create_figure(xs ,ys,'comments_courses', 'courses','number of comments' )
    url='static/images/comments_course.png'
    if os.path.exists(url):
        os.remove(url)
    fig.savefig(url)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/comments_dates')
def comments_dates():
    data= get_data_comments_by_date()
    xs=[];ys=[]
    for x,y in data:
        xs.append(str(x))
        ys.append(y)
    print(xs,ys)
    fig = create_figure(xs ,ys,'date' ,'courses','number of comments')
    url='static/images/comments_dates.png'
    if os.path.exists(url):
        os.remove(url)
    fig.savefig(url)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/rating')
def rating():
    data = get_each_element_rating()
    xs = np.arange(0,11,1)
    ys = [0]*11
    for  y in data:
        ys[y[0]]+=1
    fig = create_figure_line(xs, ys, 'number of rating', 'rating', 'ratings')
    url = 'static/images/rating_line.png'
    if os.path.exists(url):
        os.remove(url)
    fig.savefig(url)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')